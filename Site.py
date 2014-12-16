'''
    The class module for a Site Object
'''

__author__ = 'hapresto'

from collections import namedtuple
from time import time, mktime
from db_utils import jules_data
from datetime import datetime, timedelta
import json
from Sensor import Sensor_v2

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0, 0)

data = jules_data()

class Site(object):
    '''
        Object representing a Site in the system
    '''

    def __init__(self, site_id):
        # The site_id is a required attribute
        self.site_id = site_id

        # Try to load port from data source
        if (self.load()):
            # Found in DB
            print "Loaded!"
            pass
        else:
            print "Not found!"
            pass

    def load(self):
        '''
        Attempt to retrieve information about this site from the data source
        :return:
        '''
        site = data.site_load(self.site_id)
        if (site):
            for key in site:
                self.__dict__[key] = site[key]
            self._get_sensor_list()
            return True
        else:
            return False

    def _get_sensor_list(self):
        '''
        Get the list of sensors, if any that this site has registered with the database
        :return:
        '''
        sensor_list = data.site_sensor_list(self.site_id)
        if (len(sensor_list) > 0):
            self.sensors = []
            for sensor_id in sensor_list:
                #self.ports.append(data.port_load(port))
                sensor = Sensor_v2(id = sensor_id)
                self.sensors.append(sensor)
            return True
        else:
            return False


    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__dict__.__repr__()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
