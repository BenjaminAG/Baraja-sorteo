import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('db/baraja.db')
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS cartas;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    rol TEXT NOT NULL
);

CREATE TABLE cartas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carta TEXT NOT NULL UNIQUE,
    nombre TEXT,
    telefono TEXT
);
""")

palos = ['oros', 'copas', 'espadas', 'bastos']
numeros = [1,2,3,4,5,6,7,10,11,12]

for palo in palos:
    for numero in numeros:
        carta = f"{numero} de {palo}"
        cursor.execute("INSERT INTO cartas (carta) VALUES (?)", (carta,))

hash_admin = generate_password_hash("admin123")

cursor.execute(
    "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
    ('admin', hash_admin, 'admin')
)

conn.commit()
conn.close()

print("Base de datos creada correctamente con usuario admin.")
