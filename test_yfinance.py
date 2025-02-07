import yfinance as yf

symbol = "AAPL"  # Test için Apple hissesini çekelim
stock = yf.Ticker(symbol)

current_price = stock.history(period="1d")["Close"].iloc[-1]
print(f"{symbol} Hissesi Güncel Fiyatı: ${current_price}")
