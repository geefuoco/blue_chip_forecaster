from prophet import Prophet


def forecast_prophet(df, num_days=1):
    """
    Returns a pandas Dataframe of forecasted closing price for the number of days
    and the Prophet model

    df: pandas.DataFrame\tDataframe containing columns ["Date", "Closing"]
    num_days: int\tThe number of days to forecast
    """
    data = df[["Date", "Close"]]
    data.columns = ["ds", "y"]
    m = Prophet()
    m.fit(data)

    future = m.make_future_dataframe(periods=num_days)
    forecast = m.predict(future)
    return forecast, m
