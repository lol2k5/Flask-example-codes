const escapeHtml = str => {
    if (str == null)
        return "";
    return String(str)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
};

const initialization = async () => {
    let resp = await fetch("http://192.168.2.3/notes");
    let data = await resp.json();

    let table_body = document.getElementById("notes_body");
    data.forEach(note => {
        let row = `
        <tr>
            <td>${escapeHtml(note.id)}</td>
            <td>${escapeHtml(note.info)}</td>
            <td>${escapeHtml(note.date)}</td>
            <td><button class="del-btn" data-id="${escapeHtml(note.id)}">Delete</button></td>
        </tr>
        `;
        table_body.innerHTML += row;
    });


    document.querySelectorAll(".del-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            let id = button.getAttribute("data-id");
            await fetch(`http://192.168.2.3/notes/${encodeURIComponent(id)}`, {
                method: "DELETE"
            });
            button.closest("tr").remove();
        });
    });
};

initialization();