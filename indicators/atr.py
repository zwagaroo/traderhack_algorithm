from .tech_indicator import TechIndicator
from collections import deque
from statistics import mean, stdev

from scipy.stats import linregress

class ATR(TechIndicator):
    def __init__(self, tickers, length = 14):
        super().__init__(tickers, length)
        # could be using 14 or 30 day atr
        self.length = length
        self.tickers = tickers
        #print(self.tickers)
        # stores the true ranges for the past 14 trading days
        self.TRs = {ticker : deque([], maxlen=self.length) for ticker in self.tickers}
# helper
    # def select_true_range(self,data):
    #     # close open low and high
    #     for ticker in self.tickers:
    #         self.TRs[ticker] = []
    #         for i in range(-1, -, -1):
    #             cSum += data[ticker][i].c
    #             oSum += data[ticker][i].o
    #             lSum += data[ticker][i].l
    #             hSum += data[ticker][-1].h

    #     # COMPARING ALL THE VALUES TO FIND THE TRUE RANGE
    #     # current high minus current low
    #     x = highB - lowB
    #     # current high minus previous close
    #     y = abs(highB-closeB)
    #     # current low minus previous close
    #     z = abs(lowB-closeB)
    #     # USING MAX TO FIND TRUE RANGE
    #     true_range = max(x,y,z)
    #     return true_range
        
  

    def calculate(self, data, **kwargs):
        
        for ticker in self.tickers:
            self.TRs[ticker].clear()
            lookback = min(self.length, len(self.values[ticker]))
            for i in range(-1, -lookback - 1, -1):
                # high - low
                hl = abs(data[ticker][i].h - data[ticker][i].l)
                # high - close
                hc = abs(data[ticker][i].h - data[ticker][i - 1].c)
                # low - close
                lc = abs(data[ticker][i].l - data[ticker][i - 1].c)

                true_range = max(hl, hc, lc)
                self.TRs[ticker].append(true_range)
            
            sum_tr = sum(self.TRs[ticker])
            # finding average of all the true ranges for current ticker
            atr = sum_tr/ self.length
            self.values[ticker].append(atr)


    # need to come to consensus on evaluation
    def evaluate(self, data, **kwargs):
        self.calculate(data)
        for ticker in self.tickers:
            values = self.values[ticker]
            min_val = min(values)
            max_val = max(values)
            max_r = 0
            m = 0
            for i in range(4,9):
                slope, intercept, r_value, p_value, std_err = linregress([x for x in range(-i,0)],[data[ticker][x].c for x in range(-i,0)])
                if abs(r_value) > max_r:
                    max_r = abs(r_value)
                    m = slope 
            
            if max_val == min_val:
                self.signals[ticker].append(0.5)
            else:
                dev = (values[-1] - min_val)/(max_val-min_val) * 0.5
                if m != 0:
                    self.signals[ticker].append(0.5 + abs(m)/m * dev)
                else:
                    self.signals[ticker].append(0.5)

            


        
            
