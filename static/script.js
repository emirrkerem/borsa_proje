document.addEventListener("DOMContentLoaded", function () {
    // 📌 My Lists Kısmı
    const addListBtn = document.getElementById("addList");
    const modal = document.getElementById("listModal");
    const closeModal = document.querySelector(".close");
    const saveListBtn = document.getElementById("saveList");
    const listNameInput = document.getElementById("listName");
    const userLists = document.getElementById("userLists");

    if (addListBtn) {
        addListBtn.addEventListener("click", function () {
            modal.style.display = "block";
        });

        closeModal.addEventListener("click", function () {
            modal.style.display = "none";
        });

        saveListBtn.addEventListener("click", function () {
            const listName = listNameInput.value.trim();
            if (listName !== "") {
                const li = document.createElement("li");
                li.innerHTML = `<a href="/list/${listName}">${listName}</a>`;
                userLists.appendChild(li);
                modal.style.display = "none";
                listNameInput.value = "";
            }
        });
    }

    // 📌 Trade İşlemleri
    const tradeTable = document.querySelector("#tradeTable tbody");
    const addTradeBtn = document.querySelector("#addTrade");

    if (!tradeTable || !addTradeBtn) return; // Eğer tradeTable veya buton bulunamazsa kod çalışmaz.

    addTradeBtn.addEventListener("click", function () {
        const symbol = document.querySelector("#symbol").value.trim();
        const action = document.querySelector("#action").value;
        const quantity = parseFloat(document.querySelector("#quantity").value);
        let price = parseFloat(document.querySelector("#price").value);
        const date = new Date().toLocaleString(); // Güncel tarih al

        if (symbol === "" || isNaN(quantity) || isNaN(price)) {
            alert("Lütfen geçerli değerler girin.");
            return;
        }

        // 📌 Canlı fiyat API bağlanana kadar sabit bir değer kullanılacak
        fetch(`/api/get_price/${symbol}`)
            .then(response => response.json())
            .then(data => {
                let currentPrice = parseFloat(data.price);
                let totalCost = (quantity * entryPrice).toFixed(2);
                let profitLoss = ((currentPrice - entryPrice) * quantity).toFixed(2);
                let profitClass = profitLoss >= 0 ? 'profit' : 'loss';

        // Hisse sembolü girildiğinde fiyatı otomatik olarak getir
function fetchStockPrice() {
    let symbol = document.getElementById("stockSymbol").value;
    if (!symbol) return;

    fetch(`/get_stock_price?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("price").value = "Hata!";
            } else {
                document.getElementById("price").value = data.price.toFixed(2);
            }
        })
        .catch(error => console.error("Hata:", error));

// Hisseyi ekle
function addTrade() {
    let symbol = document.getElementById("stockSymbol").value;
    let action = document.getElementById("action").value;
    let quantity = document.getElementById("quantity").value;
    let price = document.getElementById("price").value;
    let date = new Date().toLocaleString();
    let totalCost = (quantity * price).toFixed(2);

    if (!symbol || !quantity || !price) {
        alert("Lütfen tüm alanları doldurun!");
        return;
    }
}
       

        

        // Toplam maliyet hesapla
        const totalCost = quantity * price;

        // Kâr / Zarar hesapla
        let profitLoss = action === "Satış" ? (quantity * (price - currentPrice)) : 0;

        // Yeni satır ekle
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${symbol}</td>
            <td>${action}</td>
            <td>${quantity}</td>
            <td>${date}</td>
            <td>${entryPrice.toFixed(2)}</td>
            <td>${currentPrice.toFixed(2)}</td>
            <td>${price.toFixed(2)}</td>
            <td>${totalCost.toFixed(2)}</td>
            <td>${currentPrice.toFixed(2)}</td>
            <td class="${profitLoss >= 0 ? 'profit' : 'loss'}">${profitLoss.toFixed(2)}</td>
        `;

        tradeTable.appendChild(newRow);

        // Formu temizle
        resetTradeForm();
    });

    function resetTradeForm() {
        document.querySelector("#symbol").value = "";
        document.querySelector("#quantity").value = "";
        document.querySelector("#price").value = "";
    }
});
