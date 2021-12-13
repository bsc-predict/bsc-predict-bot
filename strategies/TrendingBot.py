from strategies.BaseBot import BaseBot
from typing import Optional
from classes.RoundClass import Round
from classes.BetClass import Bet, Direction

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
    
    # Look at the last 5 oracle values
    # NOTE: Oracle is the "current" price. Oracles get updated more frequently than rounds.
    last_oracles = self.oracle_history[-5:]

    # assume both bullish and bearish
    # bullish means every oracle print is greater than the prior (e.g. [500, 500.1, 500.2, 500.3, 500.4])
    # bearish means every oracle print is lower than the prior
    bullish = True
    bearish = True
    
    prior = last_oracles[0]
    for o in last_oracles[1:]:
      # oracle is lower than the prior, so not bullish
      if o.answer < prior.answer:
        bullish = False
      # oracle is greater than the prior, so not bearish
      elif o.answer > prior.answer:
        bearish = False
      prior = o

    if bullish:
      # if last 5 value are trending up, bet BULL
      return Bet(direction=Direction.BULL, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
    elif bearish:
      # if last 5 value are trending down, bet BEAR
      return Bet(direction=Direction.BEAR, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
    