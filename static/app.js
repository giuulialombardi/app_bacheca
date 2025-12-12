async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.status === 200)
        location.href = "messages.html";
}


async function registerUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/api/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.status === 201)
        location.href = "login.html";
}


async function logout() {
    await fetch("/api/logout", {method: "POST"});
    location.href = "login.html";
}



async function loadTasks() {
    const res = await fetch("/api/tasks");

    if (res.status !== 200) {
        location.href = "login.html";
        return;
    }

    const data = await res.json();
    const list = document.getElementById("taskList");
    list.innerHTML = "";

    const utente=data.current_user;
    print(utente);

    data.items.forEach(t => {
        const li = document.createElement("li");
        //li.className = t.done ? "done" : "";

        // Testo
        const textSpan = document.createElement("span");
        textSpan.textContent = `${t.text} (pubblicato da ${t.author} il ${t.created_at})`;


        // Area icone
        const actions = document.createElement("div");

        // 🗑 icona
        if(t.deletable === "True"){
            const del = document.createElement("button");
            del.className = "icon-btn";
            del.innerHTML = '<i class="fa-solid fa-trash" title="Elimina"></i>';
            del.onclick = () => deleteTask(t.id);
            actions.appendChild(del);
        }

        li.appendChild(textSpan);
        li.appendChild(actions);
        list.appendChild(li);
    });
}

async function addTask() {
    const text = document.getElementById("taskText").value;

    await fetch("/api/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    loadTasks();
}

async function updateTask(id, done) {
    await fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({done})
    });

    loadTasks();
}


async function deleteTask(id) {
    await fetch(`/api/tasks/${id}/delete`, {method: "DELETE"});
    loadTasks();
}

if (location.pathname.endsWith("messages.html"))
    loadTasks();