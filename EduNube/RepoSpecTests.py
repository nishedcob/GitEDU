# coding: utf-8
from apiApp.Validation import RepoSpec
py3_code_exec_template_repospec = RepoSpec.create(repo="python3-code-executor-template", parent=None)
token = py3_code_exec_template_repospec.token
print(token)
secret_key = py3_code_exec_template_repospec.secret_key
print(secret_key)
py3_code_exec_template_repospec = RepoSpec.RepoSpec.objects.get(repo="python3-code-executor-template")
# token == py3_code_exec_template_repospec.token
# secret_key == py3_code_exec_template_repospec.secret_key
# RepoSpec.validate_repospec(py3_code_exec_template_repospec.token) == True
# RepoSpec.decode_repospec(repospec=py3_code_exec_template_repospec.token,
#                          stored_repospec=py3_code_exec_template_repospec)
#                          == {'repo': "python3-code-executor-template"}
# RepoSpec.decode_repospec(repospec=py3_code_exec_template_repospec.token) == {'repo': "python3-code-executor-template"}
# RepoSpec.decode(stored_repospec=py3_code_exec_template_repospec, repospec=None, decode_stored=True)
#                   == {'repo': "python3-code-executor-template"}
py3_code_exec_template_repospec = RepoSpec.update_repospec(repospec=py3_code_exec_template_repospec,
                                                           parent="http://192.168.1.100/shell.git",
                                                           repo=py3_code_exec_template_repospec.repo,
                                                           regen_secret_key=False)
# token != py3_code_exec_template_repospec.token
# secret_key == py3_code_exec_template_repospec.secret_key
token = py3_code_exec_template_repospec.token
print(token)
secret_key = py3_code_exec_template_repospec.secret_key
print(secret_key)
py3_code_exec_template_repospec = RepoSpec.update_repospec(repospec=py3_code_exec_template_repospec,
                                                           parent="http://192.168.1.100/shell.git",
                                                           repo=py3_code_exec_template_repospec.repo,
                                                           regen_secret_key=True)
# token != py3_code_exec_template_repospec.token
# secret_key != py3_code_exec_template_repospec.secret_key
token = py3_code_exec_template_repospec.token
print(token)
secret_key = py3_code_exec_template_repospec.secret_key
print(secret_key)
# RepoSpec.validate_repospec(repospec=py3_code_exec_template_repospec.token) == True
py3_code_exec_template_repospec = RepoSpec.RepoSpec.objects.get(repo="python3-code-executor-template")
# token == py3_code_exec_template_repospec.token
# secret_key == py3_code_exec_template_repospec.secret_key
token = py3_code_exec_template_repospec.token
print(token)
secret_key = py3_code_exec_template_repospec.secret_key
print(secret_key)
py3_code_exec_template_repospec = RepoSpec.update_repospec(repospec=py3_code_exec_template_repospec, parent=None,
                                                           repo=py3_code_exec_template_repospec.repo,
                                                           regen_secret_key=True)
# token != py3_code_exec_template_repospec.token
# secret_key != py3_code_exec_template_repospec.secret_key
token = py3_code_exec_template_repospec.token
print(token)
secret_key = py3_code_exec_template_repospec.secret_key
print(secret_key)
py3_code_exec_template_repospec = RepoSpec.update_repo(old_repo=py3_code_exec_template_repospec.token)
# token == py3_code_exec_template_repospec.token
# secret key == py3_code_exec_template_repospec.secret_key
py3_code_exec_template_repospec = RepoSpec.update_repo(old_repo=py3_code_exec_template_repospec.token,
                                                       regen_secret_key=True)
# token != py3_code_exec_template_repospec.token
# secret_key != py3_code_exec_template_repospec.secret_key
