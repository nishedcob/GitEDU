
import gitlab
from GitEDU.settings import GITLAB_DEFAULT_SERVER, GITLAB_SERVERS

gitlab_default_srv = GITLAB_DEFAULT_SERVER


def connect_to_gitlab_token(protocol=None, host=None, port=None, token=None):
    if host is None:
        return None
    # gitlab_conn = gitlab.Gitlab(protocol + host + port, token)
    gitlab_conn = gitlab.Gitlab(protocol + host, token)
    #gitlab_conn.auth()
    return gitlab_conn


def connect_to_settings_gitlab_token(indx=GITLAB_DEFAULT_SERVER):
    return connect_to_gitlab_token(protocol=GITLAB_SERVERS[indx]['API_PROTOCOL'], host=GITLAB_SERVERS[indx]['HOST'],
                                   port=GITLAB_SERVERS[indx]['API_PROTOCOL'], token=GITLAB_SERVERS[indx]['TOKEN'])


def connect_to_gitlab_user_password(protocol=None, host=None, port=None, user=None, password=None):
    if host is None:
        return None
    gitlab_conn = gitlab.Gitlab(protocol + host + port, email=user, password=password)
    gitlab_conn.auth()
    return gitlab_conn


def connect_to_settings_gitlab_user_password(indx=GITLAB_DEFAULT_SERVER):
    return connect_to_gitlab_user_password(protocol=GITLAB_SERVERS[indx]['API_PROTOCOL'],
                                           host=GITLAB_SERVERS[indx]['HOST'], port=GITLAB_SERVERS[indx]['API_PROTOCOL'],
                                           user=GITLAB_SERVERS[indx]['USER'], password=GITLAB_SERVERS[indx]['PASSWORD'])


def connect_to_settings_gitlab(indx=GITLAB_DEFAULT_SERVER):
    if GITLAB_SERVERS[indx]['WITH_TOKEN']:
        return connect_to_settings_gitlab_token(indx)
    elif GITLAB_SERVERS[indx]['WITH_CRED']:
        return connect_to_settings_gitlab_user_password(indx)
    else:
        return None

gitlab_srv = None
try:
    gitlab_srv = connect_to_settings_gitlab(gitlab_default_srv)
except Exception as e:
    print("No se pudo connectar a GitLab")
    print(e)