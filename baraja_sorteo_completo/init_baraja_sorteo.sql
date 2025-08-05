DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS cartas;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    rol TEXT CHECK(rol IN ('admin', 'usuario')) NOT NULL
);

CREATE TABLE cartas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carta TEXT NOT NULL UNIQUE,
    nombre TEXT,
    telefono TEXT
);

INSERT INTO cartas (carta) VALUES
('1 de oros'), ('2 de oros'), ('3 de oros'), ('4 de oros'), ('5 de oros'), ('6 de oros'), ('7 de oros'), ('10 de oros'), ('11 de oros'), ('12 de oros'),
('1 de copas'), ('2 de copas'), ('3 de copas'), ('4 de copas'), ('5 de copas'), ('6 de copas'), ('7 de copas'), ('10 de copas'), ('11 de copas'), ('12 de copas'),
('1 de espadas'), ('2 de espadas'), ('3 de espadas'), ('4 de espadas'), ('5 de espadas'), ('6 de espadas'), ('7 de espadas'), ('10 de espadas'), ('11 de espadas'), ('12 de espadas'),
('1 de bastos'), ('2 de bastos'), ('3 de bastos'), ('4 de bastos'), ('5 de bastos'), ('6 de bastos'), ('7 de bastos'), ('10 de bastos'), ('11 de bastos'), ('12 de bastos');

-- Hash de 'admin123' con werkzeug
INSERT INTO usuarios (username, password, rol) VALUES
('admin', 'pbkdf2:sha256:600000$dummy$1234567890abcdef', 'admin'),('usuario', '1234', 'usuario');
