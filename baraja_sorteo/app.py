from flask import Flask, render_template, jsonify, request
import random
import json
import os

app = Flask(__name__)

CARTAS_FILE = 'data/cartas.json'

palos = ["oros", "copas", "espadas", "bastos"]
numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]

def cargar_cartas():
    if not os.path.exists(CARTAS_FILE):
        cartas = [
            {"id": f"{n}-{p}", "numero": n, "palo": p, "vendida": False, "nombre": "", "telefono": ""}
            for p in palos for n in numeros
        ]
        guardar_cartas(cartas)
    else:
        with open(CARTAS_FILE, 'r') as f:
            cartas = json.load(f)
    return cartas

def guardar_cartas(cartas):
    with open(CARTAS_FILE, 'w') as f:
        json.dump(cartas, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartas')
def obtener_cartas():
    return jsonify(cargar_cartas())

@app.route('/seleccionar_azar', methods=['POST'])
def seleccionar_azar():
    cartas = cargar_cartas()
    disponibles = [c for c in cartas if not c["vendida"]]
    if not disponibles:
        return jsonify({"error": "No hay cartas disponibles"}), 400
    carta = random.choice(disponibles)
    return jsonify(carta)

@app.route('/seleccionar_manual', methods=['POST'])
def seleccionar_manual():
    carta_id = request.json.get("id")
    cartas = cargar_cartas()
    for carta in cartas:
        if carta["id"] == carta_id and not carta["vendida"]:
            return jsonify(carta)
    return jsonify({"error": "Carta no disponible"}), 400

@app.route('/vender_carta', methods=['POST'])
def vender_carta():
    data = request.json
    cartas = cargar_cartas()
    for carta in cartas:
        if carta["id"] == data["id"]:
            carta["vendida"] = True
            carta["nombre"] = data.get("nombre", "")
            carta["telefono"] = data.get("telefono", "")
            guardar_cartas(cartas)
            return jsonify({"success": True})
    return jsonify({"error": "Carta no encontrada"}), 400

if __name__ == '__main__':
    app.run(debug=True)