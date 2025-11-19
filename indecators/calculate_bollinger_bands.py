from ta.volatility import BollingerBands

bollinger_bands_window = 20

def calculate_bollinger_bands(df):
    for i in range(1, 4):
        indicator_bb = BollingerBands(close=df["close"], window=bollinger_bands_window, window_dev=i)
        df[f'upper_{i}σ'] = indicator_bb.bollinger_hband()
        df[f'lower_{i}σ'] = indicator_bb.bollinger_lband()
        df['middle_band'] = indicator_bb.bollinger_mavg()

def calculate_bollinger_bands_pandas(df):
    # calculate Bollinger Bands
    df['middle_band'] = df['close'].rolling(window=bollinger_bands_window).mean()
    df['std_dev'] = df['close'].rolling(window=bollinger_bands_window).std()

    # 1σ, 2σ, 3σ
    for i in range(1, 4):
        df[f'upper_{i}σ'] = df['middle_band'] + (df['std_dev'] * i)
        df[f'lower_{i}σ'] = df['middle_band'] - (df['std_dev'] * i)