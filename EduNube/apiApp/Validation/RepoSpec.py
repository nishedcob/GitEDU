
import re
import jwt
import bcrypt

from apiApp.models import RepoSpec

clean_repospec = re.compile('([a-zA-Z0-9_\.]+)')

def validate_repospec(repospec=None):
    if repospec is None:
        raise ValueError("RepoSpec can't be None")
    repospec = clean_repospec.findall(repospec)[0]
    stored_repospec = RepoSpec.objects.get(token=repospec)
    if stored_repospec is None:
        raise ValueError('No Stored RepoSpec Token for token \'%s\'' % repospec)
    repospec_values = decode_repospec(repospec=repospec, stored_repospec=stored_repospec)
    return stored_repospec.repo == repospec_values.get('repo') and\
           stored_repospec.parent_repo == repospec_values.get('parent_repo')


def decode_repospec(repospec, stored_repospec=None):
    repospec = clean_repospec.findall(repospec)[0]
    return decode(repospec=repospec, stored_repospec=stored_repospec, decode_stored=False)


def decode(repospec=None, stored_repospec=None, decode_stored=False):
    if not decode_stored:
        if repospec is None:
            raise ValueError("RepoSpec can't be None")
        else:
            repospec = clean_repospec.findall(repospec)[0]
            if stored_repospec is None:
                stored_repospec = RepoSpec.objects.get(token=repospec)
            if stored_repospec is None:
                raise ValueError('No Stored RepoSpec Token for token \'%s\'' % repospec)
            return jwt.decode(repospec, stored_repospec.secret_key, algorithms=[stored_repospec.token_algo])
    else:
        if repospec is None and stored_repospec is None:
            raise ValueError("Both RepoSpec and Stored_RepoSpec can't be None")
        else:
            if stored_repospec is None:
                repospec = clean_repospec.findall(repospec)[0]
                stored_repospec = RepoSpec.objects.get(token=repospec)
            if stored_repospec is None:
                raise ValueError('No Stored RepoSpec Token for token \'%s\'' % repospec)
            return jwt.decode(stored_repospec.token, stored_repospec.secret_key,
                              algorithms=[stored_repospec.token_algo])


def encode(parent, repo):
    return create(parent, repo)


def create(parent, repo, algo='HS256'):
    if repo is None:
        raise ValueError("Repo can't be None")
    repospec_values = {
        'repo': repo
    }
    if parent is not None:
        repospec_values['parent_repo'] = parent
    secret_key = bcrypt.gensalt()  # Generate Random Unique Secret Key
    repospec = RepoSpec(**repospec_values, secret_key=secret_key, token_algo=algo)
    repospec.token = jwt.encode(payload=repospec_values, key=secret_key, algorithm=algo)
    repospec.save()
    return repospec


def update_repo(old_repo, parent=None, new_repo=None, regen_secret_key=False):
    if old_repo is None:
        raise ValueError("Old_Repo can't be None")
    repospec = RepoSpec.objects.get(token=old_repo)
    if repospec is None:
        raise ValueError("RepoSpec with Token '%s' does not exist" % old_repo)
    if new_repo is None:
        new_repo = repospec.repo
    return update_repospec(repospec=repospec, parent=parent, repo=new_repo, regen_secret_key=regen_secret_key)


def update_repospec(repospec, parent=None, repo=None, regen_secret_key=False):
    if repospec is None:
        raise ValueError("Provided RepoSpec Object can't be None")
    if regen_secret_key:
        repospec.secret_key = bcrypt.gensalt()
    if repo is not None:
        repospec.repo = repo
    repospec.parent_repo = parent
    payload = {
        'repo': repospec.repo,
        'parent_repo': repospec.parent_repo
    }
    repospec.token = jwt.encode(payload=payload, key=repospec.secret_key, algorithm=repospec.token_algo)
    repospec.save()
    return repospec
