from config import Config
from classes.BetClass import Bet, Direction
import json
from web3_provider import web3
import os
from classes.RoundClass import Round
from typing import Tuple, List
import requests

base_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{base_path}/prediction_abi.json', 'r') as f:
  abi = json.load(f)

contract = web3.eth.contract(Config.prediction_contract, abi=abi)


def get_history() -> List[Round]:
  r = requests.get(Config.history_url)
  rounds = [Round(r.split(",")) for r in r.text.split("\n")[1:] if len(r) > 0]
  max_round = max([r.epoch for r in rounds])
  cur_epoch = get_current_epoch()
  for epoch in range(max_round, cur_epoch + 1):
    rounds.append(get_round(epoch))
  return rounds

def get_current_epoch() -> int:
  return contract.functions.currentEpoch().call()

def get_round(epoch: int) -> Round:
  r = contract.functions.rounds(epoch).call()
  return Round(r)

def get_current_round() -> Round:
    current_epoch = get_current_epoch()
    return get_round(current_epoch)

def round_to_tuple(r: Round) -> Tuple:
  return (
    r.epoch,
    r.startTimestamp,
    r.lockTimestamp,
    r.closeTimestamp,
    r.lockPrice,
    r.closePrice,
    r.lockOracleId,
    r.closeOracleId,
    r.totalAmount,
    r.bullAmount,
    r.bearAmount,
    r.rewardBaseCalAmount,
    r.rewardAmount,
    r.oracleCalled
  )

def create_bet(account: str, secret_key: str, bet: Bet):
  method = contract.functions.betBull if bet.direction == Direction.BULL else contract.functions.betBear
  transaction = method(bet.epoch).buildTransaction({
    'from': account,
    'nonce': web3.eth.getTransactionCount(account),
    'value': web3.toWei(bet.amount_eth, "ether"),
    'gas': '0',
    'gasPrice': web3.eth.gas_price,
  })
  gas = web3.eth.estimate_gas(transaction)
  transaction.update({ 'gas' : gas })

  return web3.eth.account.sign_transaction(transaction, secret_key)

def make_bet(account: str, secret_key: str, bet: Bet):
  signed_transaction = create_bet(account=account, secret_key=secret_key, bet=bet)
  return web3.eth.send_raw_transaction(signed_transaction.rawTransaction)


def get_claimable_epochs(account: str):
  # Returns claimable rounds from the 1,000 most recent rounds played 
  rounds = get_history()
  winners = {}
  for r in rounds:
    winners[r.epoch] = r.winner

  user_rounds_length = contract.functions.getUserRoundsLength(account).call()
  # getUserRounds returns uint256[], tuple[], uint256.
  # The first array is epochs, the second return (direction, size, claimed)
  # direction is 0 for BULL, 1 for bear, size is amount of wei wagered, and claimed is true of false
  start_page = max(0, (user_rounds_length - 1000))
  res = contract.functions.getUserRounds(account, start_page, 1000).call()
  epochs = res[0]
  claimable = res[1]

  # zip them up and throw it in a dictionary, then a dataframe
  claimable = [{"epoch": epoch, "direction": Direction.BULL if info[0] == 0 else Direction.BEAR , "size": info[1], "claimed": info[2]} for epoch, info in zip(epochs, claimable)]
  claimable = [c['epoch'] for c in claimable if c['direction'] == winners.get(c['epoch']) and not c['claimed']]

  return claimable
  
def claim(account: str, secret_key: str):
  claimable_epochs = get_claimable_epochs(account)
  if len(claimable_epochs) >= max(0, Config.claim_every):
    transaction = contract.functions.claim(claimable_epochs).buildTransaction({
    'from': account,
    'nonce': web3.eth.getTransactionCount(account),
    'gas': '0',
    'gasPrice': web3.eth.gas_price,
    })
    gas = web3.eth.estimate_gas(transaction)
    transaction.update({ 'gas' : gas })
    signed_transaction =  web3.eth.account.sign_transaction(transaction, secret_key)
    web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return claimable_epochs
  return []
