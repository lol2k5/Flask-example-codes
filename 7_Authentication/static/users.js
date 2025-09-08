const set_up = () => {
    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", async () => {
            let id = button.getAttribute("data-id");
            await fetch(`http://127.0.0.1:5000/users/${id}`, {
                method: "DELETE"
            });
            button.closest("tr").remove();
        });
    });
};

set_up();