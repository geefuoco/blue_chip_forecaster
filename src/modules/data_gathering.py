import pandas as pd
import pandas_datareader.data as reader
from datetime import datetime
import os
from pathlib import Path

_DATA_PATH = Path("../../data/").resolve()


def get_stock_data(ticker: str, force=False):
    """
    Returns a pandas Dataframe of from data folder for given ticker.
    If the file is not found, and Force=True, will query for the
    historical data and save to file

    ticker: str\tStock symbol
    force: bool\tQueries for data if not found in data path. Defaults to False
    """
    path = str(_DATA_PATH) + f"/{ticker}" + ".csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"Could not find {ticker}.csv inside of data folder")
        if force:
            print("Querying data")
            df = _query_stock_data(ticker)
            if df is not None:
                df.to_csv(path)
                return df


def _query_stock_data(ticker: str,
                      start=datetime(1980, 1, 1),
                      source="yahoo"):
    """
    Returns historical stock data as a pandas Dataframe for given
    ticker from start date to today

    ticker: str\tStock symbol.
    start: datetime date\tDefaults to 1980-01-01.
    source: str\t Date source to get info from. Find full list on
    pandas_datareader documentation.
    """
    today = datetime.today()
    try:
        stock = reader.DataReader(ticker,
                                  start=start,
                                  end=today,
                                  data_source=source)
        return stock
    except KeyError:
        print(f"Could not find ticker symbol: {ticker}")
    except Exception:
        print(f"An error occured while looking for {ticker}")
        print("Please ensure that the ticker is real")
