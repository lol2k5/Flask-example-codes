const initialization = async () => {
    document.querySelectorAll(".del-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            let id = button.getAttribute("data-id");
            await fetch(`http://192.168.2.3/notes/${encodeURIComponent(id)}`, {
                method: "DELETE"
            }); // Chỉnh theo địa chỉ ip và cổng
            button.closest("tr").remove();
        });
    });
};

initialization();