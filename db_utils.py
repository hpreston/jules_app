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


# ToDo - 1st move to a different file
# ToDo - 2nd move to a serparte module with indpendent API
class jules_data(object):
    '''
    Database interface for working with the MySQL database backend
    '''

    def __init__(self, dbhost = dbhost, dbuser = dbuser, dbpassword = dbpassword, dbname = dbname):
        '''

        :param dbhost: Database Server to use
        :param dbuser: User to conenct as
        :param dbpassword: Password for user
        :param dbname: Database name
        :return:
        '''
        self.conn = cymysql.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbname)

    def sensor_load(self, macaddress, id = None):
        '''
        Pull relevant data from the database for a sensor with given mac address
        :param macaddress:
        :return:
        '''

        query = "SELECT " \
                    "sensor.sensor_id, " \
                    "sensor.site_id, " \
                    "sensor.sensor_type_id, " \
                    "sensor.sensor_mac, " \
                    "sensor.local_ip, " \
                    "sensor.date_register, " \
                    "sensor.date_refresh, " \
                    "sensor_type.sensor_part_number, " \
                    "sensor.name, " \
                    "sensor.description, " \
                    "sensor.location," \
                    "sensor.state_override " \
                    " " \
                "FROM sensor " \
                "INNER JOIN sensor_type ON sensor.sensor_type_id = sensor_type.sensor_type_id " \
                "WHERE " \
                    "sensor.sensor_mac = '%s' OR " \
                    "sensor.sensor_id = %s " % (macaddress, id)

        cur = self.conn.cursor()
        cur.execute(query)
        # Get most of the info
        sensor_list = cur.fetchall()

        if len(sensor_list) > 0:
            # Build a dictionary of relevant details
            sensor = {
                        "id": sensor_list[0][0],
                        "site_id": sensor_list[0][1],
                        "sensor_type_id": sensor_list[0][2],
                        "sensor_mac": sensor_list[0][3],
                        "local_ip": sensor_list[0][4],
                        "date_register": sensor_list[0][5],
                        "date_refresh": sensor_list[0][6],
                        "sensor_part_number": sensor_list[0][7],
                        "name": sensor_list[0][8],
                        "description": sensor_list[0][9],
                        "location": sensor_list[0][10],
                        "state_override": sensor_list[0][11]
                      }
            return sensor
        else:
            # No sensor found
            return False

    def sensor_port_list(self, sensor_id):
        '''
        Get the list of port_ids for all ports registered with this sensor_id
        :param sensor_id:
        :return:
        '''

        query = "SELECT " \
                "port.port_id " \
                "FROM port " \
                "WHERE " \
                "port.sensor_id = %s " % (sensor_id)

        cur = self.conn.cursor()
        cur.execute(query)
        port_list = cur.fetchall()
        return [port[0] for port in port_list]

    def port_load(self, port_id):
        '''
        Pull relevant data from the database for a port with given port_id
        :param macaddress:
        :return:
        '''

        query = "SELECT " \
                    "port.port_id, " \
                    "port.sensor_index, " \
                    "port_type.port_part_number, " \
                    "port.current_state, " \
                    "port.desired_state, " \
                    "port.name, " \
                    "port.description " \
                    " " \
                "FROM port " \
                "INNER JOIN port_type ON port.port_type_id = port_type.port_type_id " \
                "WHERE " \
                    "port.port_id = %s " \
                "ORDER BY port.sensor_index " % (port_id)

        cur = self.conn.cursor()
        cur.execute(query)
        # Get most of the info
        port_list = cur.fetchall()

        if len(port_list) > 0:
            # Build a dictionary of relevant details
            port = {
                        "id" : port_list[0][0],
                        "sensor_index" : port_list[0][1],
                        "part_number" : port_list[0][2],
                        "current_state" : port_list[0][3],
                        "desired_state" : port_list[0][4],
                        "name" : port_list[0][5],
                        "description" : port_list[0][6]
                      }
            # print port
            return port
        else:
            # No sensor found
            return False

    def site_load(self, site_id):
        '''
        Pull relevant data from the database for a site with given site_id
        :param site_id:
        :return:
        '''
        query = "SELECT " \
                    "site.site_id, " \
                    "site.site_name " \
                    " " \
                "FROM site " \
                "WHERE " \
                    "site.site_id = %s " % (site_id)

        cur = self.conn.cursor()
        cur.execute(query)
        # Get most of the info
        site_list = cur.fetchall()

        if len(site_list) > 0:
            # Build a dictionary of relevant details
            site = {
                        "id" : site_list[0][0],
                        "name" : site_list[0][1]
                      }
            return site
        else:
            return False

    def site_sensor_list(self, site_id):
        '''
        Get the list of sensor_ids for all sensors registered with this site_id
        :param site_id:
        :return:
        '''

        query = "SELECT " \
                "sensor.sensor_id " \
                "FROM sensor " \
                "WHERE " \
                "sensor.site_id = %s " % (site_id)

        cur = self.conn.cursor()
        cur.execute(query)
        sensor_list = cur.fetchall()
        return [sensor[0] for sensor in sensor_list]
