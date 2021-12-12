from classes.BetClass import Direction
from decimal import Decimal
from web3_provider import web3

def get_account_balance_eth(account: str) -> Decimal:
  return web3.fromWei((web3.eth.get_balance(account)), "ether")


