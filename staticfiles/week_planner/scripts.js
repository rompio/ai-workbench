function editMeal(element) {
    let newMeal = prompt("Gib eine Mahlzeit ein:", element.innerText);
    if (newMeal !== null && newMeal.trim() !== "") {
        element.innerText = newMeal;
    }



}
// Modal beim Klicken auf einen Block öffnen
function editMeal(block) {
    // Hier speichern wir, welcher Block geklickt wurde
    const mealTime = block.innerText.trim(); // Morgens, Mittags oder Abends
    document.getElementById('mealTitle').value = ''; // Leeren das Eingabefeld
    document.getElementById('mealDescription').value = ''; // Leeren das Beschreibungfeld

    // Ändern den Modal-Titel je nach dem, welcher Block angeklickt wurde
    document.getElementById('mealModalLabel').innerText = `${mealTime} hinzufügen`;

    // Öffne das Modal
    new bootstrap.Modal(document.getElementById('mealModal')).show();
}

// Speichern des Eintrags (simuliert)
document.getElementById('mealForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Verhindert, dass das Formular standardmäßig abgeschickt wird

    // Hier kannst du die Eingabedaten weiterverarbeiten (z.B. in der Datenbank speichern)
    const mealTitle = document.getElementById('mealTitle').value;
    const mealDescription = document.getElementById('mealDescription').value;

    if (mealTitle && mealDescription) {
        alert(`Mahlzeit: ${mealTitle}\nBeschreibung: ${mealDescription}`);
        // Hier kannst du auch AJAX verwenden, um die Daten zu speichern
        // Danach kannst du das Modal schließen
        bootstrap.Modal.getInstance(document.getElementById('mealModal')).hide();
    } else {
        alert("Bitte alle Felder ausfüllen!");
    }
});
function searchFood() {
    const query = document.getElementById('foodSearch').value;
    if (query) {
        fetch(`/food/search_food/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const foodList = document.getElementById('foodResults');
                foodList.innerHTML = '';
                data.results.forEach(food => {
                    const listItem = document.createElement('li');
                    listItem.classList.add('list-group-item');
                    listItem.textContent = food.name;
                    listItem.onclick = () => selectFood(food.id, food.name);
                    foodList.appendChild(listItem);
                });
            });
    }
}

function selectFood(id, name) {
    document.getElementById('foodSearch').value = name;
    document.getElementById('addFoodButton').onclick = () => addFoodToBlock(id, name);
}

function addFoodToBlock(id, name) {
    const quantity = document.getElementById('foodQuantity').value;
    if (quantity) {
        // Hier kann man die Logik für das Hinzufügen des Lebensmittels zur Mahlzeit einfügen
        alert(`Lebensmittel: ${name}, Menge: ${quantity}g, ID: ${id} hinzugefügt.`);
        $('#foodModal').modal('hide');
    } else {
        alert('Bitte eine Menge eingeben.');
    }
}
