'''
    This will be the App Server for the Jules System
    This server will take REST API calls from:
        - Sensors
        - Local Gateways
        - Cloud Management
    This server will leverage a DB backend to store persistent data.
'''

__author__ = 'hpreston'

from collections import namedtuple
from flask import Flask, make_response, request, jsonify, url_for
from Sensor import Sensor

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0, 0)

app = Flask(__name__)
apiv0 = '/api/v0'


@app.route('/')
def hello_world():
    return 'Hello World!'

# Sensor Register Function
@app.route(apiv0 + '/sensor/<mac>/register')
def sensor_register(mac):
    '''
    Sensors send a registration request at startup and periodic hellos
    Registration includes the mac for id as well as ip and the states for the ports
    Returns the sensor_id from the database for reference
    '''
    sensor_ip = request.args.get('ip')
    ports = request.args.getlist('port')
    states = request.args.getlist('state')
    print ports

    s = Sensor(mac, sensor_ip, states)

    resp = make_response(str(s.sensor_id))
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

