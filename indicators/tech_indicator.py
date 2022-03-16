from abc import ABC, abstractmethod
from collections import deque
from itertools import islice


class TechIndicator(ABC):

    def __init__(self, tickers, length, data=None, **kwargs):

        self.length = length
        self.tickers = tickers
        # stores actual indicator values
        self.values = {ticker: list() for ticker in tickers}
        # stores buy/sell signals based on each indicator
        self.signals = {ticker: list() for ticker in tickers}

        if data:
            self.populate(data, kwargs=kwargs)

    @abstractmethod
    def calculate(self, data, **kwargs):
        """
        Computes & stores the indicator value inside self.values.
        """
        pass

    @abstractmethod
    def evaluate(self, data, **kwargs):
        """
        Computes & stores the buy/sell signal inside self.signals.
        The buy/sell signal must be in between 0-1, with 0 = strong sell, 1 = strong buy
        """
        pass

    def get_values(self):
        return self.values

    def get_signals(self):
        return self.signals

    def populate(self, data, **kwargs):

        # this is here for legacy reasons, not entirely sure about it
        if 'kwargs' in kwargs.keys():
            kwargs = kwargs['kwargs']

        for ticker in self.tickers:

            # if for some reason our calculations & evaluations don't match, reset both of them to empty
            if len(self.values[ticker]) != len(self.signals[ticker]):
                self.values[ticker].clear()
                self.signals[ticker].clear()

            # if an indicator relies on previous N days of data, we can only start computing it on Nth day
            # e.g. for a 12-day SMA, we need 12 data points, so we start calculating the SMA at index 12
            start = self.length - 1
            # if we already have x values computed, we can skip to index start + x
            start += len(self.values[ticker])

            # run evaluate() (which calls calculate) on first i times of data
            for i in range(start, len(data[ticker])):
                data_for_first_i_times = {
                    ticker: data[ticker][:i+1] for ticker in self.tickers}
                self.evaluate(data_for_first_i_times, kwargs=kwargs)

        # the first few evaluations will probably be bad since there is minimal data,
        # so we will drop the first <self.length> items from calculations & evaluations data
        # self.values = {ticker: self.values[ticker][self.length:] for ticker in self.tickers}
        # self.signals = {ticker: self.signals[ticker][self.length:] for ticker in self.tickers}
