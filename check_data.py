from app import db, Stock, Transaction, app

with app.app_context():
    stocks = Stock.query.all()
    print("📊 Hisseler:")
    for stock in stocks:
        print(f"Hisse: {stock.symbol}, Adet: {stock.quantity}, Alış Fiyatı: {stock.purchase_price}, Güncel Fiyat: {stock.current_price}")

    transactions = Transaction.query.all()
    print("\n🔄 İşlemler:")
    for transaction in transactions:
        print(f"İşlem: {transaction.transaction_type}, Hisse: {transaction.stock_symbol}, Miktar: {transaction.quantity}, Fiyat: {transaction.price}")
