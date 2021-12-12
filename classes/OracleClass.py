from __future__ import division
from dataclasses import dataclass
from typing import List

PRICE_DIVISOR = 100000000.0

@dataclass
class Oracle:
  roundId: int
  answer: float
  startedAt: int
  updatedAt: int
  answeredInRound: int

  def __init__(self, t: List):
    roundId, \
    answer, \
    startedAt, \
    updatedAt, \
    answeredInRound = t

    self.roundId = int(roundId)
    self.answer = answer / PRICE_DIVISOR 
    self.startedAt = int(startedAt)
    self.updatedAt = int(updatedAt)
    self.answeredInRound = int(answeredInRound)
  
  def __repr__(self) -> str:
    return "Oracle(" + \
      f"roundId={self.roundId}, " + \
      f"answer={self.answer}, " + \
      f"startedAt:{self.startedAt}, " + \
      f"updatedAt: {self.updatedAt}, " + \
      f"answeredInRound: {self.answeredInRound}" + \
    ")"

