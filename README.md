# 🏆 TU CANCHA

**TU CANCHA** es una plataforma web que permite a los usuarios **reservar canchas de fútbol** de forma fácil, rápida y sin intermediarios.  
Su objetivo es **promover el deporte comunitario** y facilitar la **gestión de instalaciones deportivas**, apoyándose en una arquitectura escalable y un modelo ágil de desarrollo.

---

## ✨ Características principales

- 📝 **Registro** e **inicio de sesión** de usuarios.
- 📅 **Consulta de disponibilidad** de canchas.
- 📌 **Gestión de reservas** y edición de reservas existentes.
- 🛠️ **Administración** de usuarios y canchas.
- 📱 Interfaz **adaptada a móviles y escritorio**.
- 🔒 **Seguridad y facilidad de uso** con experiencia intuitiva.

---

## 📂 Estructura del proyecto
```
static/ # Archivos estáticos
├── img/ # Imágenes utilizadas en la plataforma
│ ├── hayuelos.png
│ ├── modelia.png
│ ├── parque el ruby.png
│ ├── SALITRE.png
│ ├── villemar.png
│ └── logo.png
├── js/ # Funcionalidades en JavaScript
│ ├── login.js # Lógica de inicio de sesión
│ ├── registro.js # Lógica de registro de usuarios
│ └── reservar.js # Lógica de reservas de canchas

templates/ # Plantillas HTML
├── 1_registro.html # Registro de usuarios
├── 2_login.html # Inicio de sesión
├── 3_bienvenida.html # Página de bienvenida
├── 4_reservar.html # Realizar reservas
└── editar_reserva.html # Editar reservas existentes

app.py # Backend principal con Flask
database.db # Base de datos SQLite
schema.sql # Script de creación de la base de datos
```

## ✅ Requisitos previos

- 🐍 [Python 3.x](https://www.python.org/downloads/) instalado.
- 📦 [pip](https://pip.pypa.io/en/stable/) instalado.
- 💡 Recomendado: usar un entorno virtual (`venv`).

---

## 🛠️ Tecnologías usadas

- **Backend:** Python + Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Base de datos:** SQLite
- **Almacenamiento en navegador:** LocalStorage y SessionStorage

---

## 🚀 Ejecución del proyecto

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/juanes-15/TU-CANCHA.git
   cd TU-CANCHA
   ```
3. **Instalar dependencias:**
   ```
   pip install flask
   ```
4. **Ejecutar la aplicación:**
   ```
   python app.py
   ```
5. **Abrir en el navegador:**
   ```
   http://127.0.0.1:5000/
   ```

---

## 📌 Flujo de la aplicación

1. **El usuario se registra en 1_registro.html o inicia sesión en 2_login.html.**

2. **Tras autenticarse, es redirigido a 3_bienvenida.html.**

3. **Desde allí puede:**

-📅 Hacer reservas en 4_reservar.html.

-✏️ Editar reservas existentes en editar_reserva.html.

-🖼️ Las imágenes de las canchas se encuentran en static/img/.

-⚙️ La lógica del frontend está en static/js/.

## 📄 Notas adicionales

-📷 static/img/ contiene imágenes de las canchas disponibles.

-🖥️ static/js/ implementa la lógica del cliente (validaciones, interacciones, etc.).

-📑 templates/ define las vistas HTML siguiendo el flujo: registro → login → bienvenida → reserva.

-🖧 app.py actúa como servidor y maneja rutas y base de datos.

## 📚 Documentación
-📄 Documentación Parte 1

-📄 Documentación Parte 2

**Incluyen:**

-📌 Planificación del proyecto.

-🛠️ Modelado y diseño.

-💻 Desarrollo y pruebas.

-🚀 Visión futura y mejoras.

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas!
Puedes:

-🐛 Reportar errores.

-💡 Sugerir nuevas funcionalidades.

-🔧 Mejorar el código o la documentación.

##📜 Licencia
Este proyecto está bajo la licencia MIT.
Consulta el archivo LICENSE para más detalles.
