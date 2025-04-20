import finnhub


def get_stock_data(ticker):
    finnhub_client = finnhub.Client(api_key="d01tecpr01qt2u30mpkgd01tecpr01qt2u30mpl0")
    return finnhub_client.symbol_lookup(ticker)


def get_stock_price_data(ticker):
    finnhub_client = finnhub.Client(api_key="d01tecpr01qt2u30mpkgd01tecpr01qt2u30mpl0")
    return finnhub_client.quote(ticker)
