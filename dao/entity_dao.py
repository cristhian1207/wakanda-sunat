from my_sql_connection import *
from parameters import *
from SunatEntity import SunatEntity
import logging

def import_data(filename, se):
    # allow_load_data()
    conn=get_connection()
    table_name=se.table_name
    query="""
        LOAD DATA LOCAL INFILE '%s' 
        INTO TABLE %s
        CHARACTER SET latin1
        FIELDS TERMINATED BY '|' 
        OPTIONALLY ENCLOSED BY '"' 
        LINES TERMINATED BY '\n'
        (ruc, name, status, address_condition, ubigeo, address_type, address_name, zone_code, zone_type, 
            address_no, address_in, address_lot, address_dpt, address_block, address_km)
        """ % (filename, table_name)  
    logging.info('Poblando tabla: %s'%table_name)
    with conn.cursor() as c:
        c.execute(query)
        conn.commit()
    conn.close()

def allow_load_data():
    conn=get_connection()
    query='SET GLOBAL local_infile = 1;'
    with conn.cursor() as c:
        c.execute(query)
        conn.commit()
    conn.close()

def truncate_table(se):
    conn=get_connection()
    table_name=se.table_name
    logging.info('Truncando tabla: %s' % table_name)
    query='TRUNCATE %s' % table_name
    with conn.cursor() as c:
        c.execute(query)
        conn.commit()
    conn.close()
