import seaborn as sns
from pandas import to_datetime
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, ConciseDateFormatter


sns.set_theme(style="darkgrid", context="talk")


def plot_stock(df, start: date = None):
    """
    Draws a plot of the provided stock dataframe
    Dateframe must contain columns ["Date", "Close"]

    start: date\tThe date which the x axis should start from
    """
    df["Date"] = to_datetime(df["Date"]).dt.to_pydatetime()
    locator = YearLocator(3)
    formatter = ConciseDateFormatter(locator)
    _, ax = plt.subplots(figsize=(16, 8))
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.tick_params(axis="x", labelrotation=45)
    if start is not None:
        ax.set_xlim(start, df["Date"].max())
    sns.lineplot(ax=ax, data=df, x=df["Date"], y="Close")

    plt.show()
