
from GitEDU.ideApp.CodePersistenceBackends.MongoDB.models import CodeModel
from ideApp.CodePersistenceBackends.GitLab.connect import gitlab_srv
from ideApp.models import GitlabUser, GitlabSnippet


def get_gitlab_user(gitlab_conn=gitlab_srv, user=None):
    if gitlab_conn is None:
        return None
    if user is None or not user.is_authenticated:
        return None
    gitlab_users = GitlabUser.objects.filter(user=user)
    gitlab_user = None
    if len(gitlab_users) == 0:
        username = user.username
        users_in_gitlab = gitlab_conn.users.list(username=username)  # , private_token='yP1RiyMZiDBzDAgTDzNz')
        if len(users_in_gitlab) == 0:
            remote_gitlab_user = gitlab_conn.users.create({'username': username, 'password': username+username+username,
                                                           'name': user.first_name + " " + user.last_name,
                                                           'email': user.email})
        else:
            idx = 0
            while len(users_in_gitlab) != 0:
                idx += 1
                users_in_gitlab = gitlab_conn.users.list(username=(username + str(idx)))  # , private_token='yP1RiyMZiDBzDAgTDzNz')
            remote_gitlab_user = gitlab_conn.users.create({'username': username, 'password': username,
                                                           'name': user.first_name + " " + user.last_name})
        local_gitlab_user = GitlabUser(user=user, username=username, email=user.email, password=username,
                                       name=user.first_name + " " + user.last_name)
        remote_gitlab_user.save()
        local_gitlab_user.save()
        gitlab_user = local_gitlab_user
    elif len(gitlab_users) == 1:
        gitlab_user = gitlab_users[0]
    return gitlab_user


def create_gitlab_snippet(gitlab_conn=gitlab_srv, user=None, user_code=None):
    if gitlab_conn is None:
        print("sin conexion")
        return None
    if user is None or not user.is_authenticated:
        print("no autenticado")
        return None
    if user_code is None:
        print("sin codigo")
        return None
    gitlab_user = get_gitlab_user(gitlab_conn=gitlab_conn, user=user)
    if gitlab_user is None:
        print("sin usuario de gitlab")
        return None
    print("code_id: " + str(user_code.code_id))
    codes = CodeModel.objects.raw({'cmid': str(user_code.code_id)})
    # code = None
    if codes is None:
        print("nada en mongo")
        return None
    elif codes.count() == 0:
        print("cero resultados mongo")
        return None
    elif codes.count() > 1:
        print("muchos resultados mongo")
        return None
    else:
        code = codes[0]
    snippet = gitlab_conn.snippets.create({'title': user_code.file_name,
                                           'file_name': user_code.file_name,
                                           'content': code.code}, sudo=gitlab_user.username, private_token='EwJbTqxDY-sQF_sPDScb')
    snippet.save()
    gitlab_snippet = None
    if snippet is not None:
        gitlab_snippet = GitlabSnippet(gitlabUser=gitlab_user, userCode=user_code, title=user_code.file_name,
                                       file_name=user_code.file_name, code_id=user_code.code_id, snippet_id=snippet.id)
        gitlab_snippet.save()
    return snippet, gitlab_snippet


def get_gitlab_snippet(gitlab_conn=gitlab_srv, user=None, snippet_id=None):
    if gitlab_conn is None:
        return None
    if user is None:  # or not user.is_authenticated:
        return None
    if snippet_id is None:
        return None
    return gitlab_conn.snippets.get(snippet_id, sudo=user.username)  # , private_token='yP1RiyMZiDBzDAgTDzNz')


def update_gitlab_snippet(gitlab_conn=gitlab_srv, user=None, snippet=None, user_code=None, code=None):
    if gitlab_conn is None:
        return None
    if user is None:  # or not user.is_authenticated:
        return None
    if snippet is None:
        return None
    if user_code is None:
        return None
    if code is None:
        return None
    snippet.title = user_code.file_name
    snippet.file_name = user_code.file_name
    snippet.content = code.code
    snippet.save()  # private_token='yP1RiyMZiDBzDAgTDzNz')
    return snippet
