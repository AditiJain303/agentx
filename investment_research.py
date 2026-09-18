from market_data import get_stock_data
from alerts import check_stock_alert


def analyze_investment(symbol, investment_amount):
    data = get_stock_data(symbol)

    if data is None:
        return None

    current_price = data["close"]
    opening_price = data["open"]

    price_change = current_price - opening_price
    price_change_percent = (price_change / opening_price) * 100

    price_range = data["high"] - data["low"]

    # Convert INR to USD
    usd_amount = investment_amount / 88
    shares_possible = usd_amount / current_price

    # Check if the stock has moved significantly
    alert = check_stock_alert(symbol)

    return {
        "symbol": symbol,
        "current_price": current_price,
        "day_high": data["high"],
        "day_low": data["low"],
        "volume": data["volume"],
        "price_change": round(price_change, 2),
        "price_change_percent": round(price_change_percent, 2),
        "price_range": round(price_range, 2),
        "investment_amount_inr": investment_amount,
        "estimated_shares": round(shares_possible, 2),
        "data_confidence": "High",
        "alert": alert
    }


