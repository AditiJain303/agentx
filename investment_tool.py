from investment_research import analyze_investment


def investment_tool(symbol, investment_amount):
    result = analyze_investment(symbol, investment_amount)

    if result is None:
        return {
            "success": False,
            "message": f"Could not find market data for {symbol}."
        }

    return {
        "success": True,
        "symbol": result["symbol"],
        "current_price": result["current_price"],
        "day_high": result["day_high"],
        "day_low": result["day_low"],
        "price_change_percent": result["price_change_percent"],
        "volume": result["volume"],
        "investment_amount_inr": result["investment_amount_inr"],
        "estimated_shares": result["estimated_shares"],
        "data_confidence": result["data_confidence"],
        "alert": result["alert"]
    }


# Test
result = investment_tool("AAPL", 5000)
print(result)