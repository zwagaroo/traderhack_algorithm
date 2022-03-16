from .tech_indicator import TechIndicator
from types import *

smoothing = 2

class EMA(TechIndicator):

    def __init__(self, tickers, length = 14):
        super().__init__(tickers, length)
        self.length = length

    def calculate(self, data, **kwargs):
        for ticker in self.tickers:
            if len(self.values[ticker]) == 0:
                #Calculate the SMA since no previous EMA data
                total = 0

                for price in data[ticker][:self.length]:
                    total += price.c

                simpleSMA = total / self.length
                self.values[ticker].append(simpleSMA)
            else:
                prevEMA = self.values[ticker][-1]
                price = data[ticker][-1].c

                kVal = smoothing / (1 + self.length)
                newEMA = (price * kVal) + (prevEMA * (1 - kVal))
                self.values[ticker].append(newEMA)
                


        # for ticker in self.tickers:
        #     if len(self.values[ticker]) == 0:
        #         # sma
        #         total = 0
        #         for i in range(-1, -self.length - 1, -1):
        #             total += data[ticker][i].c
        #         self.values[ticker].append(total/self.length)
        #     else:
        #         # ema
        #         priceToday = data[ticker][-1].c
        #         kVal = smoothing / (1 + self.length)
        #         yesterdayEMA = self.values[ticker][-1]
        #         newEMA = (priceToday * kVal) + (yesterdayEMA * (1 - kVal))
        #         self.values[ticker].append(newEMA)
    
    def evaluate(self, data, **kwargs):
        self.calculate(data)
        for ticker in self.tickers:
            lookback = min(self.length, len(self.values[ticker]))
            diffs = [data[ticker][i].c - self.values[ticker][i] for i in range(-1, -lookback - 1, -1)]
            
            local_max = max(diffs)
            local_min = min(diffs)
            if local_max == local_min:
                self.signals[ticker].append(0.5)
            else:
                self.signals[ticker].append((local_max - diffs[-1]) / (local_max - local_min))


# why does this exist? it is never called    
def calculate(data, period, **kwargs):
    prevEMA = kwargs['prevEMA']
    if type(data) is ListType:
        return calculate_list(data, period, prevEMA)
    elif type(data) is DictType:
        new = {}
        for key in data:
            if prevEMA is None:
                new[key] = calculate_list(data[key], period)
            else:
                new[key] = calculate_list(data[key], period, prevEMA[key])
        return new
    return None

def calculate_list(data, period, prevEMA = None):
    if prevEMA is None:
        ema = 0
        for i in range(period):
            ema += data[i]
        ema /= period
        for i in range(1, period):
            kVal = smoothing / (1 + period)
            ema = (data[i] * kVal) + (ema * (1 - kVal))
        return ema
    kVal = smoothing / (1 + period)
    ema = (data[-1] * kVal) + (prevEMA * (1 - kVal))
    return ema