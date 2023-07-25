import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

class VoRSI:
    """
    Class for calculating Volume-based Relative Strength Index (VoRSI) and generating buy/sell signals.

    Args:
        ticker (str): Ticker symbol of the stock.
        window (int): Window size for calculating the VoRSI.
        threshold_high (float): High threshold for generating sell signal.
        threshold_low (float): Low threshold for generating buy signal.
        start_date (str): Start date for fetching the stock data in the format 'YYYY-MM-DD'.
        end_date (str): End date for fetching the stock data in the format 'YYYY-MM-DD'.
    """

    def __init__(self, ticker, window=14, threshold_high=70, threshold_low=30, start_date='2022-01-01',
                 end_date='2023-07-01'):
        self.ticker = ticker
        self.window = window
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):
        """
        Download stock data using yfinance library.

        Returns:
            pd.DataFrame: DataFrame containing the stock data.
        """
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return df

    def calculate_vorsi(self, data):
        """
        Calculate Volume-based Relative Strength Index (VoRSI).

        Args:
            data (pd.DataFrame): DataFrame containing the stock data.

        Returns:
            pd.DataFrame: DataFrame with VoRSI column added.
        """
        up_volume = data['Volume'].where(data['Close'] > data['Close'].shift(1), 0)
        down_volume = data['Volume'].where(data['Close'] < data['Close'].shift(1), 0)

        avg_up_volume = up_volume.rolling(window=self.window).mean()
        avg_down_volume = down_volume.rolling(window=self.window).mean()

        vorsi = (avg_up_volume / (avg_up_volume + avg_down_volume)) * 100

        data['VoRSI'] = vorsi
        return data

    def generate_signals(self, data):
        """
        Generate buy and sell signals based on VoRSI thresholds.

        Args:
            data (pd.DataFrame): DataFrame containing the stock data.

        Returns:
            pd.DataFrame: DataFrame with buy and sell signals added.
        """
        data['buy']= 0.0
        data['sell']= 0.0
        data['buy'] = np.where(data['VoRSI'] < self.threshold_low, -1.0, 0.0)
        data['sell'] = np.where(data['VoRSI'] > self.threshold_high, 1.0, 0.0)
        data['buy'] = data['buy'].diff()
        data['sell'] = data['sell'].diff()
        data.loc[data['buy']==-1.0,['buy']]=0 
        data.loc[data['sell']== 1.0,['sell']]=0 
        data['Signal'] = data['buy'] + data['sell']
        return data

    def plot_chart(self, data):
        """
        Plot the stock price with RSI and buy/sell signals.

        Args:
            data (pd.DataFrame): DataFrame containing the stock data with signals.

        Returns:
            None
        """
        fig, ax1 = plt.subplots(figsize=(12,6))
        ax1.plot(data.index, data['Adj Close'], color='blue')
        ax1.set_ylabel('Price', color='blue')

        ax2 = ax1.twinx()
        ax2.plot(data.index, data['VoRSI'], color='purple', label='RSI', linestyle='dotted')

        buy_signals = data[data['Signal'] == 1]
        sell_signals = data[data['Signal'] == -1]
        ax1.scatter(buy_signals.index, buy_signals['Adj Close'], color='green', marker='^', label='Buy Signal')
        ax1.scatter(sell_signals.index, sell_signals['Adj Close'], color='red', marker='v', label='Sell Signal')

        plt.title('VoRSI with Buy/Sell Signals - ' + self.ticker)
        plt.xlabel('Date')
        plt.legend(loc='best')
        plt.show()

    def run_strategy(self):
        """
        Run the VoRSI strategy by downloading data, calculating VoRSI, generating signals, and plotting the chart.

        Returns:
            None
        """
        # Download stock data
        data = self.download_data()

        # Calculate VoRSI
        data = self.calculate_vorsi(data)

        # Generate signals
        data = self.generate_signals(data)

        # Plot chart
        self.plot_chart(data)

# # # Example usage
# ticker = 'TATAMOTORS.NS'  # Replace with your desired stock ticker symbol
# window = 14
# threshold_high = 75
# threshold_low = 25
# vorsi = VoRSI(ticker, window, threshold_high, threshold_low, "2022-01-01", "2023-07-06")
# vorsi.run_strategy()