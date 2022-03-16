from abc import ABC, abstractmethod
from .tech_indicator import TechIndicator


class CCI(TechIndicator):
    """ CCI is a technical indicator.  """

    def __init__(self, tickers, periods=20):
        """ Initialize technical indicator.  """

        super().__init__(tickers, periods)
        self.mean_deviation = {ticker : 0.0 for ticker in self.tickers}
        self.typical_period = {ticker : [] for ticker in self.tickers}
        self.moving_average = {ticker : 0.0 for ticker in self.tickers}
        self.periods = periods

    def evaluate(self, data, **kwargs):
        """ ML to be implemented. """

        self.calculate(data)
        for ticker in self.tickers:
            max_val = max(self.values[ticker])
            min_val = min(self.values[ticker])
            avg_val = sum(self.values[ticker]) / len(self.values[ticker])

            if self.values[ticker][-1] > avg_val:
                self.signals[ticker].append((self.values[ticker][-1] - avg_val) / (max_val - avg_val) * 0.5 + 0.5)
            elif self.values[ticker][-1] < avg_val:
                self.signals[ticker].append((self.values[ticker][-1] - min_val) / (avg_val - min_val) * 0.5)
            else:
                self.signals[ticker].append(0.5)

    def calculate(self, data, **kwargs):
        """ Perform the CCI calculation. """

        self.get_data(data)
        # insert most recent typical price, ma, and mean deviation to get current cci
        for ticker in self.tickers:
            self.values[ticker].append((self.typical_period[ticker][-1] - self.moving_average[ticker]) / (0.015 * self.mean_deviation[ticker]))
        # repeat as each new period ends

    def get_data(self, data):
        """ Fill up the arrays and all necessary data for CCI calculation. """

        for ticker in self.tickers:
            self.typical_period[ticker] = []
            for period in range(1, self.periods + 1):
                close = data[ticker][-period].c
                high = data[ticker][-period].h
                low = data[ticker][-period].l
                self.typical_period[ticker].append((close + high + low) / 3)
        # sum up the typical price and divide by 20 for moving average
            # total_typical = 0
            # for period in range(self.periods):
            #     total_typical += self.typical_price[ticker][-period]
            total_typical = sum(self.typical_period[ticker])
            self.moving_average[ticker] = total_typical / self.periods
        # subtract the moving average from typical price for last 20 periods
        # sum absolute values of these and divide by 20
            total_deviation = 0
            for period in range(1, self.periods + 1):
                total_deviation += abs(self.moving_average[ticker] - self.typical_period[ticker][-period])
            self.mean_deviation[ticker] = total_deviation / self.periods
