import yfinance as yf
from market_data import get_stock_data


alerts = []


def create_alert(alert_type, title, message):
    alert = {
        "type": alert_type,
        "title": title,
        "message": message,
        "read": False
    }

    alerts.append(alert)
    return alert


def get_alerts():
    return alerts


def check_stock_alert(symbol, threshold=1):
    data = get_stock_data(symbol)

    if data is None:
        return None

    price_change_percent = (
        (data["close"] - data["open"]) / data["open"]
    ) * 100

    if abs(price_change_percent) >= threshold:
        direction = "up" if price_change_percent > 0 else "down"

        return create_alert(
            "stock",
            f"{symbol} Price Alert",
            f"{symbol} is {direction} "
            f"{abs(price_change_percent):.2f}% today."
        )

    return None


def get_ipo_data():
    calendar = yf.Calendars()
    ipo_data = calendar.get_ipo_info_calendar(limit=10)

    return ipo_data


def check_ipo_alert():
    ipo_data = get_ipo_data()

    if ipo_data is None or ipo_data.empty:
        return None

    first_ipo = ipo_data.iloc[0]

    symbol = first_ipo.name
    company = first_ipo.get("Company", "Unknown company")

    return create_alert(
        "ipo",
        f"New IPO Alert: {symbol}",
        f"{company} has an upcoming IPO."
    )