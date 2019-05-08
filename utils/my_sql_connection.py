import MySQLdb
from global_config import *

def get_connection():
    return MySQLdb.connect(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        passwd=MYSQL_CONFIG['passwd'],
        database=MYSQL_CONFIG['database'],
        local_infile=MYSQL_CONFIG['local_infile']
    )