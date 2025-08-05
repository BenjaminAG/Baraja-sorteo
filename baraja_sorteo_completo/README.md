# Aplicación Web de Sorteo con Baraja Española

Esta aplicación permite realizar sorteos usando una baraja española de 40 cartas, con control de acceso por roles.

## Tecnologías

- Flask (Python)
- SQLite
- HTML/CSS/JS (Jinja2)
- Render.com (despliegue gratuito)

## Instalación

```bash
git clone https://gitlab.com/usuario/baraja-sorteo.git
cd baraja-sorteo
pip install -r requirements.txt
```

## Inicializar base de datos

```bash
sqlite3 db/baraja.db < init_baraja_sorteo.sql
```

## Ejecutar localmente

```bash
python app.py
```

## Despliegue en Render

- Crear un nuevo servicio web en [Render.com](https://render.com)
- Conectar repositorio GitLab
- Render detectará `requirements.txt` y `render.yaml`
