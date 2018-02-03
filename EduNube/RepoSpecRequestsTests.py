# coding: utf-8
from repospec_example_client import EduNubeRepoSpecConsumer

enrsc = EduNubeRepoSpecConsumer()

repo = 'shell-code-executor-template'
create_request = enrsc.create(repo=repo)
print(create_request.text)

get_request = enrsc.get(repo=repo)
print(get_request.text)

repo = 'postgresql-code-executor-template'
get_or_create_request = enrsc.get_or_create(repo=repo)
print(get_or_create_request.text)

get_or_create_request = enrsc.get_or_create(repo=repo)
print(get_or_create_request.text)

repospec_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXBvIjoicG9zdGdyZXNxbC1jb2RlLWV4ZWN1dG9yLXRlbXBsYXRlIn0.cv' \
                 'JgNebtviihNa-rAE74g9begUypZ5qpX8_CcP2XSm4'
get_or_create_request = enrsc.get_or_create(repo=repo, repospec_token=repospec_token)
print(get_or_create_request.text)

edit_request = enrsc.edit(repo=repo)
print(edit_request.text)

parent = 'shell-code-executor-template'
edit_request = enrsc.edit(repo=repo, parent_repo=parent)
print(edit_request.text)

regen_secret_key = True
edit_request = enrsc.edit(repo=repo, parent_repo=parent, regen_secret_key=regen_secret_key)
print(edit_request.text)
