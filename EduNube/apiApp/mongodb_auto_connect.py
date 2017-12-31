
from apiApp.mongodb_connect import build_connection_from_settings

from EduNube.settings import MONGODB_CONNECT_TO, NOSQL_DATABASES

profiles = NOSQL_DATABASES
alias = MONGODB_CONNECT_TO
config = profiles[alias]

#print(config)

'''build_connection(user=config['USER'], password=config['PASSWORD'], host=config['HOST'], port=config['PORT'],
                 database=config['NAME'])'''

#build_connection_from_settings(profiles=profiles, profile=config)
build_connection_from_settings(profile=config, alias=alias)
