from __future__ import division
from classes.BetClass import Direction
from dataclasses import dataclass
from typing import List

WEI_TO_ETH = 1000000000000000000.0
PRICE_DIVISOR = 100000000.0



@dataclass
class Round:
    epoch: int
    startTimestamp: int
    lockTimestamp: int
    closeTimestamp: int
    lockPrice: float
    closePrice: float
    lockOracleId: str
    closeOracleId: str
    totalAmount: float
    bullAmount: float
    bearAmount: float
    rewardBaseCalAmount: float
    rewardAmount: int
    oracleCalled: bool

    def __init__(self, t: List):
      epoch, \
      startTimestamp, \
      lockTimestamp, \
      closeTimestamp, \
      lockPrice, \
      closePrice, \
      lockOracleId, \
      closeOracleId, \
      totalAmount, \
      bullAmount, \
      bearAmount, \
      rewardBaseCalAmount, \
      rewardAmount, \
      oracleCalled = t

      self.epoch = int(epoch)
      self.startTimestamp = int(startTimestamp)
      self.lockTimestamp = int(lockTimestamp)
      self.closeTimestamp = int(closeTimestamp)
      self.lockPrice = int(lockPrice) / PRICE_DIVISOR
      self.closePrice = int(closePrice) / PRICE_DIVISOR
      self.lockOracleId = lockOracleId
      self.closeOracleId = closeOracleId
      self.totalAmount = int(totalAmount) / WEI_TO_ETH
      self.bullAmount = int(bullAmount) / WEI_TO_ETH
      self.bearAmount = int(bearAmount) / WEI_TO_ETH
      self.rewardBaseCalAmount = int(rewardBaseCalAmount) / WEI_TO_ETH
      self.rewardAmount = int(rewardAmount) / WEI_TO_ETH
      self.oracleCalled = str(oracleCalled).lower().startswith("true")
      
      winner = None
      if self.oracleCalled:
        if self.closePrice < self.lockPrice:
          winner = Direction.BEAR
        elif self.closePrice > self.lockPrice:
          winner = Direction.BULL
      self.winner = winner


