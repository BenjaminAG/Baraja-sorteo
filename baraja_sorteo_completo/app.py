from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_session'
DATABASE = 'db/baraja.db'

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

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['rol'] = user['rol']
            return redirect(url_for(user['rol']))
        else:
            error = 'Credenciales incorrectas'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    if session.get('rol') != 'usuario':
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        carta_id = request.form['carta_id']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        db.execute("UPDATE cartas SET nombre = ?, telefono = ? WHERE id = ? AND nombre IS NULL", (nombre, telefono, carta_id))
        db.commit()
        return redirect(url_for('usuario'))
    cartas = db.execute("SELECT * FROM cartas").fetchall()
    return render_template('usuario.html', cartas=cartas)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('rol') != 'admin':
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        action = request.form['action']
        carta_id = request.form['carta_id']
        if action == 'editar':
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            db.execute("UPDATE cartas SET nombre = ?, telefono = ? WHERE id = ?", (nombre, telefono, carta_id))
        elif action == 'eliminar':
            db.execute("UPDATE cartas SET nombre = NULL, telefono = NULL WHERE id = ?", (carta_id,))
        db.commit()
        return redirect(url_for('admin'))
    cartas = db.execute("SELECT * FROM cartas").fetchall()
    return render_template('admin.html', cartas=cartas)

# 🔐 Crear usuario admin automáticamente si no existe
def crear_usuario_admin():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username = ?", ('admin',))
    if c.fetchone() is None:
        hash_pass = generate_password_hash("admin123")
        c.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                  ('admin', hash_pass, 'admin'))
        conn.commit()
        print("✅ Usuario admin creado: admin / admin123")
    else:
        print("ℹ️ Usuario admin ya existe.")
    conn.close()

if __name__ == '__main__':
    crear_usuario_admin()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=True)
