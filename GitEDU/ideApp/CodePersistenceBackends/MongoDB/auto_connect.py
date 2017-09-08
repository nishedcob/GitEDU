
from ideApp.CodePersistenceBackends.MongoDB.mongodb_connect import build_connection_from_settings

from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, MONGODB_CONNECT_TO

profiles = CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profiles']
config = profiles[CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile']]

#print(config)

'''build_connection(user=config['USER'], password=config['PASSWORD'], host=config['HOST'], port=config['PORT'],
                 database=config['NAME'])'''

#build_connection_from_settings(profiles=profiles, profile=config)
build_connection_from_settings(profile=config)
