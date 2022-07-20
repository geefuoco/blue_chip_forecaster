import seaborn as sns
from pandas import to_datetime
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import os.path as path
from matplotlib.dates import YearLocator, ConciseDateFormatter


sns.set_theme(style="darkgrid", context="talk")
_save_path = path.join(path.dirname(__file__), "../../assets/")

def plot_loss(history, save=False, name=None):
    """
    Plot the loss history from the neural network

    history: history callback from model.fit
    """
    fig, ax = plt.subplots(figsize=(16, 8))
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    df = pd.DataFrame()
    df["loss"] = loss
    df["val_loss"] = val_loss
    sns.lineplot(data=df, palette=["r", "b"], ax=ax)
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Loss (MSE)")
    ax.set_title("Loss History")
    if save and name is not None:
        plt.savefig(_save_path+name+"_loss")
    plt.show()


def plot_prediction(y_pred_unscaled, y_test_unscaled, save=False, name=None):
    fig, ax = plt.subplots(figsize=(16, 8))
    df = pd.DataFrame()
    df["actual"] = y_test_unscaled.reshape(-1)
    df["predicted"] = y_pred_unscaled.reshape(-1)
    sns.lineplot(data=df, palette=["r", "b"], ax=ax)
    ax.set_title("Predicted Stock Price vs Actual Price")
    ax.set_ylabel("Price USD")
    ax.set_xlabel("Days")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.legend()
    if save and name is not None:
        plt.savefig(_save_path+name+"_prediction")
    plt.show()


def plot_stock(df, start: date = None, save=False, name=None):
    """
    Draws a plot of the provided stock dataframe
    Dateframe must contain columns ["Date", "Close"]

    start: date\tThe date which the x axis should start from
    """
    df["Date"] = to_datetime(df["Date"]).dt.to_pydatetime()
    locator = YearLocator(3)
    formatter = ConciseDateFormatter(locator)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.tick_params(axis="x", labelrotation=45)
    if start is not None:
        ax.set_xlim(start, df["Date"].max())
    sns.lineplot(ax=ax, data=df, x="Date", y="Close")
    if save and name is not None:
        plt.savefig(_save_path+name)
    plt.show()


def plot_forecast(df, m, save=False, name=None):
    """
    Draws a plot of the forecast made from a Prophet object

    df\tForecast Dataframe from Prophet
    """
    fig = m.plot(df)
    if save and name is not None:
        fig.savefig(_save_path+name+"_forecast")
    plt.show()
