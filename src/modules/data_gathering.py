import pandas as pd
import pandas_datareader.data as reader
from datetime import datetime, timedelta
import os


_DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/")


def get_stock_data(ticker: str, force=False):
    """
    Returns a pandas Dataframe of from data folder for given ticker.
    If the file is not found, and Force=True, will query for the
    historical data and save to file

    ticker: str\tStock symbol
    force: bool\tQueries for data if not found in data path. Defaults to False
    """
    path = _generate_file_path(ticker)
    if os.path.exists(path):
        _update_current_data(ticker)
        return pd.read_csv(path)
    else:
        print(f"Could not find {ticker}.csv inside of data folder at {path}")

        if force:
            print("Querying data")
            df = _query_stock_data(ticker)
            if df is not None:
                df.to_csv(path)
                return df


def _update_current_data(ticker: str):
    """
    Grabs new day's data for ticker and appends it to old data. Raises
    an error if old data is not found.

    ticker: str\tStock symbol
    """
    path = _generate_file_path(ticker)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find data file in {path}")

    today = datetime.today().strftime("%Y-%m-%d")
    df = pd.read_csv(path)
    last_observation = df.tail(1)
    old_date = last_observation["Date"].values[0]

    if old_date == today:
        print("Data is up to date")
        return

    start = datetime.strptime(old_date, "%Y-%m-%d") + timedelta(1)
    observation = _query_stock_data(ticker, start=start)

    if observation is not None:
        df = pd.concat(df, observation, axis=0)
        df.to_csv(path)
        print(f"Successfully updated {ticker}.csv")


def _generate_file_path(ticker: str):
    return _DATA_PATH + f"/{ticker}" + ".csv"


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
