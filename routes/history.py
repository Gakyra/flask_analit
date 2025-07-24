from flask import Blueprint, render_template
import requests
from datetime import datetime
import os

history_bp = Blueprint("history", __name__)

def get_real_data(symbol, api_key, days=5):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        return []

    raw = data["Time Series (Daily)"]
    result = []

    for date, values in sorted(raw.items())[-days:]:
        result.append({
            "date": date,
            "close": float(values["4. close"])
        })

    return result

@history_bp.route("/assets/<symbol>/history")
def history(symbol):
    api_key = os.getenv("ALPHA_KEY")
    data = get_real_data(symbol, api_key)
    return render_template("asset_history.html", symbol=symbol.upper(), data=data)
