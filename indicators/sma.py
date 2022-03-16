from abc import ABC, abstractmethod
from .tech_indicator import TechIndicator

class SMA(TechIndicator):

    def __init__(self, tickers, length = 14):
        super().__init__(tickers, length)
        self.length = length
    

    def calculate(self, data, **kwargs):
        for ticker in self.tickers:
            total = 0
            for i in range(len(data[ticker]) - self.length, len(data[ticker])):
                total += data[ticker][i].c
            self.values[ticker].append(total / self.length) 

    
    def evaluate(self, data, **kwargs):
        self.calculate(data)
        for ticker in self.tickers:
            lookback = min(len(self.values[ticker]), self.length)   # how many points to consider when evaluating
            ratios = [data[ticker][i].c / self.values[ticker][i] for i in range(-lookback, 0)]
            max_r = max(ratios)
            min_r = min(ratios)

            # (max, 0), (1, 0.5) y = 0.5/(1-max) * (x-1) + 0.5
            # (1, 0.5), (min, 1) y = 0.5/(min-1) * (x-1) + 0.5

            if min_r == max_r or ratios[-1] == 1:  # neutral when we only have 1 datapoint or when close price == SMA
                self.signals[ticker].append(0.5)
            elif ratios[-1] < 1: # if closing price is below the SMA
                self.signals[ticker].append(0.5 * ((1 - ratios[-1]) / (1 - min_r)) + 0.5)
            else:   # if closing price is above the SMA
                self.signals[ticker].append(-0.5 * ((ratios[-1] - 1) / (max_r - 1))  + 0.5)


            # min_r = 0.5, max_r = 1.5
            # ratio = 0.75
            # 0.5 / (-0.5) * -0.25