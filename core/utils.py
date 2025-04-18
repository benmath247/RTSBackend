import finnhub

def get_stock_data(ticker):
    finnhub_client = finnhub.Client(api_key="cndqam1r01qml3k1pbi0cndqam1r01qml3k1pbig")
    return finnhub_client.symbol_lookup(ticker)

def get_stock_price_data(ticker):
    finnhub_client = finnhub.Client(api_key="cndqam1r01qml3k1pbi0cndqam1r01qml3k1pbig")
    return finnhub_client.quote(ticker)
