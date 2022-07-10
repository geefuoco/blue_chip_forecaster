import pandas as pd
import pandas_datareader.data as reader
from datetime import datetime, timedelta, date
import os
import subprocess

_DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/")


def get_headlines_data(crawler):
    """
    Returns the headlines dataframe up to date for today

    crawler: WSJCrawler\tCrawler to grab data if it needs to be updated
    """
    path = _DATA_PATH + "headlines_data/headlines_data.csv"
    if not os.path.exists(path):
        print("Could not find headlines data. Consider using WSJCrawler")
        return
    df = pd.read_csv(path)

    df = _update_headlines_data(df, crawler)
    return df


def _update_headlines_data(df: pd.DataFrame, crawler):
    """
    Updates the provided dataframe with the latest WSJ Headlines

    df: pd.Dataframe of headlines data
    crawler: WSJCrawler\tCrawler to crawl WSJ
    """
    latest = pd.to_datetime(df["date"].max()).date()
    today = date.today()

    if latest < today:
        print("Fetching latest headlines...")
        try:
            crawler.crawl(latest + timedelta(1), today)
        except Exception:
            print("Error while grabbing latest headlines")
            return
        name = today.strftime("%Y-%m-%d") + "_headlines.csv"
        crawler.save_headlines(name)
        new_df = pd.read_csv(_DATA_PATH + f"wsj_archive/{name}")
        new_df = _transform_to_headlines_df(new_df)
        df = pd.concat((df, new_df))
        df.to_csv(_DATA_PATH + "headlines_data/headlines_data.csv", index=False)
        print("Headlines data updated")
    return df


def _transform_to_headlines_df(df: pd.DataFrame):
    """
    Returns a new dataframe that is the same format as a headlines dataframe

    df: pd.DataFrame\tThe dataframe to transform
    """
    new_df = df
    new_df = new_df.T.reset_index().rename(columns={"index": "date"})
    new_df.columns = [str(c) for c in new_df.columns]
    return new_df


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
        return pd.read_csv(path, parse_dates=["Date"])
    else:
        print(f"Could not find {ticker}.csv inside of data folder at {path}")

        if force:
            print("Querying data")
            df = _query_stock_data(ticker)
            if df is not None:
                df = df.reset_index()
                df.to_csv(path, index=False)
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

    old_date = subprocess.check_output([f"tail -1 {path} | cut -d, -f1"], shell=True)
    old_date = old_date.decode("utf-8").rstrip()
    old_date = datetime.strptime(old_date, "%Y-%m-%d").date()

    if not _valid_time_to_update(old_date):
        print("Data is up to date")
        return

    start = old_date + timedelta(1)
    observation = _query_stock_data(ticker, start=start)

    if observation is not None:
        df = pd.read_csv(path)
        df = pd.concat(df, observation, axis=0)
        df.to_csv(path)
        print(f"Successfully updated {ticker}.csv")


def _valid_time_to_update(old_date: datetime):
    today = datetime.today()
    today_date = today.date()
    today_market_close = datetime.strptime(
        today.strftime("%Y-%m-%d") + " 16", "%Y-%m-%d %H"
    )
    weekday = int(today.strftime("%w"))
    # Not the same day and the market has closed and its not weekend
    return (
        old_date < today_date and today >= today_market_close and weekday in range(1, 6)
    )


def _generate_file_path(ticker: str):
    return _DATA_PATH + f"{ticker}" + ".csv"


def _query_stock_data(ticker: str, start=datetime(1980, 1, 1), source="yahoo"):
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
        stock = reader.DataReader(ticker, start=start, end=today, data_source=source)
        return stock
    except KeyError:
        print(f"Could not find ticker symbol: {ticker}")
    except Exception:
        print(f"An error occured while looking for {ticker}")
        print("Please ensure that the ticker is real")
