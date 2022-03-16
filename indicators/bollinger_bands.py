from .tech_indicator import TechIndicator
    
class Bollinger_Bands(TechIndicator):

    def __init__(self, tickers, length = 20, std = 2):
        super().__init__(tickers, length)
        self.length = length
        self.std = std

    def calculate(self, data, **kwargs):
        for ticker in self.tickers:
            if 'kwargs' in kwargs.keys():
                kwargs = kwargs['kwargs']
            ma = kwargs['SMA'].get_values()[ticker][-1]
            
            sdeviation = 0
            for i in range(-1,-self.length - 1,-1):
                sdeviation += (data[ticker][i].c - ma) * (data[ticker][i].c - ma)
            sdeviation = (sdeviation / self.length) ** (1/2)
            # Append a tuple (high, low)
            self.values[ticker].append((ma + self.std * sdeviation, ma - self.std * sdeviation))

    def evaluate(self, data, **kwargs):
        if 'kwargs' in kwargs.keys():
            kwargs = kwargs['kwargs']
        self.calculate(data, kwargs = kwargs)
        for ticker in self.tickers:
            (high, low) = self.values[ticker][-1]
            max_val = max([data[ticker][i].c - high for i in range(len(data[ticker]))])
            min_val = min([data[ticker][i].c - low for i in range(len(data[ticker]))])
            if data[ticker][-1].c > high:
                self.signals[ticker].append(.25 * (max_val - data[ticker][-1].c)/(max_val - high)) # potentially change this from 0 -> linear scale (0 - 0.25)
            elif data[ticker][-1].c < low:
                self.signals[ticker].append(1 - .25 * (min_val - data[ticker][-1].c)/(min_val - low))   # potentially change this from 1 -> linear scale (0.75 - 1)
            else:
                self.signals[ticker].append((high - data[ticker][-1].c)/(high - low) * 0.5 + 0.25)