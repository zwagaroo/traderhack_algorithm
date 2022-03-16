from .tech_indicator import TechIndicator

class MFI(TechIndicator):

    def __init__(self, tickers, length = 14):
    
        super().__init__(tickers, length)

        self.length = length
        self.pos_mfs = {ticker: None for ticker in self.tickers}
        self.neg_mfs = {ticker: None for ticker in self.tickers}


    def evaluate(self, data, **kwargs):
    
        self.calculate(data)
        for ticker in self.tickers:

            mfi = self.values[ticker][-1]
            if mfi < 20:    # oversold: range from 0.75 - 1
                self.signals[ticker].append((80 - mfi) / 80)
            elif mfi > 80:  # overbought: range from 0 - 0.25
                self.signals[ticker].append((100 - mfi) / 80)
            else:
                self.signals[ticker].append((110 - mfi) / 120)


    def calculate(self, data, **kwargs):

        self.calc_money_flows(data)
        for ticker in self.tickers:

            # Check for neg_mfs being 0. If so, mfi = 100
            if self.neg_mfs[ticker] == 0:
                self.values[ticker].append(100)

            else:
                mf_ratio = self.pos_mfs[ticker] / self.neg_mfs[ticker]
                mf_index = 100 - (100 / (1 + mf_ratio))
                self.values[ticker].append(mf_index)

    
    def calc_money_flows(self, data):

        for ticker in self.tickers:

            past_typ_price = 0.0
            pos_mf, neg_mf = 0.0, 0.0
            prev_periods = min(self.length + 1, len(data[ticker]))

            for p in range(len(data[ticker]) - prev_periods, len(data[ticker])):

                typ_price = (data[ticker][p].h 
                            + data[ticker][p].l 
                            + data[ticker][p].c) / 3

                # We need "one past" typical price for comparison
                if not p == len(data[ticker]) - prev_periods:

                    # Compute raw money flow & add to pos/neg money flow
                    raw_mf = typ_price * data[ticker][p].v
                    if typ_price < past_typ_price:
                        neg_mf += raw_mf
                    else:
                        pos_mf += raw_mf

                past_typ_price = typ_price

            self.pos_mfs[ticker] = pos_mf
            self.neg_mfs[ticker] = neg_mf

