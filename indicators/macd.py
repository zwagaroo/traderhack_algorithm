from .tech_indicator import TechIndicator
from collections import deque
from statistics import mean, stdev

max_days_streak = 30

class MACD(TechIndicator):
    def __init__(self, tickers, short_len = 12, long_len = 26, signal_len = 9):
        super().__init__(tickers, long_len)
        self.short_len = short_len
        self.long_len = long_len
        self.signal_len = signal_len

        self.long = {ticker : None for ticker in self.tickers}
        self.short = {ticker : None for ticker in self.tickers}
        self.signal = {ticker : deque(maxlen=self.signal_len) for ticker in self.tickers}

    def calculate(self, data, **kwargs):
        self.find_short_long(data)
        for ticker in self.tickers:
            self.signal[ticker].append(self.short[ticker] - self.long[ticker])
            self.values[ticker].append(self.signal[ticker][-1] - sum(self.signal[ticker]) / self.signal_len)
        

    def evaluate(self, data, **kwargs):
        self.calculate(data)
        for ticker in self.tickers:
            days_streak = 0
            is_positive_streak = True
            # keep track of consecutive days macd is positive or negative
            for i in range(-1, -len(self.values[ticker]) - 1, -1):
                if i == -1 and self.values[ticker][i] < 0:
                    is_positive_streak = False
                if self.values[ticker][i] >= 0 and is_positive_streak:
                    days_streak += 1
                elif self.values[ticker][i] < 0 and not is_positive_streak:
                    days_streak += 1
                else:
                    break

            most_recent_macd = self.values[ticker][-1]
            booster = days_streak * 0.01
            
            max_num = max(self.values[ticker])
            min_num = min(self.values[ticker])
            if most_recent_macd > 0:
                self.signals[ticker].append(min(0.5 / max_num * most_recent_macd + 0.5 + booster, 1))
            else:
                self.signals[ticker].append(max(-0.5 / min_num * most_recent_macd + 0.5 - booster, 0))
                    
                    
        
    def find_short_long(self, data):
        for ticker in self.tickers:
            if self.long[ticker] is None or self.short[ticker] is None:
                # long period sma and short period sma
                short_sum = 0
                for i in range(-1, -self.short_len - 1, -1):
                    short_sum += data[ticker][i].c
                long_sum = short_sum
                self.short[ticker] = short_sum / self.short_len
                for i in range(-self.short_len - 1, -self.long_len - 1, -1):
                    long_sum += data[ticker][i].c
                self.long[ticker] = long_sum / self.long_len
                    
            else:
                self.long[ticker] = (self.long[ticker] * (self.long_len - 1) + data[ticker][-1].c) / self.long_len
                self.short[ticker] = (self.short[ticker] * (self.short_len - 1) + data[ticker][-1].c) / self.short_len
