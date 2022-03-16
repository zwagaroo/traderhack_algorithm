from abc import ABC, abstractmethod
from .tech_indicator import TechIndicator


class VWAP(TechIndicator):

    def __init__(self, tickers, length=20):
        super().__init__(tickers, length)
        self.length = length

    def calculate(self, data, **kwargs):
        for ticker in self.tickers:
            sum_total_price = 0
            total_volume = 0
            for i in range(len(data[ticker]) - self.length, len(data[ticker])):
                sum_total_price += (data[ticker][i].c + data[ticker]
                                    [i].h + data[ticker][i].l)/3*data[ticker][i].v
                total_volume += data[ticker][i].v

            self.values[ticker].append(sum_total_price/total_volume)

    def evaluate(self, data, **kwargs):
        self.calculate(data)

        for ticker in self.tickers:
            lookback = min(len(self.values[ticker]), self.length)
            diffs = [data[ticker][i].c - self.values[ticker][i]
                     for i in range(-1, -lookback - 1, -1)]

            if (len(diffs) == 0):
                self.signals[ticker].append(.5)
            else:
                max_diff = max(diffs)
                min_diff = min(diffs)
                if (max_diff == min_diff):
                    self.signals[ticker].append(.5)
                else:
                    self.signals[ticker].append(
                        (max_diff - diffs[-1]) / (max_diff - min_diff))

            # min_diffs corresponds to a 1, max_diffs corresponds to a 0

        # c = closing, o = opening, v = volume, l = low, h = high
