from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
  BULL = 0
  BEAR = 1

@dataclass
class Bet:
  """ Class for specifying a bet """
  direction: Direction
  amount_eth: int
  epoch: int
