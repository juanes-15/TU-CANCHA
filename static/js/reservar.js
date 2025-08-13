document.addEventListener('DOMContentLoaded', function () {
  const boton = document.getElementById('btnEnviarReserva');
  if (!boton) return;

  boton.addEventListener('click', async function () {
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('emailReserva').value;
    const telefono = document.getElementById('telefono').value;
    const ubicacion = document.getElementById('ubicacion').value;
    const hora = document.getElementById('hora').value;
    const fecha = document.getElementById('fecha').value;
    const messageDiv = document.getElementById('messageReserva');
    messageDiv.textContent = '';

    if (!nombre || !email || !ubicacion || !hora || !fecha) {
      messageDiv.style.color = 'red';
      messageDiv.textContent = 'Todos los campos son obligatorios (excepto teléfono).';
      return;
    }

    try {
      const response = await fetch('/submit_reservation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre: nombre,
          email: email,
          telefono: telefono,
          ubicacion: ubicacion,
          hora: hora,
          fecha: fecha
        }),
      });

      const data = await response.json();
      if (response.ok) {
        window.location.href = '/bienvenida'; // Redirige si se guarda bien
      } else {
        messageDiv.style.color = 'red';
        messageDiv.textContent = data.message || 'Error al enviar la reserva.';
      }
    } catch (error) {
      messageDiv.style.color = 'red';
      messageDiv.textContent = 'Error de conexión. Inténtalo de nuevo.';
      console.error('Error:', error);
    }
  });
});
