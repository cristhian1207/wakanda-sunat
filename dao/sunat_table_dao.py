from SunatEntity import SunatEntity
from my_sql_connection import *

def update(se):
    cnn=get_connection()
    query="""
        UPDATE sunat_table se
        SET se.locked=%s, se.rows=%s, se.last_update=%s
        WHERE se.id=%s
    """
    args=(se.locked, se.rows, se.last_update, se.id)
    with cnn.cursor() as c:
        c.execute(query, args)
        cnn.commit()
    cnn.close()

def find_available():
    cnn=get_connection()
    query="""
        SELECT st.id, st.table_name, st.locked, st.rows, st.last_update
        FROM sunat_table as st
        WHERE locked=0
        ORDER BY last_update DESC
        LIMIT 1
    """
    se=None
    with cnn.cursor() as c:
        c.execute(query)
        result=c.fetchone()
        se=SunatEntity(
            result[0],
            result[1],
            result[2],
            result[3],
            result[4]
        )
    cnn.close()
    return se