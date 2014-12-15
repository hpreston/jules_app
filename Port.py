'''
    The class module for a Port Object
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


class Port(object):
    '''
        Object representing a single Port from the system.
    '''

    def __init__(self, port_id):
        # The mac address is a required attribute
        self.port_id = port_id

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
        Attempt to retrieve information about this portfrom the data source
        :return:
        '''

        # Sample from Sensor
        # sensor = data.sensor_load(self.macaddress)
        # if (sensor):
        #     for key in sensor:
        #         self.__dict__[key] = sensor[key]
        #     return True
        # else:
        #     return False

        pass
