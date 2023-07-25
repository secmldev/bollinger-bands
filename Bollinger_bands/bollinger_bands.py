import pandas as pd
import yfinance as yf
import os
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


class TechnicalIndicators():
    """ """
    def __init__(self, download_path) -> None:
        self.download_path = download_path
    
    def download_data(self, symbol, from_dt, to_dt, data_path = None):
        """
        This method downloads the data from yahoo finance.\n\n
        
        Input parametes:\n
        symbol --> Needs to provide appropriete symbol.\n
            Ex: symbol = 'TATASTEEL.NS'
        from_dt = From date should be in only in YYYY-DD-MM format.\n
        to_dt = To date should be in only in YYYY-DD-MM format.\n
        """
        file_name = f"./20230702/Bollinger_bands/data/{symbol}.csv"
        df = yf.download(symbol, from_dt, to_dt, actions=True)
        if not os.path.exists('./20230702/Bollinger_bands/data/'):
            os.makedirs(data_path)
        df.to_csv(file_name)
        return file_name
        
    def read_csv(
            self,
            data_path,
            set_index = None,
            req_cols = None
        ) -> pd.DataFrame:
        """ 
        This method reads the data from csv file and returns a dataframe.\n
        data_path = Accepts only .csv file.
        set_index = index column name
        req_cols = default is none and default columns are [Date, Adj Close],
        if wish to further column, provide column name in list
        -> ['OPEN','HIGH','LOW']
        Ex:
        data_path = "C:path\\to\\dataset.csv"
        """
        try:
            df = pd.read_csv(data_path, index_col="Date")
            if req_cols == None:
                return df[['Adj Close']]
            else:
                return df[req_cols]
        except FileNotFoundError as fnf:
            print(fnf.args)

    def bolling_band_calc(self, df, period:int = 20):
        """
        This method calculates the bollinger band
        
        Input parameters:
        period = default set to 14 days sma, or change it to as required.
        """
        # Calculate standard deviation
        df['std'] = df['Adj Close'].rolling(window=20).std()
        # sma 20 or middle band (BB)
        df['mid_band'] = df['Adj Close'].rolling(window=20).mean()
        df['upper_band'] = df['mid_band'] + (df['std'] * 2)
        df['lower_band'] = df['mid_band'] - (df['std'] * 2)
        return df

    def generate_signals(self, data):
        """
        Generate buy and sell signals based on Bollinger Bands.

        Args:
            data (pd.DataFrame): DataFrame containing the stock data.

        Returns:
            pd.DataFrame: DataFrame with buy and sell signals added.
        """
        data['buy']= 0.0
        data['sell']= 0.0
        data['buy'] = np.where(data['Adj Close'] < data['lower_band'], 1, 0)
        data['sell'] = np.where(data['Adj Close'] > data['upper_band'], -1, 0)
        data['buy'] = data['buy'].diff()
        data['sell'] = data['sell'].diff()
        data.loc[data['buy']==-1.0,['buy']]=0 
        data.loc[data['sell']== 1.0,['sell']]=0 
        data['Signal'] = data['buy'] + data['sell']
        print(data)
        return data

    def plot_bollinger_band(self, data):
        """
        """
        fig, ax1 = plt.subplots()
        ax1.plot(data.index, data['Adj Close'], color='blue')
        ax1.set_ylabel('Price', color='blue')

        ax2 = ax1.twinx()
        ax2.plot(data.index, data['upper_band'], color='red', linestyle='dashed', label='Upper Band')
        ax2.plot(data.index, data['lower_band'], color='green', linestyle='dashed', label='Lower Band')

        buy_signals = data[data['Signal'] == 1]
        sell_signals = data[data['Signal'] ==-1]
        ax1.scatter(buy_signals.index, buy_signals['Adj Close'], color='green', marker='^', label='Buy Signal')
        ax1.scatter(sell_signals.index, sell_signals['Adj Close'], color='red', marker='v', label='Sell Signal')

        plt.title('Bollinger Bands with Buy/Sell Signals - ' + 'TATAMOTORS')
        plt.xlabel('Date')
        plt.legend(loc='best')
        plt.show()


ti = TechnicalIndicators("20230702/Bollinger_bands/data")
data = ti.download_data('TATAMOTORS.NS', "2020-07-01", "2023-07-03")
df = ti.read_csv(data)
df = ti.bolling_band_calc(df)
ti.generate_signals(df)
ti.plot_bollinger_band(df)


