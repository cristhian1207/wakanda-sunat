from parameters import *
from global_config import *
import os
import zipfile
import urllib3
import entity_dao


def download_file():
    chunksize=1000
    http=urllib3.PoolManager()
    response=http.request('GET', URL_SUNAT_RUC, preload_content=False)
    with open(ZIP_SUNAT_RUC, 'wb') as padron:
        while 1:
            data=response.read(chunksize)
            if not data:
                break
            padron.write(data)
    response.release_conn()

def unzip_file():
    with zipfile.ZipFile(ZIP_SUNAT_RUC, 'r') as zipref:
        zipref.extractall(PATH_SUNAT_RUC)
    remove_file(ZIP_SUNAT_RUC)

def remove_file(filename):
    os.remove(filename)

def rows_quantity_in_file(filename):
    process=os.popen("sed -n '=' " + filename + '| wc -l')
    rows_qty=int(process.read())
    process.close()
    return rows_qty

def split_file():
    total_rows=0
    suffix='.bak'
    dfl_cmd="sed -i 1d %s" % (TXT_SUNAT_RUC)
    os.system(dfl_cmd)
    old_fn='prev_charset.txt'
    rnm_cmd='mv %s %s' % (TXT_SUNAT_RUC, old_fn)
    os.system(rnm_cmd)
    charset_cmd='iconv -f iso-8859-1 -t utf-8 %s > %s' % (old_fn, TXT_SUNAT_RUC)
    os.system(charset_cmd)

    total_rows=rows_quantity_in_file(TXT_SUNAT_RUC)  
    rows_per_file=0
    mod_file=total_rows % FILES_NUMBER
    rows_per_file=round(total_rows / FILES_NUMBER)
    if mod_file != 0:
        rows_per_file += + mod_file
    
    split_cmd=''
    if OPERATIVE_SYSTEM=='mac':
        split_cmd='split -l %s %s %s' % (rows_per_file, TXT_SUNAT_RUC, TXT_SUNAT_RUC + '.')
    else:
        split_cmd='split -l %s --additional-suffix .csv -d %s %s' % (rows_per_file, TXT_SUNAT_RUC, TXT_SUNAT_RUC)
        
    os.system(split_cmd)
    remove_file(TXT_SUNAT_RUC)
    if OPERATIVE_SYSTEM=='mac':
        for root, dirs, files in os.walk(PATH_SUNAT_RUC):
            for file in files:
                os.rename(PATH_SUNAT_RUC+file, PATH_SUNAT_RUC+file+'.txt')
    return total_rows

def files_in_folder(folder):
    for root, dirs, files in os.walk(folder):
        return files
    return []

def process_file(filename, se):
    filename=PATH_SUNAT_RUC+filename
    entity_dao.import_data(filename, se)
    remove_file(filename)