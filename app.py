from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from service import getCategories, getTruck, drawInterventionBaseCard, getListOfTruckFile, drawNextCard
#from flask_script import Manager


import random
from lxml import etree

import model

app = Flask(__name__, static_url_path="/static")
CORS(app)


socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/truck/<name>.svg')
def getTruckImage(name):
    print(getListOfTruckFile())
    return app.send_static_file(f'truck/{name}.svg') if name in getListOfTruckFile() else app.send_static_file('truck/None.svg')

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
def handle_drawInterventionBaseCard(blackList):
    print('drawCard')
    card = drawInterventionBaseCard(blackList)
    if card:
        print('send InterventionBaseCard')
        emit('InterventionCard', card)

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


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

#model.truck.createTrucks()


#manager.run()

if __name__ == '__main__':
    from waitress import serve
    #serve(app, host='0.0.0.0', port=5000)
    socketio.run(app, host= '0.0.0.0', port=5000, debug=True)