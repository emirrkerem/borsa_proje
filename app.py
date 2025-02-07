from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import yfinance as yf
db = SQLAlchemy()


app = Flask(__name__)

# 📌 Veritabanı Bağlantısı
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'borsa.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 📌 Hisse Senetleri Tablosu
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=True)
    total_value = db.Column(db.Float, nullable=True)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    sell_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Stock {self.symbol}>'

#trade sayfası kaybolmasın diye 

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # "Alış" veya "Satış"
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Trade {self.symbol} {self.action} {self.quantity}>"
         

# 📌 İşlem Geçmişi Tablosu
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'buy' veya 'sell'

# 📌 Döviz Kuru Tablosu
class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usd_to_try = db.Column(db.Float, nullable=False)

# 📌 Ana Sayfa
@app.route('/')
def index():
    stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)

# 📌 Sayfa Yönlendirmeleri
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/trade')
def trade():
    return render_template('trade.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/hedef-getirin')
def hedef_getirin():
    return render_template('hedef_getirin.html')

@app.route('/performance-reports')
def performance_reports():
    return render_template('performance_reports.html')

# 📌 API - İşlem Geçmişini Listeleme
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    transaction_list = [
        {
            "stock_symbol": t.stock_symbol,
            "quantity": t.quantity,
            "price": t.price,
            "transaction_type": t.transaction_type
        }
        for t in transactions
    ]
    return jsonify(transaction_list)

#trade ekledik
@app.route("/add_trade", methods=["POST"])
def add_trade():
    data = request.json
    new_trade = Trade(
        symbol=data["symbol"],
        action=data["action"],
        quantity=data["quantity"],
        price=data["price"]
    )
    db.session.add(new_trade)
    db.session.commit()
    return jsonify({"message": "Trade başarıyla eklendi!"}), 201

@app.route('/trades', methods=['GET'])
def get_trades():
    trades = Trade.query.all()
    trade_list = [
        {
            "symbol": trade.symbol,
            "action": trade.action,
            "quantity": trade.quantity,
            "price": trade.price,
            "date": trade.date.strftime("%Y-%m-%d %H:%M:%S")
        }
        for trade in trades
    ]
    return jsonify(trade_list)


# 📌 API - Yeni İşlem Ekleme
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    stock_symbol = request.form['stock_symbol']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    transaction_type = request.form['transaction_type']

    new_transaction = Transaction(
        stock_symbol=stock_symbol,
        quantity=quantity,
        price=price,
        transaction_type=transaction_type
    )
    db.session.add(new_transaction)
    db.session.commit()
    
    return "✅ İşlem başarıyla eklendi!", 201

# 📌 API - Hisse Senetlerini JSON Formatında Listeleme
@app.route('/api/stocks')
def api_get_stocks():
    stocks = Stock.query.all()
    stocks_json = [
        {
            "id": stock.id,
            "symbol": stock.symbol,
            "quantity": stock.quantity,
            "purchase_price": stock.purchase_price,
            "current_price": stock.current_price,
            "purchase_date": stock.purchase_date.strftime('%Y-%m-%d %H:%M:%S'),
            "sell_date": stock.sell_date.strftime('%Y-%m-%d %H:%M:%S') if stock.sell_date else None
        }
        for stock in stocks
    ]
    return jsonify(stocks_json)

# 📌 API - İşlem Güncelleme (Update)
@app.route('/edit_transaction/<int:id>', methods=['POST'])
def edit_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return "❌ İşlem bulunamadı!", 404

    transaction.stock_symbol = request.form['stock_symbol']
    transaction.quantity = int(request.form['quantity'])
    transaction.price = float(request.form['price'])
    transaction.transaction_type = request.form['transaction_type']
    
    db.session.commit()
    return "✅ İşlem başarıyla güncellendi!", 200

# 📌 API - Hisse Silme
@app.route('/delete_stock/<int:stock_id>', methods=['POST'])
def delete_stock(stock_id):
    stock = Stock.query.get(stock_id)
    if stock:
        db.session.delete(stock)
        db.session.commit()
    
    return redirect(url_for('index'))

# 📌 API - Hisse Satış Tarihini Güncelleme
@app.route('/sell_stock/<int:id>', methods=['POST'])
def sell_stock(id):
    stock = Stock.query.get(id)
    if not stock:
        return "❌ Hisse bulunamadı!", 404

    stock.sell_date = datetime.utcnow()
    db.session.commit()

    return "✅ Hisse satıldı ve satış tarihi kaydedildi!", 200

# 📌 API - Canlı Hisse Fiyatlarını Getirme (Yahoo Finance)
@app.route("/get_stock_price", methods=["GET"])
def get_stock_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Hisse sembolü gerekli!"}), 400

    try:
        stock = yf.Ticker(symbol)
        current_price = stock.history(period="1d")["Close"].iloc[-1]
        return jsonify({"symbol": symbol, "price": float(current_price)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 Test için Veritabanı Kontrolü
@app.route('/test_db')
def test_db():
    stocks = Stock.query.all()
    if not stocks:
        return "⚠️ Veritabanında hiç hisse senedi yok!"
    
    response = "<h2>📊 Veritabanındaki Hisse Senetleri:</h2><ul>"
    for stock in stocks:
        response += f"<li>ID: {stock.id}, Sembol: {stock.symbol}, Miktar: {stock.quantity}, Alış Fiyatı: {stock.purchase_price}, Güncel Fiyat: {stock.current_price}</li>"
    response += "</ul>"

    return response

# 📌 Veritabanını oluştur ve uygulamayı çalıştır
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
