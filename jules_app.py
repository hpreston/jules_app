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
    sensor_type = request.args.get('sensortype')
    port_types = request.args.getlist('porttype')
    states = request.args.getlist('state')
    ports = zip(port_types, states)

    try:
        s = Sensor(mac, sensor_ip, sensor_type, port_types, states, ports)

        response_text = str(s.sensor_id) + "?"
        for i, port in enumerate(s.desired_states()):
            response_text += str(port[0]) + "=" + str(port[1])
            if i < len(s.ports) - 1:
                response_text += "&"

        response_text += "\n"
        #print response_text

        #resp = make_response(str(s.sensor_id) + '\n')
        resp = make_response(response_text)
        return resp
    except:
        resp = make_response("Error")
        return resp

# Sensor Register Function
@app.route(apiv0 + '/sensor/<mac>/register-dev')
def sensor_register_dev(mac):
    '''
    Sensors send a registration request at startup and periodic hellos
    Registration includes the mac for id as well as ip and the states for the ports
    Returns the sensor_id from the database for reference
    Returns the desired states for all the ports
    '''
    sensor_ip = request.args.get('ip')
    sensor_type = request.args.get('sensortype')
    port_types = request.args.getlist('porttype')
    states = request.args.getlist('state')
    ports = zip(port_types, states)

    try:
        s = Sensor(mac, sensor_ip, sensor_type, port_types, states, ports)

        response_text = str(s.sensor_id) + "?"
        for i, port in enumerate(s.desired_states()):
            response_text += str(port[0]) + "=" + str(port[1])
            if i < len(s.ports) - 1:
                response_text += "&"

        response_text += "\n"
        #print response_text

        #resp = make_response(str(s.sensor_id) + '\n')
        resp = make_response(response_text)
        return resp
    except:
        resp = make_response("Error")
        return resp

# Client functions here
# todo - build inventory api call 1st

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

