
from EduNube.settings import GIT_SERVER_HOST_SSH, GIT_SERVER_HOST_HTTP


def build_git_base_http_url():
    protocol = GIT_SERVER_HOST_HTTP.get('protocol')
    if protocol is None:
        raise ValueError("GIT_SERVER_HOST doesn't define a Protocol")
    host = GIT_SERVER_HOST_HTTP.get('host')
    if host is None:
        raise ValueError("GIT_SERVER_HOST doesn't define a Host")
    url = "%s://" % protocol
    print("Building Git Base URL: %s" % url)
    user = GIT_SERVER_HOST_HTTP.get('user')
    if user is not None:
        url = "%s%s" % (url, user)
        print("Building Git Base URL: %s" % url)
        password = GIT_SERVER_HOST_HTTP.get('password')
        if password is not None:
            url = "%s:%s" % (url, password)
            print("Building Git Base URL: %s" % url)
        url = "%s@" % url
        print("Building Git Base URL: %s" % url)
    url = "%s%s" % (url, host)
    print("Building Git Base URL: %s" % url)
    port = GIT_SERVER_HOST_HTTP.get('port')
    if port is not None:
        url = "%s:%s" % (url, str(port))
        print("Building Git Base URL: %s" % url)
    return url


def build_git_base_url_ssh(repo_type):
    url = ''
    if GIT_SERVER_HOST_SSH.get('alias') is not None:
        url = GIT_SERVER_HOST_SSH.get('alias')
    else:
        if GIT_SERVER_HOST_SSH.get('user') is not None:
            url = "%s@" % GIT_SERVER_HOST_SSH.get('user')
        if GIT_SERVER_HOST_SSH.get('host') is None:
            raise ValueError('Host can\'t be None if Alias is None!')
        url += '%s' % GIT_SERVER_HOST_SSH.get('host')
    url += ':'
    if GIT_SERVER_HOST_SSH.get('base_route') is None:
        raise ValueError('base_route can\'t be None')
    url += GIT_SERVER_HOST_SSH.get('base_route')
    routes = GIT_SERVER_HOST_SSH.get('routes')
    if routes is None:
        raise ValueError('routes can\'t be None')
    if routes.get(repo_type) is None:
        raise ValueError('Specified repo_type = \'%s\' within routes can\'t be None')
    url += routes.get(repo_type)
    return url
