from dataquery import *
import credentials
import sys

# Create the MySQLdb object with the proper credentials to connect to
# the data base with all of the network flow data.
if 'port' in credentials.login:
    db = MySQLdb.connect(user = credentials.login['user'], 
    passwd = credentials.login['password'],
    db = credentials.login['db'],
    host = credentials.login['host'],
    port = int(credentials.login['port']))
else:
    db = MySQLdb.connect(user = credentials.login['user'], 
    	passwd = credentials.login['password'],
    	db = credentials.login['db'],
    	host = credentials.login['host'])
c = db.cursor()
db = DataQuery(c)