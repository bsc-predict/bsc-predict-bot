class Config:
  # the amount of time to sleep between polling rounds
  sleep_seconds = 3

  # the minimum number of wins to accumulate before saving
  claim_every = 3

  # the amount of oracle history to query when starting
  oracle_history = 100 

  # dump of round history, used to check claimable
  history_url = "https://raw.githubusercontent.com/bsc-predict/bsc-predict-updater/master/data/v2/main/rounds.csv"
  
  oracle_contract = "0xD276fCF34D54A926773c399eBAa772C12ec394aC"
  prediction_contract = "0x18B2A687610328590Bc8F2e5fEdDe3b582A49cdA"
  
  # NOTE: Below are specific to prediction contract. Only change variables below if you change the prediction contract.
  bear_bet = "0xaa6b873a"
  bull_bet = "0x57fb096f"
  claim = "0x6ba4c138"