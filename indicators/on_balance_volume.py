from abc import ABC, abstractmethod
from .tech_indicator import TechIndicator

class On_Balance_Volume(TechIndicator):
    def __init__(self, tickers):
        super().__init__(tickers, length)

    def evaluate(self, data):
        self.calculate(data)
        for ticker in self.tickers:
            min = min(self.values[ticker])
            max = max(self.values[ticker])
            # (min, 0), (max, 1)
            # y = mx + b
            # m = 1/(max - min)
            # y = 1/(max - min) * x + b
            # 0 = 1/(max - min) * min + b
            # b = -min / (max - min)
            # y = 1/(max - min) * x - min/(max - min)
            # y = (x - min) / (max - min)
            obv = self.values[ticker][-1]
            self.signals[ticker].append((obv - min) / (max - min))


    def calculate(self, data):
        for ticker in self.tickers:
            diff = data[ticker][-1].c - data[ticker][-2].c
            if len(self.values[ticker]) = 0:
                if diff > 0:
                    self.values[ticker].append(data[ticker][-1].v)
                elif diff < 0:
                    self.values[ticker].append(-data[ticker][-1].v)
                else:
                    self.values[ticker].append(0)
            else:
                if diff > 0:
                    self.values[ticker].append(self.values[ticker][-1] + data[ticker][-1].v)
                elif diff < 0:
                    self.values[ticker].append(self.values[ticker][-1] - data[ticker][-1].v)
                else:
                    self.values[ticker].append(self.values[ticker][-1])