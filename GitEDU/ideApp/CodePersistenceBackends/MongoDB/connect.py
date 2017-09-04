
from pymodm import connect

from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, MONGODB_CONNECT_TO

profiles = CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profiles']
config = profiles[CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile']]

# Read Connection Details from Settings
connection_str = "mongodb://"
user = config['USER']
if user is not None:
    connection_str += user
    password = config['PASSWORD']
    if password is not None:
        connection_str += ":" + password
    connection_str += "@"
connection_str += config['HOST']
port = config['PORT']
if port is not None:
    connection_str += ":" + port
connection_str += "/"
database = config['NAME']
if database is not None:
    connection_str += database

# print("Connection String: %s" % connection_str)

# Connect to MongoDB and call the connection "my-app".
connect(connection_str, alias=CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile'])

print("Connected to MongoDB @ mongodb://%s:%s" % (config['HOST'], config['PORT']))

# Connect to MongoDB and call the connection "my-app".
# connect("mongodb://localhost:27017/gitEduERP", alias="nosql")
