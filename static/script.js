document.addEventListener("DOMContentLoaded", function () {
    // 📌 Trade İşlemleri
    const tradeTable = document.querySelector("#tradeTable tbody");
    const addTradeBtn = document.querySelector("#addTrade");

    if (!tradeTable || !addTradeBtn) return;

    // 📌 Hisse sembolü girildiğinde fiyatı otomatik getir
    document.getElementById("symbol").addEventListener("change", function () {
        fetchStockPrice();
    });

    function fetchStockPrice() {
        let symbol = document.getElementById("symbol").value.trim();
        if (!symbol) return;

        fetch(`/api/get_price/${symbol}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById("price").value = "Hata!";
                } else {
                    document.getElementById("price").value = data.price.toFixed(2);
                }
            })
            .catch(error => console.error("Fiyat alınamadı:", error));
    }

    // 📌 Hisseyi ekle
    addTradeBtn.addEventListener("click", function () {
        let symbol = document.getElementById("symbol").value.trim();
        let action = document.getElementById("action").value;
        let quantity = parseFloat(document.getElementById("quantity").value);
        let price = parseFloat(document.getElementById("price").value);
        let date = new Date().toLocaleString();
        
        if (!symbol || isNaN(quantity) || isNaN(price)) {
            alert("Lütfen geçerli değerler girin!");
            return;
        }

    //trade için güncelledik    
    document.getElementById("addTradeButton").addEventListener("click", function () {
        let symbol = document.getElementById("symbol").value;
        let action = document.getElementById("action").value;
        let quantity = document.getElementById("quantity").value;
        let price = document.getElementById("price").value;    
        
            fetch("/add_trade", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ symbol, action, quantity, price })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();  // Sayfayı yenileyerek yeni eklenen hisseleri göster
            });
        });
        

        // 📌 Kâr / Zarar hesapla
        fetch(`/api/get_price/${symbol}`)
            .then(response => response.json())
            .then(data => {
                let currentPrice = parseFloat(data.price);
                let totalCost = (quantity * price).toFixed(2);
                let profitLoss = ((currentPrice - price) * quantity).toFixed(2);
                let profitClass = profitLoss >= 0 ? 'profit' : 'loss';

                // 📌 Yeni satır ekle
                const newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td>${symbol}</td>
                    <td>${action}</td>
                    <td>${quantity}</td>
                    <td>${date}</td>
                    <td>${price.toFixed(2)}</td>
                    <td>${currentPrice.toFixed(2)}</td>
                    <td>${totalCost}</td>
                    <td class="${profitClass}">${profitLoss}</td>
                `;

                tradeTable.appendChild(newRow);

                // 📌 Formu temizle
                resetTradeForm();
            })
            .catch(error => console.error("Fiyat alınamadı:", error));
    });

    function resetTradeForm() {
        document.getElementById("symbol").value = "";
        document.getElementById("quantity").value = "";
        document.getElementById("price").value = "";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("/trades")  // Sayfa açıldığında kayıtlı işlemleri getir
        .then(response => response.json())
        .then(trades => {
            let table = document.getElementById("tradeTableBody");
            table.innerHTML = ""; // Önce tabloyu temizle
            trades.forEach(trade => {
                let row = table.insertRow();
                row.innerHTML = `
                    <td>${trade.symbol}</td>
                    <td>${trade.action}</td>
                    <td>${trade.quantity}</td>
                    <td>${trade.price}</td>
                    <td>${trade.date}</td>
                `;
            });
        });
});

// Yeni hisse eklemek için API çağrısı
document.getElementById("addTradeBtn").addEventListener("click", function () {
    let symbol = document.getElementById("symbol").value;
    let action = document.getElementById("action").value;
    let quantity = document.getElementById("quantity").value;
    let price = document.getElementById("price").value;

    if (!symbol || !quantity || !price) {
        alert("Lütfen tüm alanları doldurun!");
        return;
    }

    fetch("/add_trade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            symbol: symbol,
            action: action,
            quantity: parseInt(quantity),
            price: parseFloat(price)
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload(); // Sayfayı yenileyerek tabloyu güncelle
    });
});
