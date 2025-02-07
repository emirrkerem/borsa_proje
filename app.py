from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Stock
import yfinance as yf
app = Flask(__name__)

# SQLite veritabanı bağlantısını ayarla
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'borsa.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Hisse Senetleri Tablosu
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Otomatik ID
    symbol = db.Column(db.String(10), nullable=False)  # Hisse sembolü (AAPL, TSLA vb.)
    quantity = db.Column(db.Integer, nullable=False)  # Hisse adedi
    purchase_price = db.Column(db.Float, nullable=False)  # Alış fiyatı
    current_price = db.Column(db.Float, nullable=True)  # Güncel fiyat
    total_value = db.Column(db.Float, nullable=True)  # Güncel toplam değer
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Satın alma tarihi
    sell_date = db.Column(db.DateTime, nullable=True)  # Satış tarihi (isteğe bağlı)

    def __repr__(self):
        return f'<Stock {self.symbol}>'
    
@app.route('/')
def home():
    return render_template('stocks.html')

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
    
@app.route('/')
def index():
    stocks = Stock.query.all()  # Veritabanındaki hisse senetlerini çek
    return render_template('stocks.html', stocks=stocks)  # stocks.html şablonunu yükle 

  

# İşlem Geçmişi Tablosu
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'buy' veya 'sell'

# Döviz Kuru Tablosu
class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usd_to_try = db.Column(db.Float, nullable=False)

#transactions ekledik     
@app.route('/transactions', methods=['GET'])
def get_transactions():
    with app.app_context():
        transactions = Transaction.query.all()
        transaction_list = [
            {
                "stock_symbol": transaction.stock_symbol,
                "quantity": transaction.quantity,
                "price": transaction.price,
                "transaction_type": transaction.transaction_type
            }
            for transaction in transactions
        ]
    return jsonify(transaction_list)

# API - Yeni işlem ekleme
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    with app.app_context():
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

# 📌 6️⃣ API ile JSON Formatında Hisse Listesi
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

# İşlem Düzenleme (Update)
@app.route('/edit_transaction/<int:id>', methods=['POST'])
def edit_transaction(id):
    with app.app_context():
        transaction = Transaction.query.get(id)
        if not transaction:
            return "❌ İşlem bulunamadı!", 404

        # Formdan gelen yeni verileri al
        transaction.stock_symbol = request.form['stock_symbol']
        transaction.quantity = int(request.form['quantity'])
        transaction.price = float(request.form['price'])
        transaction.transaction_type = request.form['transaction_type']

        db.session.commit()
    return "✅ İşlem başarıyla güncellendi!", 200


# İşlem Silme (Delete)
@app.route('/delete_stock/<int:stock_id>', methods=['POST'])
def delete_stock(stock_id):
    stock = Stock.query.get(stock_id)
    if stock:
        db.session.delete(stock)
        db.session.commit()
    
    return redirect(url_for('get_stocks'))

# Hisse Senetlerini Listeleme
@app.route('/stocks', methods=['GET'])
def get_stocks():
    with app.app_context():
        stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)

#listeye hisse ekleme
@app.route('/list/<string:list_name>')
def user_list(list_name):
    stocks = Stock.query.filter_by(list_name=list_name).all()
    return render_template("user_list.html", list_name=list_name, stocks=stocks)

@app.route('/ad_stock', methods=['POST'])
def ad_stock():
    data = request.json
    new_stock = Stock(symbol=data['symbol'], list_name=data['list_name'])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({"message": "Hisse eklendi!"})

#Yeni hisse ekleme
@app.route('/add_stock', methods=['POST'])
def add_stock():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    purchase_price = float(request.form['purchase_price'])
    
    new_stock = Stock(symbol=symbol, quantity=quantity, purchase_price=purchase_price, current_price=purchase_price)
    db.session.add(new_stock)
    db.session.commit()

    return redirect(url_for('get_stocks'))

# 📌 4️⃣ Hisse Güncelleme (Fiyat Güncelleme)
@app.route('/update_stock/<int:stock_id>', methods=['POST'])
def update_stock(stock_id):
    stock = Stock.query.get(stock_id)
    if stock:
        stock.current_price = float(request.form['new_price'])
        db.session.commit()
    
    return redirect(url_for('get_stocks'))

#satış tarihi
@app.route('/sell_stock/<int:id>', methods=['POST'])
def sell_stock(id):
    with app.app_context():
        stock = Stock.query.get(id)

        if not stock:
            return "❌ Hisse bulunamadı!", 404

        stock.sell_date = datetime.utcnow()  # Satış tarihini güncelle
        db.session.commit()

    return "✅ Hisse satıldı ve satış tarihi kaydedildi!", 200

# 📌 Hisse fiyatlarını almak için API endpoint
@app.route("/get_stock_price", methods=["GET"])
def get_stock_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Hisse sembolü gerekli!"}), 400

    try:
        stock = yf.Ticker(symbol)
        current_price = stock.history(period="1d")["Close"].iloc[-1]
        return jsonify({"symbol": symbol, "price": current_price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#test için
@app.route('/test_db')
def test_db():
    with app.app_context():
        stocks = Stock.query.all()

        if not stocks:
            return "⚠️ Veritabanında hiç hisse senedi yok!"
        
        response = "<h2>📊 Veritabanındaki Hisse Senetleri:</h2><ul>"
        for stock in stocks:
            response += f"<li>ID: {stock.id}, Sembol: {stock.symbol}, Miktar: {stock.quantity}, Alış Fiyatı: {stock.purchase_price}, Güncel Fiyat: {stock.current_price}</li>"
        response += "</ul>"

        return response

  
# Veritabanını oluştur
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



