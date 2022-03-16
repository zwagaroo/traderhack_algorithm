from abc import ABC, abstractmethod
from .tech_indicator import TechIndicator

class RSI(TechIndicator):
    def __init__(self, tickers, length = 14):
        super().__init__(tickers, length)
        self.avg_gain = {ticker : None for ticker in self.tickers}
        self.avg_loss = {ticker : None for ticker in self.tickers}
        self.length = length

    def evaluate(self, data, **kwargs):
        self.calculate(data)
        for ticker in self.tickers:
            rsi = self.values[ticker][-1]
            if rsi < 30:
                self.signals[ticker].append((120 - rsi) / 120) # (0,1), (30, 0.75)
            elif rsi > 70:
                self.signals[ticker].append((100 - rsi) / 120)
            else:
                self.signals[ticker].append((90 - rsi) / 80)

    
    def calculate(self, data, **kwargs):
        self.calc_avgs(data)
        for t in self.tickers:
            if self.avg_loss[t] == 0:
                self.values[t].append(100)
            else:
                self.values[t].append(100 - (100/(1 + (self.avg_gain[t]/self.avg_loss[t]))))

    def calc_avgs(self, data):
        for ticker in self.tickers:
            if self.avg_gain[ticker] is None or self.avg_loss[ticker] is None:
                lookback = min(len(data[ticker]), self.length + 1)   # how many points to consider when evaluating          
                differences = [(data[ticker][x + 1].c - data[ticker][x].c) / data[ticker][x].c for x in range(len(data[ticker]) - lookback, len(data[ticker]) - 1)]
                gain_total = 0
                loss_total = 0
                for diff in differences:
                    if diff > 0:
                        gain_total += diff
                    else:
                        loss_total -= diff
                self.avg_gain[ticker] =  gain_total / self.length
                self.avg_loss[ticker] =  loss_total / self.length
            else:
                gain = 0
                loss = 0
                if (data[ticker][-1].c > data[ticker][-2].c):
                    gain = (data[ticker][-1].c - data[ticker][-2].c) / data[ticker][-2].c
                else:
                    loss = (data[ticker][-2].c - data[ticker][-1].c) / data[ticker][-2].c
                self.avg_gain[ticker] = 1/self.length * gain + (self.length - 1)/(self.length) * self.avg_gain[ticker]
                self.avg_loss[ticker] = 1/self.length * loss + (self.length - 1)/(self.length) * self.avg_loss[ticker]
            
