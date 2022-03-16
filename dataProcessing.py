from dataclasses import dataclass
from datetime import datetime
from time import time
from alpaca_key import *;
import numpy as np;
import pandas as pd
from indicators.rsi import RSI
from indicators.ema import EMA
from indicators.macd import MACD
from indicators.cci import CCI
from indicators.sma import SMA
from indicators.mfi import MFI
from indicators.atr import ATR
from indicators.vwap import VWAP
from indicators.stochastic_oscillator import Stochastic_Oscillator
from indicators.bollinger_bands import Bollinger_Bands
from indicators.keltner_channels import Keltner_Channels
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import logging
from ta import momentum
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

api  = tradeapi.REST(key_id = PUB_KEY, secret_key =SEC_KEY, base_url=BASE_URL)

data = api.get_bars(["AAPL"], TimeFrame.Hour, "2022-03-10", "2022-03-14", adjustment='raw').df

money = 100000
is_open = False

priceHistory = pd.Series()

for timestep in data.close.keys():
    tempdict = {timestep :data.close[timestep]}
    tempSeries = pd.Series(tempdict)
    priceHistory = pd.concat([priceHistory,tempSeries])
    ta.momen

print(priceHistory)

