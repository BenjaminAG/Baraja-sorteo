from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cartas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELO DE CARTA
class Carta(db.Model):
    id = db.Column(db.String, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    palo = db.Column(db.String, nullable=False)
    vendida = db.Column(db.Boolean, default=False)
    nombre = db.Column(db.String, default="")
    telefono = db.Column(db.String, default="")

# 👇 Este bloque se ejecuta directamente al arrancar la app
def crear_tabla_y_cartas():
    with app.app_context():
        db.create_all()
        if Carta.query.count() == 0:
            palos = ["oros", "copas", "espadas", "bastos"]
            numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
            for palo in palos:
                for numero in numeros:
                    id_carta = f"{numero}-{palo}"
                    nueva = Carta(id=id_carta, numero=numero, palo=palo)
                    db.session.add(nueva)
            db.session.commit()

# RUTAS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartas')
def obtener_cartas():
    cartas = Carta.query.all()
    return jsonify([
        {
            "id": c.id,
            "numero": c.numero,
            "palo": c.palo,
            "vendida": c.vendida,
            "nombre": c.nombre,
            "telefono": c.telefono
        } for c in cartas
    ])

@app.route('/seleccionar_azar', methods=['POST'])
def seleccionar_azar():
    carta = Carta.query.filter_by(vendida=False).order_by(db.func.random()).first()
    if not carta:
        return jsonify({"error": "No hay cartas disponibles"}), 400
    return jsonify({
        "id": carta.id,
        "numero": carta.numero,
        "palo": carta.palo,
        "vendida": carta.vendida
    })

@app.route('/seleccionar_manual', methods=['POST'])
def seleccionar_manual():
    data = request.get_json()
    carta = Carta.query.get(data['id'])
    if carta and not carta.vendida:
        return jsonify({
            "id": carta.id,
            "numero": carta.numero,
            "palo": carta.palo,
            "vendida": carta.vendida
        })
    return jsonify({"error": "Carta no disponible"}), 400

@app.route('/vender_carta', methods=['POST'])
def vender_carta():
    data = request.get_json()
    carta = Carta.query.get(data['id'])
    if carta:
        carta.vendida = True
        carta.nombre = data.get('nombre', '')
        carta.telefono = data.get('telefono', '')
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Carta no encontrada"}), 400

if __name__ == '__main__':
    crear_tabla_y_cartas()  # 🔥 Ejecutamos esto al arranque
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
