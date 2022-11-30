from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from service import getCategories, getTruck, drawInterventionBaseCard
#from flask_script import Manager


import random
from lxml import etree

import model

app = Flask(__name__)
CORS(app)


socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/truck/<name>.svg')
def getTruckImage(name):
    #it's a call to the svg file
    #we need to return it without head and body
    #the svg file is in ressources/truck
    #the name is the name of the truck
    #the file is a svg file
    svg = etree.parse(f'resources/truck/{name}.svg')
    return etree.tostring(svg.getroot(), pretty_print=True, encoding='unicode')

#manager = Manager(app)

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


#manager.run()

if __name__ == '__main__':
    from waitress import serve
    #serve(app, host='0.0.0.0', port=5000)
    socketio.run(app, host= '0.0.0.0', port=5000, debug=True)