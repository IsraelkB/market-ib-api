from ta.volatility import BollingerBands

def calculate_bollinger_bands(df):
    for i in range(1, 4):
        indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=i)
        df[f'upper_{i}σ'] = indicator_bb.bollinger_hband()
        df[f'lower_{i}σ'] = indicator_bb.bollinger_lband()
        df['middle_band'] = indicator_bb.bollinger_mavg()

def calculate_bollinger_bands_pandas(df):
    # calculate Bollinger Bands
    period = 20
    df['middle_band'] = df['close'].rolling(window=period).mean()
    df['std_dev'] = df['close'].rolling(window=period).std()

    # 1σ, 2σ, 3σ
    for i in range(1, 4):
        df[f'upper_{i}σ'] = df['middle_band'] + (df['std_dev'] * i)
        df[f'lower_{i}σ'] = df['middle_band'] - (df['std_dev'] * i)