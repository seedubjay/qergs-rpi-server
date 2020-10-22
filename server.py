from pyrow import pyrow
from pyrow.ergmanager import ErgManager

from flask import Flask, json, request
from flask_cors import CORS, cross_origin

from datetime import datetime, time, timedelta, date
import random
import sys

data = {}
ergman = None

port = 5353
if len(sys.argv) > 1: port = int(sys.argv[1])

def add_cb(erg):
    pass

def change_cb(erg):
    global data
    description = erg._pyerg.get_erg()
    data = {
        "id": description["serial"],
        "status": description["status"],
        "time": erg.data["time"],
        "distance": erg.data["distance"],
        "interval_count": erg.data["intcount"],
        "workout_state": erg.data["state"],
        "pace": erg.data["pace"],
        "rate": erg.data["spm"]
    }

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/', methods=['GET'])
@cross_origin()
def get_state():
    global data
    return json.dumps(data)

@api.route('/workout', methods=['POST'])
@cross_origin()
def set_workout():
    if ergman is not None: ergman.set_workout(**request.form)
    return ('',204)

if __name__ == '__main__':
    ergman = ErgManager(pyrow, add_callback=add_cb, update_callback=change_cb)
    api.run(host='0.0.0.0', port=port)
