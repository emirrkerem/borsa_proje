document.addEventListener("DOMContentLoaded", function () {
    const addListBtn = document.getElementById("addList");
    const modal = document.getElementById("listModal");
    const closeModal = document.querySelector(".close");
    const saveListBtn = document.getElementById("saveList");
    const listNameInput = document.getElementById("listName");
    const userLists = document.getElementById("userLists");

    // Modal açma
    addListBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    // Modal kapatma
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Listeyi kaydetme
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
});

document.addEventListener("DOMContentLoaded", function () {
    const tradeTable = document.querySelector("#tradeTable tbody");
    const addTradeBtn = document.querySelector("#addTrade");

    addTradeBtn.addEventListener("click", function () {
        const symbol = document.querySelector("#symbol").value.trim();
        const action = document.querySelector("#action").value;
        const quantity = parseFloat(document.querySelector("#quantity").value);
        const price = parseFloat(document.querySelector("#price").value);
        const date = new Date().toLocaleString(); // Güncel tarih al

        if (symbol === "" || isNaN(quantity) || isNaN(price)) {
            alert("Lütfen geçerli değerler girin.");
            return;
        }

        // Anlık fiyatı API'den çekeceğiz (şimdilik manuel alıyoruz)
        let currentPrice = price;  // Şu an için giriş fiyatını kullanıyoruz

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
            <td>${price.toFixed(2)}</td>
            <td>${totalCost.toFixed(2)}</td>
            <td>${currentPrice.toFixed(2)}</td>
            <td class="${profitLoss >= 0 ? 'profit' : 'loss'}">${profitLoss.toFixed(2)}</td>
        `;
        
        tradeTable.appendChild(newRow);

        // Formu temizle
        document.querySelector("#symbol").value = "";
        document.querySelector("#quantity").value = "";
        document.querySelector("#price").value = ""; 
    });
});
