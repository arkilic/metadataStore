__author__ = 'arkilic'
from mongoengine import connect
from pymongo.errors import ConnectionFailure


from metadataStore.config.parseConfig import database, host, port
from metadataStore.sessionManager.databaseLogger import DbLogger

try:
    conn = connect(db=database, host=host, port=int(port))
    db = conn['metaDataStore']
except:
    raise ConnectionFailure('Connection cannot be established')

metadataLogger = DbLogger(db_name=database, host=host, port=int(port))