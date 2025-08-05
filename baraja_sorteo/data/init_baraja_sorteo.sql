
-- Tabla de usuarios
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('admin', 'usuario'))
);

-- Tabla de cartas
CREATE TABLE cartas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL,
    palo TEXT NOT NULL,
    nombre TEXT,
    telefono TEXT,
    vendida INTEGER DEFAULT 0 CHECK(vendida IN (0, 1))
);

-- Inserta usuarios con contraseña ya hasheada (SHA-256)
INSERT INTO usuarios (usuario, contrasena, rol) VALUES
('admin', 'a7c4ee5e4c254ab7a3b24b59b2c7e9a4d4f9f6a7e16c8b314a9a802ad2a78d0d', 'admin'),
('usuario1', '3993ad40628914b3d0b58b1fe94ffbe0d93db36ae94e2edee536914f3c8d4f91', 'usuario');

-- Inserta todas las cartas de la baraja española
INSERT INTO cartas (numero, palo) VALUES
-- Oros
(1, 'oros'), (2, 'oros'), (3, 'oros'), (4, 'oros'), (5, 'oros'), (6, 'oros'), (7, 'oros'), (10, 'oros'), (11, 'oros'), (12, 'oros'),
-- Copas
(1, 'copas'), (2, 'copas'), (3, 'copas'), (4, 'copas'), (5, 'copas'), (6, 'copas'), (7, 'copas'), (10, 'copas'), (11, 'copas'), (12, 'copas'),
-- Espadas
(1, 'espadas'), (2, 'espadas'), (3, 'espadas'), (4, 'espadas'), (5, 'espadas'), (6, 'espadas'), (7, 'espadas'), (10, 'espadas'), (11, 'espadas'), (12, 'espadas'),
-- Bastos
(1, 'bastos'), (2, 'bastos'), (3, 'bastos'), (4, 'bastos'), (5, 'bastos'), (6, 'bastos'), (7, 'bastos'), (10, 'bastos'), (11, 'bastos'), (12, 'bastos');
