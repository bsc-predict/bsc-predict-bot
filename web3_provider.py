from web3 import Web3
from web3.middleware import geth_poa_middleware

web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

