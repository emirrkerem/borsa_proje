from app import db, Stock, Transaction, app

with app.app_context():
    # Örnek hisse ekleyelim
    new_stock = Stock(symbol="AAPL", quantity=10, purchase_price=150, current_price=155)
    db.session.add(new_stock)

    new_stock2 = Stock(symbol="TSLA", quantity=5, purchase_price=200, current_price=210)
    db.session.add(new_stock2)

    # Örnek işlem ekleyelim
    new_transaction = Transaction(stock_symbol="AAPL", quantity=10, price=150, transaction_type="buy")
    db.session.add(new_transaction)

    # Yeni işlemler ekleyelim
    new_transaction1 = Transaction(stock_symbol="TSLA", quantity=5, price=210, transaction_type="sell")
    db.session.add(new_transaction1)

    new_transaction2 = Transaction(stock_symbol="GOOGL", quantity=8, price=2900, transaction_type="buy")
    db.session.add(new_transaction2)

    

print("📊 Veriler başarıyla eklendi! 🚀")
