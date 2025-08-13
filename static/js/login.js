document.getElementById("btnLogin").addEventListener("click", function () {
    const email = document.getElementById("emailLogin").value.trim();
    const password = document.getElementById("passwordLogin").value.trim();
    const mensaje = document.getElementById("messageLogin");
    mensaje.innerText = "";

    if (!email || !password) {
        mensaje.innerText = "Correo y contraseña obligatorios.";
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(result => {
        if (result.ok) {
            window.location.href = "/bienvenida";
        } else {
            mensaje.innerText = result.data.message || "Error de inicio de sesión.";
        }
    })
    .catch(() => {
        mensaje.innerText = "Error en la conexión con el servidor.";
    });
});
