
from ideApp.CodePersistenceBackends.generics import GenericNamespace, GenericRepository, GenericRepositoryFile,\
    CodePersistenceBackend

from ideApp.CodePersistenceBackends.MongoDB import mongodb_models, mongodb_connect

mongo_num_conn = 0

class MongoDBCodePersistenceBackend(CodePersistenceBackend):

    def __init__(self, profile=None):
        global mongo_num_conn
        if profile is None:
            raise ValueError("Connection Parameters can not be None")
        mongodb_connect.build_connection_from_settings(profile, 'mongo_%03d' % mongo_num_conn)
        mongo_num_conn = mongo_num_conn + 1
