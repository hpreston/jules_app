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
            # print "Loaded!"
            pass
        else:
            # print "Not found!"
            pass

    def load(self):
        '''
        Attempt to retrieve information about this port from the data source
        :return:
        '''
        port = data.port_load(self.port_id)
        if (port):
            for key in port:
                self.__dict__[key] = port[key]
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
