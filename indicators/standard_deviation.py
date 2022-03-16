from abc import ABC, abstractmethod
from tech_indicator import TechIndicator
from statistics import stdev

class Standard_Deviation(TechIndicator):
    def __init__(self, tickers, length = 14):
        super().__init__(tickers, length)
        self.length = length

    def evaluate(self, data):
        self.calculate(data)
        for ticker in self.tickers:
            min_val = min(self.values[ticker])
            max_val = max(self.values[ticker])
            range_val = max_val - min_val
            local_max = max(self.values[ticker][-26:])
            local_min = min(self.values[ticker][-26:])
            idx_max = self.values[ticker].index(local_max)
            idx_min = self.values[ticker].index(local_min)
            # (min, 0.5), (max, 0)
            # y = 0.5/(min - max)*(x-min) + 0.5
            # (min, 0.5), (max, 1)
            # m = 0.5 / (max - min)
            # y = (0.5 / (max - min)) * x + b
            # y = 0.5 / (max - min) * x + 1 - (0.5 * max)/(max - min)
            # y = 0.5/(max - min)*(x-max) + 1
            # our opinion - lower stdev is better, but this is debatable
            if(local_max - local_min > range_val / 4): # change threshold
                if(idx_max > idx_min):
                    self.signals[ticker].append(0.5/(max_val - min_val)*(self.values[ticker][-1]-max_val) + 1) # range - 0.5 to 1
                    break
                if(idx_min > idx_max):
                    self.signals[ticker].append(0.5/(min_val - max_val)*(self.values[ticker][-1]-min_val) + 0.5)   # range - 0 to 0.5
                    break
            self.signals[ticker].append(0.5)


    def calculate(self, data):
        for ticker in self.tickers:
            prices = []
            for i in range(-1, -self.length - 1, -1):
                prices.append(data[ticker][i].c)
            self.values[ticker].append(stdev(prices))
