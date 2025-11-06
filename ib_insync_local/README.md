# NVDA Bollinger Bands Data Collector

## Overview

This project collects historical stock data for NVDA using the **IBKR API** and calculates Bollinger Bands. It saves the data into a CSV file with multiple levels of standard deviation (1σ, 2σ, 3σ).

Bollinger Bands consist of three lines:

* **Upper Band** = Simple Moving Average (SMA) + (Standard Deviation × factor)
* **Middle Band** = SMA
* **Lower Band** = SMA − (Standard Deviation × factor)

Default parameters:

* **Period** = 20 bars
* **Factor** = 2

## Folder Structure

```
ib_insync/
│
├── .env                          # Environment variables (host, port, demo_port, client_id)
├── calculate_bollinger_bands.py  # Functions to calculate Bollinger Bands using pandas or ta library
├── ib_insync_test.py              # Main script: requests historical data, calculates Bollinger Bands, writes to CSV
├── config.py                      # Configuration file using Pydantic to load environment variables
├── scrape_bars.py                 # Script to scrape historical bars iteratively, including Bollinger Bands from IBKR study
├── requirements.txt               # Python dependencies
```

## Files Description

### 1. `.env`

Contains your IBKR API credentials and connection details:

```
HOST=127.0.0.1
PORT=7496
DEMO_PORT=7497
CLIENT_ID=123
```

### 2. `config.py`

Uses **Pydantic BaseSettings** to load environment variables:

```python
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    demo_port: int
    port: int
    host: str
    client_id: Optional[int] = None

    class Config:
        env_file = "../.env"


settings = Settings()
```

### 3. `calculate_bollinger_bands.py`

Provides functions to calculate Bollinger Bands:

* Using **ta library**:

```python
from ta.volatility import BollingerBands

def calculate_bollinger_bands(df):
    for i in range(1, 4):
        indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=i)
        df[f'upper_{i}σ'] = indicator_bb.bollinger_hband()
        df[f'lower_{i}σ'] = indicator_bb.bollinger_lband()
        df['middle_band'] = indicator_bb.bollinger_mavg()
```

* Using **pandas rolling**:

```python
def calculate_bollinger_bands_pandas(df):
    period = 20
    df['middle_band'] = df['close'].rolling(window=period).mean()
    df['std_dev'] = df['close'].rolling(window=period).std()
    for i in range(1, 4):
        df[f'upper_{i}σ'] = df['middle_band'] + (df['std_dev'] * i)
        df[f'lower_{i}σ'] = df['middle_band'] - (df['std_dev'] * i)
```

### 4. `ib_insync_test.py`

* Connects to IBKR (demo or live).
* Requests **historical data** for NVDA (1 month, 2-minute bars).
* Calculates Bollinger Bands using `calculate_bollinger_bands`.
* Saves all data to CSV: `nvda_bars.csv`.

### 5. `scrape_bars.py`

* Iteratively collects historical data backward in **10-minute steps**.
* Writes the bars including **Count** and **WAP** to CSV.
* Optionally includes **Bollinger Bands** from IBKR study options.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Fill `.env` with your IBKR credentials.

3. Run the main script to collect data:

```bash
python prepare_stock_bb_data.py
```

4. To scrape iteratively with study included:

```bash
python scrape_bars.py
```

## Example CSV Output

```
date,open,high,low,close,volume,middle_band,upper_1σ,lower_1σ,upper_2σ,lower_2σ,upper_3σ,lower_3σ
2025-10-31 16:00,480,485,478,482,1200,481.5,483.2,479.8,485.0,478.0,486.8,476.2
...
```

## Requirements

```
ib_insync
pandas
ta
pydantic-settings
```

* `ib_insync` – Interactive Brokers API wrapper
* `pandas` – Data manipulation
* `ta` – Technical analysis (Bollinger Bands)
* `pydantic-settings` – Load environment variables
