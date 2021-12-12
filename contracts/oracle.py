from config import Config
from classes.BetClass import Bet, Direction
import json
from web3_provider import web3
import os
from classes.OracleClass import Oracle
from typing import List

base_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{base_path}/oracle_abi.json', 'r') as f:
  abi = json.load(f)

oracle = web3.eth.contract(Config.oracle_contract, abi=abi)

def get_oracle_history(n: int) -> List[Oracle]:
  """ Returns last n oracle outputs """
  latest = oracle.functions.latestRound().call()
  return get_latest_oracle_data(latest - n)

def get_latest_oracle_data(start_round_id: int) -> List[Oracle]:
  """ Returns oracle data since start round id provided """
  latest = oracle.functions.latestRound().call()
  if start_round_id >= latest:
    return []

  out = []
  for n in range(start_round_id + 1, latest + 1):
    o = Oracle(oracle.functions.getRoundData(n).call())
    out.append(o)
  return out
