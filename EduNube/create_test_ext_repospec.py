# coding: utf-8
from repospec_example_client import EduNubeRepoSpecConsumer
enrsc = EduNubeRepoSpecConsumer()
repo = 'nishedcob/test.git'
parent_repo = 'http://10.10.10.1/python3-code-executor-template.git'
enrsc.create(repo=repo, parent_repo=parent_repo)
enrsc.get(repo=repo).text
