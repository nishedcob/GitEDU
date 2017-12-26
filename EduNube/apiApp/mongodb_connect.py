
from pymodm import connect

from .mongodb_settings import CONNECTION_DEFAULTS, MONGODB_ALIAS_STRING

mongodb_conn_num = 0


def build_connection_string(user=None, password=None, database=None, host=None, port=None, protocol=None):
    connection_str = ""
    if protocol:
        connection_str += protocol
    else:
        connection_str += CONNECTION_DEFAULTS['PROTOCOL']
    if user is None:
        if CONNECTION_DEFAULTS['USER'] is not None:
            user = CONNECTION_DEFAULTS['USER']
    if user is not None:
        connection_str += user
        if password is None:
            if CONNECTION_DEFAULTS['PASSWORD'] is not None:
                password = CONNECTION_DEFAULTS['PASSWORD']
        if password is not None:
            connection_str += ":" + password
        connection_str += "@"
    if host is None:
        if CONNECTION_DEFAULTS['HOST'] is not None:
            host = CONNECTION_DEFAULTS['HOST']
        else:
            raise ValueError("Host can't be None")
    connection_str += host
    if port is None:
        if CONNECTION_DEFAULTS['PORT'] is not None:
            port = CONNECTION_DEFAULTS['PORT']
    if port is not None:
        connection_str += ":" + port
    connection_str += "/"
    if database is None:
        if CONNECTION_DEFAULTS['DATABASE'] is not None:
            database = CONNECTION_DEFAULTS['DATABASE']
    if database is not None:
        connection_str += database
    #print(connection_str)
    return connection_str


def build_connection(user=None, password=None, database=None, host=None, port=None, protocol=None, alias=None):
    global mongodb_conn_num
    connection_str = build_connection_string(user=user, password=password, database=database, host=host, port=port,
                                             protocol=protocol)
    if alias is None:
        alias = MONGODB_ALIAS_STRING + str(mongodb_conn_num)
        mongodb_conn_num = mongodb_conn_num + 1
    alias = 'default'
    connect(connection_str, alias=alias)
    #connect("mongodb://gitEduUser:G1TedU$3r@127.0.0.1:27017/gitEduDB", alias=alias)
    print("Connected to MongoDB [alias: %s] @ mongodb://%s:%s" % (alias, host, port))


def build_connection_from_settings(profile=None, alias=None):
    #if profiles is None:
    #    raise ValueError("Profiles can not be None")
    if profile is None:
        raise ValueError("Profile can not be None")
    config = profile #profiles.get(profile)
    if config is None:
        raise ValueError("Invalid Configuration")
    build_connection(user=config.get('USER', None), password=config.get('PASSWORD', None),
                     database=config.get('NAME', None), host=config.get('HOST', None), port=config.get('PORT', None),
                     protocol=config.get('PROTOCOL', None), alias=alias)
