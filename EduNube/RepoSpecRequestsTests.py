# coding: utf-8
import requests
base_url = "http://127.0.0.1:8010/api/repospec/"
operation = "create"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBfbmFtZSI6IkdpdEVEVSIsImV4cGlyZXMiOmZhbHNlLCJjcmVhdGVkX2RhdGUiOiIyMDE3LTExLTEyIDE3OjMzOjE3LjY0MTY4MSIsImVkaXRfZGF0ZSI6IjIwMTctMTEtMTIgMjA6MzY6NDAuMjc5NDAyIn0.825oh2rZUlIPZFaP_UbYPDpdsXTE0XCaNsia-3NnGuc"
payload = {'token': token}
repo = 'shell-code-executor-template'
parent = None
payload['repo'] = repo
print(payload)
create_request = requests.post(base_url + operation, data=payload)
print(create_request.text)
operation = "get"
get_request = requests.post(base_url + operation, data=payload)
print(get_request.text)
operation = "get_or_create"
repo = 'postgresql-code-executor-template'
payload['repo'] = repo
get_or_create_request = requests.post(base_url + operation, data=payload)
print(get_or_create_request.text)
get_or_create_request = requests.post(base_url + operation, data=payload)
print(get_or_create_request.text)
payload['repospec_token'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXBvIjoicG9zdGdyZXNxbC1jb2RlLWV4ZWN1dG9yLXRlbXB' \
                            'sYXRlIn0.cvJgNebtviihNa-rAE74g9begUypZ5qpX8_CcP2XSm4'
get_or_create_request = requests.post(base_url + operation, data=payload)
print(get_or_create_request.text)
parent = 'shell-code-executor-template'
print(payload)
del payload['repospec_token']
print(payload)
operation = "edit"
edit_request = requests.post(base_url + operation, data=payload)
print(edit_request.text)
payload['parent'] = parent
edit_request = requests.post(base_url + operation, data=payload)
print(edit_request.text)
payload['regen_secret_key'] = True
print(payload)
edit_request = requests.post(base_url + operation, data=payload)
print(edit_request.text)
