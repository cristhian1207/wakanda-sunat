import sys
sys.path.insert(0, 'utils/')
sys.path.insert(0, 'dao/')
sys.path.insert(0, 'entity/')
from parameters import *
from SunatEntity import SunatEntity
import logging
import file_management
import sunat_table_dao
import entity_dao
from datetime import datetime

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

    logging.info('Descargando padrón')
    file_management.download_file()

    logging.info('Descomprimiendo padrón')
    file_management.unzip_file()

    logging.info('Partiendo archivos')
    total_rows=file_management.split_file()

    se=sunat_table_dao.find_available()
    setattr(se, 'locked', 1)
    sunat_table_dao.update(se)
    
    se_old=sunat_table_dao.find_available()

    files=file_management.files_in_folder(PATH_SUNAT_RUC)
    i=0
    for file in files:
        i+=1
        if file=='.DS_Store.txt':
            continue
        file_management.process_file(file, se)
        logging.info('%s/%s'%(i, len(files)))
    
    setattr(se, 'locked', 0)
    setattr(se, 'rows', total_rows)
    setattr(se, 'last_update', datetime.now())
    sunat_table_dao.update(se)

    entity_dao.truncate_table(se_old)
    logging.info('Proceso terminado')