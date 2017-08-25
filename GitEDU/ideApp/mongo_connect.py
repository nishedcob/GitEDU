
from pymodm import connect

from GitEDU.settings import NOSQL_DATABASES

# Read Connection Details from Settings
connection_str = "mongodb://"
user = NOSQL_DATABASES['nosql']['USER']
if user is not None:
    connection_str += user
    password = NOSQL_DATABASES['nosql']['PASSWORD']
    if password is not None:
        connection_str += ":" + password
    connection_str += "@"
connection_str += NOSQL_DATABASES['nosql']['HOST']
port = NOSQL_DATABASES['nosql']['PORT']
if port is not None:
    connection_str += ":" + port
connection_str += "/"
database = NOSQL_DATABASES['nosql']['NAME']
if database is not None:
    connection_str += database

# Connect to MongoDB and call the connection "my-app".
connect(connection_str, alias="nosql")

# Connect to MongoDB and call the connection "my-app".
# connect("mongodb://localhost:27017/gitEduERP", alias="nosql")
