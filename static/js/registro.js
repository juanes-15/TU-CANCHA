document.getElementById("btnRegistrarse").addEventListener("click", function () {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirm = document.getElementById("confirm_password").value.trim();
    const mensaje = document.getElementById("message");
    mensaje.innerText = "";

    if (!email || !password || !confirm) {
        mensaje.innerText = "Todos los campos son obligatorios.";
        return;
    }

    if (password !== confirm) {
        mensaje.innerText = "Las contraseñas no coinciden.";
        return;
    }

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(result => {
        if (result.ok) {
            window.location.href = "/login";
        } else {
            mensaje.innerText = result.data.message || "Error al registrar.";
        }
    })
    .catch(() => {
        mensaje.innerText = "Error en la conexión con el servidor.";
    });
});
