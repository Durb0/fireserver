from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from service import getCategories, getTruck, drawInterventionBaseCard, getListOfTruckFile, drawNextCard


import random

# Creation de l'application Flask
app = Flask(__name__, static_url_path="/static")

# Ajout de CORS
CORS(app)

# Creation de l'application SocketIO
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Route principale
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Route pour les images des camions
@app.route('/truck/<name>.svg')
def getTruckImage(name):
    print(getListOfTruckFile())
    return app.send_static_file(f'truck/{name}.svg') if name in getListOfTruckFile() else app.send_static_file('truck/None.svg')

# Scocket sur la connexion
@socketio.on('connect')
def test_connect():
    print('Connected')

# Socket sur la demande des options de partie
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

# Socket sur la demande de tirage d'une carte de base d'intervention
@socketio.on('drawInterventionBaseCard')
def handle_drawInterventionBaseCard(blackList):
    print('drawCard')
    card = drawInterventionBaseCard(blackList)
    if card:
        print('send InterventionBaseCard')
        emit('InterventionCard', card)

# Socket sur la demande de tirage d'une suite de carte d'intervention
@socketio.on('drawNextCard')
def handle_drawNextCard(id:int, level:int):
    print('drawNextCard')
    print(id, level)
    card, type = drawNextCard(id, level)
    if type == 'intervention_cards':
        print('send InterventionCard')
        emit('InterventionCard', card)
    elif type == 'information_cards':
        print('send InformationCard')
        emit('InformationCard', card)
    elif type == 'dilemme_cards':
        print('send DilemmeCard')
        emit('DilemmeCard', card)
    else:
        print('ERROR: type of card not found')

# Socket sur la deconnexion
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host= '0.0.0.0', port=5000, debug=True)