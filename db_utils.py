'''
    These functions are used to interface with the database

'''

__author__ = 'hpreston'

from collections import namedtuple
import cymysql

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0,0)

# Variables for the DB Conenction
dbhost = '10.192.81.102'
dbuser = 'jules'
dbpassword = 'password'
dbname = 'jules'

class mysqldb(object):
    'Object for working with the mysql database backend'

    def __init__(self, dbhost, dbuser, dbpassword, dbname):
        '''

        :param dbhost: Database Server to use
        :param dbuser: User to conenct as
        :param dbpassword: Password for user
        :param dbname: Database name
        :return:
        '''
        self.conn = cymysql.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbname)

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







