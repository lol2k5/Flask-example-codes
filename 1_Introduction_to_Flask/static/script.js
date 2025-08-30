function add_func_to_button() {
    // nút ở file index.html
    let button = document.getElementById("alert_button")
    if (button) {
        button.addEventListener("click", () => {
            alert("You clicked me!");
        });
    }

    // nút ở file cookie.html
    button = document.getElementById("get_cookie");
    if (button) {
        button.addEventListener("click", async () => {
            let resp = await fetch("http://127.0.0.1:5000/getcookie");
            let data = await resp.text();
            let html_tag = document.getElementById("show_cookie")
            if (html_tag) {
                html_tag.innerText = data;
            }
        });
    }
}

add_func_to_button();