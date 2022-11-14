from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
from f_database import InterventionCard
from model import  RelationLevel
from func import getInterventionBaseCard, getNextCard, getInfoBaseCard



app = Flask(__name__)
CORS(app)

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)


@socketio.on('connect')
def test_connect(msg):
    print('Connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on("drawInterventionBaseCard", namespace="/")
def drawInterventionCard():
    print("Drawing intervention card")
    card:InterventionCard = getInterventionBaseCard()
    emit("InterventionCard", json.dumps(card.__dict__), broadcast=True)


@socketio.on("drawNextCard", namespace="/")
def drawNextCard(cardId:int, level:str):
    print("Drawing next card")
    print("card Id :", cardId)
    print("level :", level)
    level:RelationLevel = RelationLevel[level]
    card = getNextCard(cardId, level)
    if card is None:
        print("No card found")
    else:
        print("Card found")
        emit("InfoCard", json.dumps(card.__dict__), broadcast=True)


@socketio.on("drawInfoBaseCard")
def drawInfoCard():
    print("Drawing info base card")
    card = getInfoBaseCard()
    print(card)
    emit("InfoCard", json.dumps(card), broadcast=True)


socketio.run(app, host= '0.0.0.0', port=5000, debug=True)