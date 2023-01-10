import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_bb_values(data, period = 20, std = 2):
    """
    Method to get bollinger band value with, middle, upper and lower band
    Input: 
    data: data frame with price
    period: moving average window for middle band
    std: standard deviatioin for upper and lower band
    Output:
    data frame with price,  middle, uppper, lower band
    """
    bb_data = pd.DataFrame(index=data.index)
    bb_data['price'] = data['price']
    
    bb_data['middleband']=bb_data['price'].rolling(window=period).mean()
    bb_data['upperband']=bb_data['middleband'] + std * (bb_data['price'].rolling(window=period).std())
    bb_data['lowerband']=bb_data['middleband'] - std * (bb_data['price'].rolling(window=period).std())
    return bb_data


def get_bb_signal(bb, period = 20):
    """
    Bollinger Band buy sell signal calculation
    Input: 
    data: data frame with price, lowerband, upperband
    Output:
    Data frame with buy sell signal
    """
    signals = pd.DataFrame(index=bb.index)
    signals.head()
    signals['price'] = bb['price']
    signals['sell']= 0.0
    signals['buy']= 0.0
    signals['buy'][period:] = np.where(bb['price'][period:] < bb['lowerband'][period:], -1.0, 0.0)
    signals['sell'][period:] = np.where(bb['price'][period:] > bb['upperband'][period:],1.0,0)
    signals['buy'] = signals['buy'].diff()
    signals['sell'] = signals['sell'].diff()
    signals.loc[signals['buy'] == -1.0,['buy']]=0 
    signals.loc[signals['sell'] == 1.0,['sell']]=0 
    signals['buy_sell'] = signals['buy'] + signals['sell']
    return signals[['price', 'buy_sell']]



def plot_bb_buy_sell(bb, signals):
    """
    Plot price, Bollinger band middle, lower, upper band with buy and sell signal
    """
    graph = plt.figure(figsize=(20,5))
    ax1 = graph.add_subplot(111)
    bb[['price','lowerband','upperband']].plot(ax = ax1,title ='Bollinger band Signals')
    ax1.plot(signals.loc[signals.buy_sell == 1].index, signals.price[signals.buy_sell == 1], "^", markersize = 12, color = "g")
    ax1.plot(signals.loc[signals.buy_sell == -1].index, signals.price[signals.buy_sell == -1], "v", markersize = 12, color = "m")
    # plt.show()
    plt.show()