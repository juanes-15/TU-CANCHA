from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, g
from flask_mail import Mail, Message
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = 'database.db'

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu.cancha.bog@gmail.com'
app.config['MAIL_PASSWORD'] = 'ktsa ucci cjrb dhob'
app.config['MAIL_DEFAULT_SENDER'] = ('Tu Cancha', 'tu.cancha.bog@gmail.com')

mail = Mail(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(stored_password_hash, provided_password):
    return stored_password_hash == hashlib.sha256(provided_password.encode('utf-8')).hexdigest()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('bienvenida'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Correo y contraseña son obligatorios.'}), 400

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({'message': 'El correo electrónico ya está registrado.'}), 409

        hashed_pw = hash_password(password)
        try:
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed_pw))
            db.commit()
            return jsonify({'message': 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.'}), 201
        except sqlite3.Error as e:
            db.rollback()
            return jsonify({'message': f'Error en la base de datos: {e}'}), 500

    return render_template('1_registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Correo y contraseña son obligatorios.'}), 400

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return jsonify({'message': 'Inicio de sesión exitoso.'}), 200
        else:
            return jsonify({'message': 'Correo o contraseña incorrectos.'}), 401

    return render_template('2_login.html')

@app.route('/bienvenida')
def bienvenida():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('login_page'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, email, phone, location, reservation_time, reservation_date
        FROM reservations
        WHERE user_id = ?
        ORDER BY reservation_date, reservation_time
    """, (session['user_id'],))
    reservas = cursor.fetchall()

    return render_template('3_bienvenida.html', reservas=reservas)

@app.route('/reservar_page')
def reservar_page_get():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para hacer una reserva.", "warning")
        return redirect(url_for('login_page'))
    return render_template('4_reservar.html')

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    if 'user_id' not in session:
        return jsonify({'message': 'No autorizado. Debes iniciar sesión.'}), 401

    try:
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')
        ubicacion = data.get('ubicacion')
        hora = data.get('hora')
        fecha = data.get('fecha')
        user_id = session['user_id']

        if not all([nombre, email, ubicacion, hora, fecha]):
            return jsonify({'message': 'Todos los campos (excepto teléfono) son obligatorios.'}), 400

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO reservations (user_id, name, email, phone, location, reservation_time, reservation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, nombre, email, telefono, ubicacion, hora, fecha))
        db.commit()

        msg = Message(
            subject='Confirmación de Reserva - Tu Cancha',
            recipients=[email],
            body=f"""Hola {nombre},

Tu reserva ha sido confirmada ✅

📍 Ubicación: {ubicacion}
📅 Fecha: {fecha}
⏰ Hora: {hora}

Gracias por reservar con Tu Cancha ⚽
""")
        mail.send(msg)

        return jsonify({'message': 'Reserva realizada con éxito. Se envió confirmación por correo electrónico.'}), 201

    except sqlite3.Error as e:
        db.rollback()
        return jsonify({'message': f'Error al guardar la reserva: {e}'}), 500
    except Exception as e:
        return jsonify({'message': f'Error inesperado: {str(e)}'}), 500

@app.route('/eliminar_reserva/<int:reserva_id>', methods=['POST'])
def eliminar_reserva(reserva_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM reservations WHERE id = ? AND user_id = ?", (reserva_id, session['user_id']))
    db.commit()
    return redirect(url_for('bienvenida'))

@app.route('/editar_reserva/<int:reserva_id>', methods=['GET'])
def editar_reserva(reserva_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reservations WHERE id = ? AND user_id = ?", (reserva_id, session['user_id']))
    reserva = cursor.fetchone()
    if not reserva:
        return redirect(url_for('bienvenida'))

    return render_template('editar_reserva.html', reserva=reserva)

@app.route('/actualizar_reserva/<int:reserva_id>', methods=['POST'])
def actualizar_reserva(reserva_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    data = request.form
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    ubicacion = data.get('ubicacion')
    hora = data.get('hora')
    fecha = data.get('fecha')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE reservations
        SET name = ?, email = ?, phone = ?, location = ?, reservation_time = ?, reservation_date = ?
        WHERE id = ? AND user_id = ?
    """, (nombre, email, telefono, ubicacion, hora, fecha, reserva_id, session['user_id']))
    db.commit()
    return redirect(url_for('bienvenida'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        with open('schema.sql', 'w') as f:
            f.write("""
            DROP TABLE IF EXISTS users;
            DROP TABLE IF EXISTS reservations;

            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                location TEXT NOT NULL,
                reservation_time TEXT NOT NULL,
                reservation_date TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """)
        init_db()
        print("Base de datos inicializada.")

    app.run(debug=True)
