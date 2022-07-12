import alpaca_trade_api as trade_api
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(__file__, "../../.env"))

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
URL = "https://paper-api.alpaca.markets"

alpaca = trade_api.REST(API_KEY, API_SECRET, URL, api_version="v2")


def place_order(ticker: str, quantity: int, type: str):
    """
    Place an order for a stock

    ticker: str\t Stock ticker
    quantity: int\t Quantity
    type: str\t "buy" or "sell"
    returns: Order Entity
    """
    try:
        order = alpaca.submit_order(
            ticker,
            quantity,
            type,
            type="market",
        )
        return order
    except trade_api.rest.APIError:
        print("Could not fulfill order")


def view_orders(status: str):
    """
    Returns a list of orders

    status: str\t Status of the orders you want to retrieve. "open", "closed"
    returns: list\t Order List
    """
    try:
        orders = alpaca.list_orders(status)
        return orders
    except trade_api.rest.APIError:
        print("Could not retrieve orders")


def get_order(order_id):
    """
    Returns an order from a given order id

    order_id: int\t Id of the order
    returns: Order Entity
    """
    try:
        order = alpaca.get_order(order_id)
        return order
    except trade_api.rest.APIError:
        print("Could not retrieve orders")


def get_account():
    """
    Get the account associated with the API key
    returns: Alapca Account
    """
    return alpaca.get_account()
