def analyze_item(item, market_data):
    # Примитивный анализатор
    item["score"] = market_data["market_price"] - item["price"]
    return item