from contracts.oracle import get_latest_oracle_data, get_oracle_history
from config import Config
from classes.RoundClass import Round
from contracts.prediction import claim, get_current_epoch, get_history, get_round,  make_bet
from typing import Optional
from classes.BetClass import Bet
from time import sleep
import logging
import time

log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

class BaseBot:  
  def __init__(
    self,
    account: str,
    secret_key: str,
    bet_size_eth: float,
    min_balance_eth: float,
    dry: bool = False
  ):
    self.last_claim = 0
    self.history = get_history()
    self.oracle_history = get_oracle_history(Config.oracle_history)
    
    self.epochs_bet = set()
    self.name = __class__
    self.account = account
    self.secret_key = secret_key
    self.min_balance_eth = min_balance_eth
    self.bet_size_eth = bet_size_eth
    self.dry = dry
    logging.info(f"Created bot {__class__}")
  
  def __update_rounds(self):
    last_completed = max([r.epoch for r in self.history if r.oracleCalled])
    remaining = [r for r in self.history if r.epoch <= last_completed]
    cur_epoch = get_current_epoch()
    update = [get_round(epoch) for epoch in range(last_completed, cur_epoch + 1)]
    self.history = remaining + update

  def __update_oracle(self):
    last_oracle = max([o.roundId for o in self.oracle_history])
    update = get_latest_oracle_data(last_oracle)
    self.oracle_history = self.oracle_history + update

  def __get_bettable_round(self) -> Optional[Round]:
    if len(self.history) == 0:
      return None
    latest = self.history[-1]
    timestamp = time.time()
    # NOTE: must account for bufferSeconds (30 seconds)
    start_timestamp = latest.startTimestamp + 30
    if start_timestamp <= timestamp and latest.lockTimestamp >= timestamp and latest.epoch not in self.epochs_bet:
      return latest

  def get_bet(self) -> Optional[Bet]:
    raise NotImplementedError("get_bet not implemented")

  def run(self):
    logging.info(f"Starting bot {self.name}")
    while True:
      now = time.time()
      since_last_claim_attempt = now - self.last_claim
      if since_last_claim_attempt >= 300 and not self.dry:
        self.last_claim = now
        try:
          claimed = claim(account=self.account, secret_key=self.secret_key)
          if len(claimed) > 0:
            logging.info(f"Claimed epochs {claimed}")
        except Exception as e:
          logging.error("Attempt claim failed", e)
      self.__update_rounds()
      self.__update_oracle()
      bettable_round = self.__get_bettable_round()
      if bettable_round:
        bet = self.get_bet(bettable_round)
        if bet:
          logging.info(f"Making bet {bet}")
          self.epochs_bet.add(bettable_round.epoch)
          try:
            if not self.dry:
              make_bet(account=self.account, secret_key=self.secret_key, bet=bet )
            logging.info("Bet success")
          except Exception as e:
            logging.error("Bet failed", e)
        sleep(Config.sleep_seconds)
      pass
