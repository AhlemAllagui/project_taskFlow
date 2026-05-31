// URL de ton backend Flask
const API_URL = "http://127.0.0.1:5000/tasks";

// Charger les tâches
async function loadTasks() {
    const res = await fetch(API_URL);
    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        li.textContent = task.title + (task.done ? " ✅" : " ❌");

        // bouton toggle done
        const btnDone = document.createElement("button");
        btnDone.textContent = "Toggle";
        btnDone.onclick = () => toggleTask(task.id);

        // bouton delete
        const btnDelete = document.createElement("button");
        btnDelete.textContent = "Delete";
        btnDelete.onclick = () => deleteTask(task.id);

        li.appendChild(btnDone);
        li.appendChild(btnDelete);

        list.appendChild(li);
    });
}

// Ajouter une tâche
async function addTask() {
    const input = document.getElementById("taskInput");

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: input.value
        })
    });

    input.value = "";
    loadTasks();
}

// Toggle done / not done
async function toggleTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "PUT"
    });

    loadTasks();
}

// Supprimer tâche
async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}

// charger au démarrage
loadTasks();