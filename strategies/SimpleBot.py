from strategies.BaseBot import BaseBot
from typing import Optional
from classes.RoundClass import Round
from classes.BetClass import Bet

from classes.RoundClass import Round
from typing import Optional, List
from classes.BetClass import Bet
import time

# NOTE: Class must be named Bot
class Bot(BaseBot):
  def get_bet(self, upcoming: Round) -> Optional[Bet]:
    # This function returns either a Bet or None based on the upcoming round.
    # If it returns a Bet, then that bet will be made
    # upcoming is the upcoming round that you're betting on

    # bet in the last 30 seconds
    timestamp = time.time()
    if upcoming.lockTimestamp - timestamp > 30:
      return None
    
    # you also have access to `self.history` which is the entire history of the games
    # At any time, there is an upcoming round that you can bet on, a `live` round that has not yet closed and the history  
    # here we filter on completed rounds or rounds that closed
    completed = [r for r in self.history if r.oracleCalled]

    if len(completed) > 0:
      last_winner = completed[-1]
      if last_winner.winner:
        return Bet(direction=last_winner.winner, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
    