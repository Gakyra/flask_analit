import requests, time

_price_sync = {}
_fallback_flags = {}

def get_current_price(symbol, retries=3):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": symbol, "vs_currencies": "usd"}
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            price = data.get(symbol, {}).get("usd")
            if price and price > 0:
                return round(price, 2)
        except Exception as e:
            print(f"[❌] CoinGecko fail [{attempt+1}/3] {symbol}: {e}")
    print(f"[⚠️] CoinGecko fallback для {symbol}")
    return get_price_from_coincap(symbol)

def get_price_from_coincap(symbol):
    mapping = {
        "bitcoin": "bitcoin",
        "ethereum": "ethereum",
        "solana": "solana",
        "dogecoin": "dogecoin",
        "binancecoin": "binance-coin",
        "cardano": "cardano"
    }
    asset_id = mapping.get(symbol)
    if not asset_id:
        print(f"[⛔] CoinCap не знает {symbol}")
        return 0.0

    url = f"https://api.coincap.io/v2/assets/{asset_id}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        price = float(data.get("data", {}).get("priceUsd", 0))
        if price > 0:
            print(f"[🟢] CoinCap цена для {symbol}: {price}")
            return round(price, 2)
    except Exception as e:
        print(f"[❌] CoinCap fail для {symbol}: {e}")
    print(f"[⛔] нет валидной цены для {symbol}")
    return 0.0

def get_synced_price(symbol, cache_sec=60):
    now = time.time()
    cached = _price_sync.get(symbol)
    if cached and now - cached["time"] < cache_sec:
        return cached["price"]

    price = get_current_price(symbol)
    if price <= 0:
        _fallback_flags[symbol] = True
        if symbol in _price_sync:
            print(f"[🔒] fallback для {symbol}, используем кэш: {_price_sync[symbol]['price']}")
            return _price_sync[symbol]["price"]
        print(f"[⛔] нет валидной цены для {symbol}")
        return 0.0

    _price_sync[symbol] = {"price": price, "time": now}
    _fallback_flags.pop(symbol, None)
    return price

def get_historical_prices(symbol, days=20):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        prices = [p[1] for p in data.get("prices", [])]
        if len(prices) >= 10 and all(p > 0 for p in prices):
            return prices
    except Exception as e:
        print(f"[❌] История цен {symbol} не загрузилась: {e}")
    print(f"[⚠️] fallback history для {symbol}")
    base = get_synced_price(symbol)
    if base <= 0:
        return []
    return [round(base * (1 + (i - 5) * 0.015), 2) for i in range(10)]
