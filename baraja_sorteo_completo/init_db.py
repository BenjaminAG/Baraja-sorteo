import sqlite3
import os

# Crear carpeta si no existe
os.makedirs("db", exist_ok=True)

# Conexión a la base de datos
conn = sqlite3.connect("db/baraja.db")
cursor = conn.cursor()

# Crear tablas
cursor.executescript("""
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS cartas;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,  -- Se guarda en texto plano (no recomendado para producción)
    rol TEXT NOT NULL
);

CREATE TABLE cartas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carta TEXT NOT NULL UNIQUE,
    nombre TEXT,
    telefono TEXT
);
""")

# Insertar cartas (sin 8 ni 9)
palos = ['oros', 'copas', 'espadas', 'bastos']
numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]

for palo in palos:
    for numero in numeros:
        carta = f"{numero} de {palo}"
        cursor.execute("INSERT INTO cartas (carta) VALUES (?)", (carta,))

# Insertar usuario admin con contraseña en texto plano
cursor.execute(
    "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
    ("admin", "admin123", "admin")
)

conn.commit()
conn.close()

print("Base de datos creada con usuario admin (sin hash en contraseña).")
