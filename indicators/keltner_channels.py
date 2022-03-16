from .tech_indicator import TechIndicator

class Keltner_Channels(TechIndicator):
    def __init__(self, tickers, multiplier = 2):
        super().__init__(tickers, 26)   # make this un-hardcoded 
        # self.upper_line = {ticker : None for ticker in self.tickers}
        # self.lower_line = {ticker : None for ticker in self.tickers}
        # self.middle_line = {ticker : None for ticker in self.tickers}
        self.multiplier = multiplier

    def evaluate(self, data, kwargs):
        self.calculate(data, kwargs)

        for ticker in self.tickers:
            (high, low) = self.values[ticker][-1]
            if data[ticker][-1].c > high:
                self.signals[ticker].append(1)   # potentially change this from 1 -> linear scale (0.75 - 1)
            elif data[ticker][-1].c < low:
                self.signals[ticker].append(0)   # potentially change this from 0 -> linear scale (0 - 0.25)
            else:
                self.signals[ticker].append((data[ticker][-1].c - self.values[ticker][-1][1])/(self.values[ticker][-1][0] - self.values[ticker][-1][1]))# * 0.5 + 0.25)
                # top = data[ticker][-1].c - low
                # bottom = high - low
                # frac = top / bottom
                # indicator = low + frac/2
                # self.signals[ticker].append(indicator)


    def calculate(self, data, kwargs):
        newDict = {ticker : None for ticker in self.tickers}
        for ticker in self.tickers:        
            atr_val = kwargs["ATR"].get_values()[ticker][-1]
            ema_val = kwargs["EMA"].get_values()[ticker][-1]
            # Append tuple (upper, lower)
            self.values[ticker].append((ema_val + self.multiplier * atr_val, ema_val - self.multiplier * atr_val))



    
