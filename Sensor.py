'''
    The class module for a Sensor Object
'''

__author__ = 'hapresto'

from collections import namedtuple
from time import time, mktime
from db_utils import mysqldb
from datetime import datetime, timedelta
import json

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0, 0)

db = mysqldb()

class Sensor(object):
    '''
    Object representing a single sensor
    '''
    sensor_mac = ''
    sensor_ip = ''

    def __init__(self, mac, ip, states):
        self.sensor_mac = mac
        self.sensor_ip = ip
        self.states = states
        # Get the ID for the sensor to determine if it already exists in the DB
        # If its a new sensor, register it, otherwise refresh it
        self._get_id()
        if (not self.sensor_id):
            self.register()
        else:
            self.refresh()

    def register(self):
        'Register the sensor to the database'
        if (self.sensor_id): return 'Already registered.'
        n = db.sensor_register(self.sensor_mac, self.sensor_ip)
        self._get_id()
        self._port_register()
        return str(n)

    def refresh(self):
        'refresh an exiting sensor'
        u = db.sensor_refresh(self.sensor_mac, self.sensor_ip, self.sensor_id)
        self._port_refresh()
        return str(u)

    def _port_register(self):
        'Register the ports for this sensor'
        for i, p in enumerate(self.states):
            db.port_register(self.sensor_id, i, p)

    def _port_refresh(self):
        'refresh the state for ports for this sensor'
        for i, p in enumerate(self.states):
            db.port_refresh(self.sensor_id, i, p)

    def _get_id(self):
        'Query the database for the sensor_id for the provided mac address'
        s = db.get_sensor(self.sensor_mac)
        if (len(s) > 0):
            self.sensor_id = s[0][0]
            return self.sensor_id
        else:
            self.sensor_id = False
            return 0

