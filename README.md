# PancakeSwap Prediction Market Starter Bot

This is a starter bot for [BSCPredict](https://bscpredict.com) or its official UI interface [PancakeSwap Prediction Markets](https://pancakeswap.finance/prediction).


**PRODUCT IS AS-IS. USE AT YOUR OWN DISCRETION**

**STRATEGIES PROVIDED ARE ONLY FOR DEMONSTRATION PURPOSES AND WILL LOSE MONEY**

# Quick Start

1. Setup your virtual environment `python3 -m venv venv && source venv/bin/activate && pip install -r requirements`

2. Copy over `.env.sample` to `.env` and update it with your account and secret key <sup>1</sup>

3. See `strategies/SimpleBot.py` for a simple "follow" strategy that copies over the last available winner. Edit the logic <sup>2</sup>

4. Run the bot `python main.py --strategy SimpleBot --size 0.001` <sup>3</sup>

5. Press CTRL+C to cancel

<sub>
1. See Security section
</sub>

<sub>
2. The SimpleBot strategy is merely for demonstration purposes. Don't run this strategy as it is surely to lose money
</sub>

<sub>
3. This will run the bot and bet 0.001 ETH per bet
</sub>

# Background

Prediction markets are 5-minute binary options on the BNB-BUSD price hosted on the Binance Smart Chain. Users can predict whether they think the price of BNB will go up or down in 5 minute intervals. Contract can be found [here](https://bscscan.com/address/0x18b2a687610328590bc8f2e5fedde3b582a49cda). See documentation [here](https://docs.pancakeswap.finance/products/prediction).


# Adding new strategies

See `SimpleBot` as an example of a strategy. You can copy this, alter it and run it with its new class name.

A strategy is defined by a class that extends `BaseClass` with a single function implementation of `get_bet(self, upcoming: Round) -> Optional[Bet]`. The function should return either a `None` or a `Bet` dataclass that's defined as follows.

```
class Direction(Enum):
  BULL = 0
  BEAR = 1

@dataclass
class Bet:
  """ Class for specifying a bet """
  direction: Direction
  amount_eth: int
  epoch: int

```

For instance, if you want to create a strategy that always bets BULL:

```
class Bot(BaseBot):
  def get_bet(self, upcoming: Round) -> Optional[Bet]:
    return Bet(direction=Direction.BULL, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)    
```

# Additional Configuration
`Config.py` has additional configuration, none of which is crucial to your both.

# Security

**NEVER SHARE YOUR PRIVATE KEYS TO ANYONE.**
If anyone has access to your private key, they can (and will) steal all your funds and you won't be able to do anything about it. 

In order for the bot to work you have to input your private key. See [metamask help](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key) for exporting your private keys.

Account and the corresponding private key need to be updated in `.env` file. **NEVER CHECK THIS FILE INTO VERSION CONTROL OR SHARE IT WITH ANYONE**

The `BaseBot` class that your strategy inherits from is initialized with your private key, and private key is passed to functions `claim` and `make_bet` in `contract/utils.py`

Review the `BaseBot` function carefully so you understand whats happening to your private key.


# Useful Links
- [BSC Predict Blog](https://bscpredict.com/blog)
- [Prediction Market Documentation](https://docs.pancakeswap.finance/products/prediction)

