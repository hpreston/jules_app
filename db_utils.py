'''
    These functions are used to interface with the database

'''

__author__ = 'hpreston'

from collections import namedtuple
import cymysql
import time

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0,0)

# Variables for the DB Conenction
dbhost = '10.192.81.111'
dbuser = 'jules'
dbpassword = 'password'
dbname = 'jules'

class mysqldb(object):
    'Object for working with the mysql database backend'

    def __init__(self, dbhost = dbhost, dbuser = dbuser, dbpassword = dbpassword, dbname = dbname):
        '''

        :param dbhost: Database Server to use
        :param dbuser: User to conenct as
        :param dbpassword: Password for user
        :param dbname: Database name
        :return:
        '''
        self.conn = cymysql.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbname)

    def get_sensor(self, mac):
        '''
        Get details about the specified sensor
        :param mac:
        :return:
        '''
        query = "SELECT * " \
              "FROM sensor " \
              "WHERE sensor_mac = '%s'" % (mac)
        query = "SELECT " \
                "sensor.sensor_id, sensor.site_id, sensor.sensor_type_id, " \
                "sensor.sensor_mac, sensor.local_ip, sensor.date_register, sensor.date_refresh, " \
                "sensor_type.sensor_part_number " \
                "FROM sensor " \
                "INNER JOIN sensor_type ON sensor.sensor_type_id = sensor_type.sensor_type_id " \
                "WHERE sensor.sensor_mac = '%s' " % (mac)

        cur = self.conn.cursor()
        cur.execute(query)
        # Get most of the info
        s = cur.fetchall()
        if len(s) > 0:
            s[0] = list(s[0])
            # Get the port_types and states
            query = "SELECT " \
                    "port_type.port_part_number, port.current_state " \
                    "FROM port " \
                    "INNER JOIN port_type ON port.port_type_id = port_type.port_type_id " \
                    "WHERE port.sensor_id = %s " % (s[0][0])
            cur = self.conn.cursor()
            cur.execute(query)
            s[0].append(list(cur.fetchall()))

        return s

    def sensor_register(self, mac, ip, sensor_type):
        '''
        Function will register a sensor to the database
        :param mac:
        :param ip:
        :param time:
        :return:
        '''
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        # Determine the sensor_type_id based on part number
        sensor_type_id = self.get_sensor_type_id(sensor_type)

        query = "INSERT INTO sensor " \
                "(site_id, sensor_type_id, sensor_mac, local_ip, date_register) " \
                "VALUES " \
                "(%s, %s, '%s', '%s', '%s')" % (1, sensor_type_id, mac, ip, t)
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return self.get_sensor(mac)

    def sensor_refresh(self, mac, ip, id):
        '''

        :param mac:
        :param ip:
        :return:
        '''
        query = "UPDATE sensor " \
                "SET " \
                "site_id = %s, " \
                "local_ip = '%s' " \
                "WHERE " \
                "sensor_id = '%s' " \
                % (1, ip, id)
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return self.get_sensor(mac)

    def port_register(self, sensor_id, index, port):
        '''

        :param sensor_id:
        :param index:
        :param port:
        :return:
        '''
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        # Determine the port_type_id based on the part_number
        port_type_id = self.get_port_type_id(port[0])

        query = "INSERT INTO port " \
                "(sensor_id, sensor_index, port_type_id, current_state) " \
                "VALUES " \
                "(%s, %s, %s, '%s')" % (sensor_id, index, port_type_id, port[1])
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def port_refresh(self, sensor_id, index, port):
        '''

        :param sensor_id:
        :param index:
        :param state:
        :return:
        '''
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "UPDATE port " \
                "SET " \
                "current_state = '%s' " \
                "WHERE sensor_id = %s AND sensor_index = %s " \
                % (port[1], sensor_id, index)
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def get_sensor_type_id(self, type):
        '''
        Get the sensor_id for the specified part_number
        :param type:
        :return:
        '''
        query = "SELECT sensor_type_id " \
              "FROM sensor_type " \
              "WHERE sensor_part_number = '%s'" % (type)

        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()[0][0]

    def get_port_type_id(self, type):
        '''
        Get the sensor_id for the specified part_number
        :param type:
        :return:
        '''
        query = "SELECT port_type_id " \
              "FROM port_type " \
              "WHERE port_part_number = '%s'" % (type)

        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()[0][0]

    def get_desired_states(self, sensor_id):
        '''

        :param sensor_id:
        :return:
        '''
        query = "SELECT sensor_index, desired_state " \
                "FROM port " \
                "WHERE sensor_id = %s AND desired_state IS NOT NULL" % (sensor_id)
                #"INNER JOIN sensor ON port.sensor_id = sensor.sensor_id " \
        #print(query)
        cur = self.conn.cursor()
        cur.execute(query)
        #print cur.fetchall()
        return cur.fetchall()

    def get_current_states(self, sensor_id):
        '''

        :param sensor_id:
        :return:
        '''
        query = "SELECT sensor_index, current_state " \
                "FROM port " \
                "WHERE sensor_id = %s" % (sensor_id)
                #"INNER JOIN sensor ON port.sensor_id = sensor.sensor_id " \
        #print(query)
        cur = self.conn.cursor()
        cur.execute(query)
        #print cur.fetchall()
        return cur.fetchall()

    def check_state_override(self, sensor_id):
        '''
        Check if this sensor has had current state override set
        :param sensor_id:
        :return: boolean
        '''
        query = "SELECT state_override " \
                "FROM sensor " \
                "WHERE sensor_id = %s " % (sensor_id)
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        #print cur.fetchall()
        return cur.fetchall()[0][0]

    def clear_state_override(self, sensor_id):
        query = "UPDATE sensor " \
                "SET " \
                "state_override = 0 " \
                "WHERE " \
                "sensor_id = '%s' " \
                % (sensor_id)
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()


    def accountlist(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM account'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def userlist(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM user'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def sitelist(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM site'
        jquery = 'SELECT account.account_name,' \
                 'user.username,' \
                 'site.site_name ' \
                 'FROM site ' \
                 'INNER JOIN account ON site.account_id = account.account_id ' \
                 'INNER JOIN user ON site.admin_id = user.user_id'
        print jquery
        cur = self.conn.cursor()
        cur.execute(jquery)
        return cur.fetchall()

    def sensortypes(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM sensor_types'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def portypes(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM port_types'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def sensorlist(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM sensor'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def portlist(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM port'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def readinglist(self):
        '''

        :return:
        '''
        query = 'SELECT * FROM reading'
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()






