from abc import ABC, abstractmethod
from .tech_indicator import TechIndicator

class Stochastic_Oscillator(TechIndicator):
    def __init__(self, tickers, length = 14, avg_len = 3):
        super().__init__(tickers, length)
        self.length = length
        self.avg_len = avg_len


    def evaluate(self, data, **kwargs):
        self.calculate(data)
        for ticker in self.tickers:
            k = self.values[ticker][-1]
            # (0,1), (20, 0.75)
            # y = -.0125x + 1 
            if k < 20:
                self.signals[ticker].append((-.0125 * k) + 1)
            # (80, 0.25), (100, 0)
            # y = (100 - x)/80    
            elif k > 80:
                self.signals[ticker].append((100 - k) / 80)
            # (20, 0.75), (80, 0.25)
            # y = (110 - x)/120
            else:
                self.signals[ticker].append((110 - k) / 120)
                


    def calculate(self, data, **kwargs):
        for ticker in self.tickers:
            prices = [data[ticker][i].c for i in range(-14,0)]
            h14 = max(prices)
            l14 = min(prices)
            close = data[ticker][-1].c 
            k = (close-l14)/(h14-l14) * 100
            self.values[ticker].append(k)

             