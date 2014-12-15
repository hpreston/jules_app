'''
    The class module for a Sensor Object
'''

__author__ = 'hapresto'

from collections import namedtuple
from time import time, mktime
from db_utils import mysqldb, jules_data
from datetime import datetime, timedelta
import json

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0, 0)

db = mysqldb()
data = jules_data()

class Sensor(object):
    '''
    Object representing a single sensor
    '''
    sensor_mac = ''
    sensor_ip = ''

    def __init__(self, mac, ip=None, sensor_type=None, port_types=None, states=None, ports=None):
        # If only the mac is provided, attempt to retrieve details from the database
        #if (ip == None & sensor_type == None & port_types == None & states == None & ports == None):
        if not ip and not sensor_type and not port_types and not states and not ports:
            self.sensor_mac = mac
            #self._get_id(mac)
            # If ID returned, pull the details from DB
            self.load()
        else:
            self.sensor_mac = mac
            self.sensor_ip = ip
            self.sensor_type = sensor_type
            self.states = states
            self.port_types = port_types
            # todo - take the independent port_types and states lists and zip to a single "ports" list
            self.ports = zip(self.port_types, self.states)

            # Get the ID for the sensor to determine if it already exists in the DB
            # If its a new sensor, register it, otherwise refresh it
            self._get_id()
            if (not self.sensor_id):
                self.register()
            else:
                self.refresh()

    def load(self):
        '''

        :return:
        '''
        sensor_info = db.get_sensor(self.sensor_mac)
        self.sensor_id = sensor_info[0][0]
        self.sensor_ip = sensor_info[0][3]
        self.sensor_type = sensor_info[0][7]
        #self.port_types = sensor_info[0][8]
        #self.states = sensor_info[0][9]
        self.ports = sensor_info[0][8]

    def register(self):
        'Register the sensor to the database'
        if (self.sensor_id): return 'Already registered.'
        n = db.sensor_register(self.sensor_mac, self.sensor_ip, self.sensor_type)
        self._get_id()
        self._port_register()
        return str(n)

    def refresh(self):
        'refresh an exiting sensor'
        u = db.sensor_refresh(self.sensor_mac, self.sensor_ip, self.sensor_id)
        self._port_refresh()
        # State_Override Check and clear
        # 1) Check if state_override set... if
        # 2) Check if current state equals desired state... if
        # 3) Clear state_override
        if (db.check_state_override(self.sensor_id)):
            print "Refresh - override set"
            current_match_desired = True
            c = db.get_current_states(self.sensor_id)
            d = db.get_desired_states(self.sensor_id)
            # print "Current: " + str(c)
            # print "Desired: " + str(d)
            for dp in d:
                if dp not in c:
                    # print "No match"
                    current_match_desired = False
                    break
            if current_match_desired:
                # print "Current equals Desired"
                db.clear_state_override(self.sensor_id)
            else:
                # print "Current not-equal Desired"
                pass





        return str(u)

    def _port_register(self):
        'Register the ports for this sensor'
        #for i, p in enumerate(self.states):
        #    db.port_register(self.sensor_id, i, p)
        for i, p in enumerate(self.ports):
            db.port_register(self.sensor_id, i, p)

    def _port_refresh(self):
        'refresh the state for ports for this sensor'
        #for i, p in enumerate(self.states):
        #    db.port_refresh(self.sensor_id, i, p)
        for i, p in enumerate(self.ports):
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

    # todo - looks like a running DB connection caches the state
    def desired_states(self):
        'Query the database for the desired states of the sensor'
        # First check to see if state_override has been set
        if (db.check_state_override(self.sensor_id)):
            # print "Override Set"
            d = db.get_desired_states(self.sensor_id)
        else:
            # print "Override NOT Set"
            d = db.get_current_states(self.sensor_id)
        #print d
        return d

class Sensor_v2(object):
    '''
        New version
        Object representing a single sensor from the system.
    '''

    def __init__(self, mac, ip=None, sensor_type=None, port_types=None, states=None, ports=None):
        '''
        Create a sensor object.
        :param mac:
        :param ip:
        :param sensor_type:
        :param port_types:
        :param states:
        :param ports:
        :return:
        '''

        # The mac address is a required attribute
        self.macaddress = mac

        # Try to load sensor from data source
        if (self.load()):
            # Sensor found in DB
            print "Loaded!"
            pass
        else:
            print "Not found!"
            # Todo - build code here to try to create a new sensor based on provided information
            pass

    def load(self):
        '''
        Attempt to retrieve information about this sensor from the data source
        :return:
        '''
        sensor = data.sensor_load(self.macaddress)
        if (sensor):
            for key in sensor:
                self.__dict__[key] = sensor[key]
            return True
        else:
            return False

    # Todo - add code to load the ports after the sensor details
        # will need to get a list of port_ids and then build port objects for each

