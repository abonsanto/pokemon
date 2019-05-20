"""Flask App Project."""

from flask import Flask, jsonify, request
from models.entrenador import Entrenador
from models.pokemon import Pokemon
from models.ligas import Liga

app = Flask(__name__)


@app.route('/createLiga', methods=['POST'])
def createLiga():
    liga = Liga()
    result = liga.createLiga(request.form)
    return jsonify(result)


@app.route('/entrenador', methods=['POST'])
def entrenador():
    entrenador = Entrenador()
    result = entrenador.createEntrenador(request.form)
    return jsonify(result)

@app.route('/battle/<string:fighter>/<string:opponent>', methods=['POST'])
def battle(fighter, opponent):
    entrenador = Entrenador()
    result = entrenador.battle(fighter, opponent)
    return jsonify(result)

@app.route('/train/<string:fighter>', methods=['POST'])
def train(fighter):
    poke = Pokemon()
    result = poke.train(fighter)
    json_data = {"a":result}
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    
