from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from service import getCategories, getTruck, drawInterventionBaseCard

import random

import model

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)


@socketio.on('connect')
def test_connect():
    print('Connected')

@socketio.on('getOptions')
def getOptions():
    print('getCategories')
    categories = getCategories()
    nbCrewMan = random.randrange(5, 10)
    nbChef = random.randrange(2, 5)
    trucks = [getTruck('VSAV'),getTruck('VL'),getTruck('FPT')]
    print('send Options')
    emit('Options',{
        'categories' :categories,
        'nbCrewMan' : nbCrewMan,
        'nbChef' : nbChef,
        'trucks' : trucks
        })

@socketio.on('drawInterventionBaseCard')
def handle_drawInterventionBaseCard():
    print('drawCard')
    card = drawInterventionBaseCard()
    print('send drawCard')
    emit('InterventionCard', card)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

#model.truck.createTrucks()

socketio.run(app, host= '0.0.0.0', port=5000, debug=True)

