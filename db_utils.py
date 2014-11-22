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
dbhost = '10.192.81.102'
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

        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def sensor_register(self, mac, ip):
        '''
        Function will register a sensor to the database
        :param mac:
        :param ip:
        :param time:
        :return:
        '''
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO sensor " \
                "(site_id, sensor_type_id, sensor_mac, local_ip, date_register) " \
                "VALUES " \
                "(%s, %s, '%s', '%s', '%s')" % (1, 1, mac, ip, t)
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
                "sensor_type_id = %s, " \
                "local_ip = '%s' " \
                "WHERE " \
                "sensor_id = '%s' " \
                % (1, 1, ip, id)
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return self.get_sensor(mac)

    def port_register(self, sensor_id, index, state):
        '''

        :param sensor_id:
        :param index:
        :param state:
        :return:
        '''
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO port " \
                "(sensor_id, sensor_index, current_state) " \
                "VALUES " \
                "(%s, %s, '%s')" % (sensor_id, index, state)
        #print query
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def port_refresh(self, sensor_id, index, state):
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
                % (state, sensor_id, index)
        #print query
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






