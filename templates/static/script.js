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
