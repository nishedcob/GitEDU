
import subprocess
import json
import pathlib
import os
import re
import shutil
import requests
import time

from EduNube.settings import DEFAULT_DOCKER_REGISTRY, DEFAULT_DOCKER_TAGS
from apiApp.Aux.Git import build_git_base_http_url, build_git_base_url_ssh
from apiApp.VirtualizationBackends.Generic import GenericVirtualizationBackend
from apiApp.VirtualizationBackends.K8S.AuxProcesses import JobLoggingProcess
from apiApp.Validation import RepoSpec
from apiApp.git_server_http_endpoint import RepositoryGitSrvHTTPEpConsumer
from apiApp import models, mongodb_models


class KubernetesVirtualizationBackend(GenericVirtualizationBackend):

    path_class = 'k8s'

    def __init__(self):
        self.docker_image = self.get_full_docker_image_string()

    kubernetes_job_template = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": "<UNIQUE JOB NAME>"
        },
        "spec": {
            "template": {
                "metadata": {
                    "name": "<UNIQUE JOB NAME>"
                },
                "spec": {
                    "containers": [
                        {
                            "name": "<UNIQUE JOB NAME>",
                            "image": "<DOCKER IMAGE>",
                            "volumeMounts": [
                                {
                                    "mountPath": "/code",
                                    "name": "code-repo"
                                }
                            ]
                        }
                    ],
                    "restartPolicy": "Never",
                    "volumes": [
                        {
                            "name": "code-repo",
                            "gitRepo": {
                                "repository": "<GIT REPOSITORY>",
                                "directory": "."
                            }
                        }
                    ]
                }
            },
            "backoffLimit": 4
        }
    }

    def find_and_replace_data_value(self, in_dict, orig_val, new_val):
        out_dict = in_dict.copy()
        if type(in_dict) == dict:
            for key, val in in_dict.items():
                if val == orig_val:
                    out_dict[key] = new_val
                elif type(val) == dict:
                    out_dict[key] = self.find_and_replace_data_value(in_dict=val, orig_val=orig_val, new_val=new_val)
                elif type(val) == list:
                    out_dict[key] = self.find_and_replace_data_value(in_dict=val, orig_val=orig_val, new_val=new_val)
        elif type(in_dict) == list:
            for idx in range(len(in_dict)):
                val = in_dict[idx]
                if val == orig_val:
                    out_dict[idx] = new_val
                elif type(val) == dict:
                    out_dict[idx] = self.find_and_replace_data_value(in_dict=val, orig_val=orig_val, new_val=new_val)
                elif type(val) == list:
                    out_dict[idx] = self.find_and_replace_data_value(in_dict=val, orig_val=orig_val, new_val=new_val)
        return out_dict

    def find_and_replace_data_values(self, in_dict, translate_dict):
        out_dict = in_dict.copy()
        for orig_val, new_val in translate_dict.items():
            out_dict = self.find_and_replace_data_value(in_dict=out_dict, orig_val=orig_val, new_val=new_val)
        return out_dict

    def build_job_template(self, job_name, git_repo):
        translate_dict = {
            "<UNIQUE JOB NAME>": job_name,
            "<DOCKER IMAGE>": self.build_docker_string(),
            "<GIT REPOSITORY>": git_repo
        }
        return self.find_and_replace_data_values(in_dict=self.kubernetes_job_template, translate_dict=translate_dict)

    executor_name = 'Generic'

    def get_docker_registry(self):
        # External Docker Repository as Default (gitlab.com)
        #return DEFAULT_DOCKER_REGISTRY.get('base', 'registry.gitlab.com')
        # Internal Docker Repository as Default (10.10.10.1:5000)
        return DEFAULT_DOCKER_REGISTRY.get('base', '10.10.10.1:5000')

    def get_docker_registry_user(self):
        return DEFAULT_DOCKER_REGISTRY.get('user', 'nishedcob')

    def get_docker_registry_repo(self):
        # External Docker Repository as Default (gitedu in gitlab.com)
        #repository = DEFAULT_DOCKER_REGISTRY.get('repository', 'gitedu')
        # Internal Docker Repository with Null as Default (10.10.10.1:5000)
        repository = DEFAULT_DOCKER_REGISTRY.get('repository', None)
        if repository is None:
            return '%s' % self.get_docker_registry_user()
        else:
            return '%s/%s' % (self.get_docker_registry_user(), repository)

    def get_full_docker_image_string(self):
        return '%s/%s/%s-executor' % (self.get_docker_registry(), self.get_docker_registry_repo(), self.executor_name)

    docker_tag = DEFAULT_DOCKER_TAGS.get('default', None) if DEFAULT_DOCKER_TAGS.get(executor_name, None) is None\
        else DEFAULT_DOCKER_TAGS.get(executor_name)

    def build_docker_string(self):
        if not self.docker_image:
            raise ValueError('Docker_Image can\'t be None')
        if self.docker_tag:
            return "%s:%s" % (self.docker_image, self.docker_tag)
        return self.docker_image

    def format_command_result(self, command_proc):
        return command_proc.stdout, command_proc.stderr, command_proc.returncode

    def command_string(self, command):
        command_str = ""
        for word in command:
            if command_str != "":
                command_str += " "
            command_str += word
        return command_str

    def run_command(self, command, cwd=None):
        print("CWD = %s" % cwd)
        print("COMMAND = %s" % self.command_string(command))
        if cwd is None:
            cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        return self.format_command_result(command_proc=cmd)

    git_repo_data_extractor = re.compile('(https?://[a-z0-9\.]+)/([-a-zA-Z0-9/]+)\.git')

    def get_repospec(self, repository):
        git_data = self.git_repo_data_extractor.findall(repository)
        git_domain, repo = git_data[0]
        request_url = "%s/?p=%s.git;a=blob_plain;f=.repospec;hb=HEAD" % (git_domain, repo)
        print(request_url)
        repospec_request = requests.get(request_url)
        if repospec_request.status_code == 404:
            raise Exception('Failure to get RepoSpec')
        return repospec_request.text

    def clone_or_pull(self, repository, path):
        path_object = pathlib.Path(path)
        if path_object.exists():
            if not path_object.is_dir():
                os.remove(path)
        os.makedirs(path, self.dir_mode, exist_ok=True)
        command = ['git', 'status']
        git_status = self.run_command(command=command, cwd=path)
        if git_status[2] == 0:
            commands = [
                ['git', 'checkout', '--', '.'],
                ['git', 'clean', '-f'],
                ['git', 'pull', repository, 'master']
            ]
            git_command = None
            failure = False
            for command in commands:
                print(command)
                git_command = self.run_command(command=command, cwd=path)
                print(git_command[0])
                if git_command[2] != 0:
                    print(git_command[1])
                    failure = True
                    break
            if failure:
                command = ['rm', '-rdvf', path]
                cmd = self.run_command(command=command)
                print(cmd[0])
            else:
                return git_command
        command = ['git', 'clone', repository, path]
        return self.run_command(command=command)

    def _concat_files(self, dest, src):
        with open(src, 'r') as src_fd:
            with open(dest, 'a') as dest_fd:
                for line in src_fd:
                    dest_fd.write(line)
                    dest_fd.flush()

    def _build_edunube_ignore(self, repo_path, full_ignore_path, exists_parent=False):
        # Get edunubeignore for current repo
        current_edunube_ignore = repo_path + "/.edunubeignore"
        current_edunube_ignore_path = pathlib.Path(current_edunube_ignore)

        # write out its edunube ignore
        if current_edunube_ignore_path.exists() and current_edunube_ignore_path.is_file():
            if exists_parent:
                # concat internal .edunubeignore to external .edunubeignore seeded from parent .edunubeignore.children
                self._concat_files(src=current_edunube_ignore, dest=full_ignore_path)
            else:
                # use internal .edunubeignore
                shutil.copy(current_edunube_ignore, full_ignore_path)
        else:
            if exists_parent:
                # non existent internal .edunubeignore
                # we don't need to do anything
                pass
            else:
                # no parent so lets write out a blank external .edunubeignore
                with open(full_ignore_path, mode='w') as full_ignore_path_fd:
                    full_ignore_path_fd.write("")

        # Get edunubeignore.children for current repo
        current_edunube_ignore_children = current_edunube_ignore + ".children"
        current_edunube_ignore_children_path = pathlib.Path(current_edunube_ignore_children)

        # edunubeignore.children path
        full_ignore_path_children = full_ignore_path + ".children"

        if current_edunube_ignore_children_path.exists() and current_edunube_ignore_children_path.is_file():
            # copy edunubeignore.children out of repo
            shutil.copy(current_edunube_ignore_children, full_ignore_path_children)

            # copy lines from external edunubeignore into external edunubeignore.children
            self._concat_files(src=full_ignore_path, dest=full_ignore_path_children)
        else:
            # copy external edunubeignore to edunubeignore.children
            shutil.copy(full_ignore_path, full_ignore_path_children)

    build_edunube_ignore_called_params = set()
    build_edunube_ignore_called_params_2 = set()

    def build_edunube_ignore(self, repo_path, full_ignore_path, recursive_call=False):
        # Recursive loop protection
        called_params_dict = {
            'repo_path': repo_path,
            'full_ignore_path': full_ignore_path,
        }
        called_params = "{%s}" % "'repo_path': \"{repo_path}\", 'full_ignore_path': \"{full_ignore_path}\""\
            .format_map(called_params_dict)
        print(called_params)
        if called_params in self.build_edunube_ignore_called_params:
            if called_params in self.build_edunube_ignore_called_params_2:
                print("Recursive loop detected on build_edunube_ignore! Cutting loop now...")
                self.build_edunube_ignore_called_params.remove(called_params)
                self.build_edunube_ignore_called_params_2.remove(called_params)
                return
            self.build_edunube_ignore_called_params_2.add(called_params)
        else:
            self.build_edunube_ignore_called_params.add(called_params)

        # get repospec for current repo
        current_edunube_repospec = repo_path + "/.repospec"
        current_edunube_repospec_path = pathlib.Path(current_edunube_repospec)

        if current_edunube_repospec_path.exists() and current_edunube_repospec_path.is_file():
            with open(current_edunube_repospec, mode='r') as repospec_fd:
                repospec_data = repospec_fd.read()
            decoded_repospec = RepoSpec.decode_repospec(repospec=repospec_data)
            parent_repository = decoded_repospec.get('parent_repo')
        else:
            raise ValueError("Problem reading repository's repospec")

        # if no parent repo:
        if parent_repository is None:
            self._build_edunube_ignore(repo_path=repo_path, full_ignore_path=full_ignore_path, exists_parent=False)
        else:   # if has parent repo
            parent_repository_name = self.extract_repo_name.findall(parent_repository)[0]
            parent_repo_path = self.get_tmp_repo_path() + "/" + parent_repository_name
            parent_repo_edunube_ignore = parent_repo_path + ".edunubeignore"
            self.clone_or_pull(repository=parent_repository, path=parent_repo_path)
            # recursively build edunube ignore of parent repo
            self.build_edunube_ignore(repo_path=parent_repo_path, full_ignore_path=parent_repo_edunube_ignore)
            # edunubeignore.children for parent repo
            parent_repo_edunube_ignore_children = parent_repo_edunube_ignore + ".children"
            # copy parent repo edunubeignore.children as seed for current edunubeignore
            shutil.copy(parent_repo_edunube_ignore_children, full_ignore_path)

            # Get edunubeignore for current repo
            self._build_edunube_ignore(repo_path=repo_path, full_ignore_path=full_ignore_path, exists_parent=True)

        # Sort and Uniq on .edunubeignore
        cmd = ['sort', full_ignore_path, ">", "%s.sorted" % full_ignore_path]
        command = self.run_command(command=cmd)
        command_results = list(command)
        if command[2] == 0:
            command_results = [command[0], command[1], command[2]]
            cmd = ['rm', full_ignore_path]
            command = self.run_command(command=cmd)
            command_results[0] += command[0]
            command_results[1] += command[1]
            command_results[2] += command[2]
            if command[2] == 0:
                cmd = ['uniq', "%s.sorted" % full_ignore_path, ">", full_ignore_path]
                command = self.run_command(command=cmd)
                command_results[0] += command[0]
                command_results[1] += command[1]
                command_results[2] += command[2]
        print(command_results)

        # edunubeignore.children path
        full_ignore_path_children = full_ignore_path + ".children"

        # Sort and Uniq on .edunubeignore
        cmd = ['sort', full_ignore_path_children, ">", "%s.sorted" % full_ignore_path_children]
        command = self.run_command(command=cmd)
        command_results[0] += command[0]
        command_results[1] += command[1]
        command_results[2] += command[2]
        if command[2] == 0:
            command_results = [command[0], command[1], command[2]]
            cmd = ['rm', full_ignore_path_children]
            command = self.run_command(command=cmd)
            command_results[0] += command[0]
            command_results[1] += command[1]
            command_results[2] += command[2]
            if command[2] == 0:
                cmd = ['uniq', "%s.sorted" % full_ignore_path_children, ">", full_ignore_path_children]
                command = self.run_command(command=cmd)
                command_results[0] += command[0]
                command_results[1] += command[1]
                command_results[2] += command[2]
        print(command_results)

        return command_results

    def repo_sync(self, origin_repo, dest_repo, ignore):
        command = ['rsync', '-a', "%s/" % origin_repo, dest_repo, '--exclude-from', ignore, '--exclude=".git"']
        return self.run_command(command=command)

    extract_ns_name = re.compile("[hf]t?tps?://[a-zA-Z0-9-_\.]+/([a-zA-Z0-9-_]+)?/[a-zA-Z0-9-_]+\.git")
    extract_repo_name = re.compile("/([a-zA-Z0-9-_]+)\.git$")

    def build_exec_repo(self, repository, repo_path):
        if repository is None:
            return None
        if type(repository) == list:
            for repo in repository:
                self.build_exec_repo(repository=repo, repo_path=repo_path)
        repospec = self.get_repospec(repository=repository)
        RepoSpec.validate_repospec(repospec=repospec)
        decoded_repospec = RepoSpec.decode(repospec=repospec)
        parent_path = self.build_exec_repo(repository=decoded_repospec.get('parent_repo'), repo_path=repo_path)
        namespace_name = self.extract_ns_name.findall(repository)
        print(namespace_name)
        if namespace_name is not None and type(namespace_name) == list and len(namespace_name) > 0:
            namespace_name = namespace_name[0]
        else:
            namespace_name = None
        repository_name = self.extract_repo_name.findall(repository)[0]
        current_repo_path = self.get_tmp_repo_path() + "/"
        if namespace_name is not None:
            current_repo_path += namespace_name + "/"
            os.makedirs(current_repo_path, self.dir_mode, exist_ok=True)
        current_repo_path += repository_name
        self.clone_or_pull(repository=repository, path=current_repo_path)
        edunube_ignore_path = "%s.edunubeignore" % current_repo_path
        self.build_edunube_ignore(repo_path=current_repo_path, full_ignore_path=edunube_ignore_path)
        cmd = self.repo_sync(origin_repo=current_repo_path, dest_repo=repo_path, ignore=edunube_ignore_path)
        print(cmd)
        return repo_path

    def always_deterministic(self):
        return False

    def always_execute(self):
        return False

    def build_new_name(self, name, index):
        return "%s-%d" % (name, index)

    def is_deterministic(self, namespace, repository, repository_url, unique_path, unique_name):
        commit_id = self.get_id_last_git_commit(repository_path=unique_path)
        job_name = self.build_job_name(unique_name=unique_name, commit_id=commit_id)
        try:
            jobSpec = models.JobSpec.objects.get(job_name=job_name)
        except models.JobSpec.DoesNotExist:
            jobSpec = None
        if jobSpec is not None:
            if jobSpec.deterministic is not None:
                return jobSpec.deterministic
            # executed at least once but determism not determined
            job_name_2 = self.build_new_name(name=job_name, index=2)
            try:
                jobSpec2 = models.JobSpec.objects.get(job_name=job_name_2)
            except models.JobSpec.DoesNotExist:
                jobSpec2 = None
            executed = False
            if jobSpec2 is not None:
                if jobSpec2.deterministic is not None:
                    # determism determined previously, database not in sync
                    jobSpec.deterministic = jobSpec2.deterministic
                    jobSpec.save()
                    return jobSpec2.deterministic
            else:
                # execute once with second name
                self.execute_job(namespace=namespace, repository=repository, repository_url=repository_url,
                                 repository_path=unique_path, job_name=job_name_2, prep_job=True)
                executed = True
                jobSpec2 = models.JobSpec.objects.get(job_name=job_name_2)
            job1_status = self.job_status(job_id=job_name)
            job2_status = self.job_status(job_id=job_name_2)
            while not job1_status.get("finished"):
                time.sleep(1)
                job1_status = self.job_status(job_id=job_name)
            while not job2_status.get("finished"):
                time.sleep(1)
                job2_status = self.job_status(job_id=job_name_2)
            params_dict = {
                'namespace': namespace,
                'repository': repository,
                'commit_id': commit_id
            }
            log1_params = params_dict.copy()
            log1_params['execution_number'] = "1"
            log1_id = mongodb_models.ExecutionLogModel.calc_uniq_combo(**log1_params)
            try:
                executionLog1 = mongodb_models.ExecutionLogModel.objects.get({'_id': log1_id})
                print("found log 1")
            except mongodb_models.ExecutionLogModel.DoesNotExist:
                executionLog1 = None
            while executionLog1 is None:
                time.sleep(1)
                try:
                    executionLog1 = mongodb_models.ExecutionLogModel.objects.get({'_id': log1_id})
                    print("found log 1")
                except mongodb_models.ExecutionLogModel.DoesNotExist:
                    executionLog1 = None
            print(executionLog1)
            log2_params = params_dict.copy()
            log2_params['execution_number'] = "2"
            log2_id = mongodb_models.ExecutionLogModel.calc_uniq_combo(**log2_params)
            try:
                executionLog2 = mongodb_models.ExecutionLogModel.objects.get({'_id': log2_id})
                print("found log 2")
            except mongodb_models.ExecutionLogModel.DoesNotExist:
                executionLog2 = None
            while executionLog2 is None:
                time.sleep(2)
                try:
                    executionLog2 = mongodb_models.ExecutionLogModel.objects.get({'_id': log2_id})
                    print("found log 2")
                except mongodb_models.ExecutionLogModel.DoesNotExist:
                    executionLog2 = None
            print(executionLog2)
            if executionLog1.stdout == executionLog2.stdout and executionLog1.stderr == executionLog2.stderr:
                jobSpec.deterministic = True
                jobSpec2.deterministic = True
            else:
                jobSpec.deterministic = False
                jobSpec2.deterministic = False
            jobSpec.save()
            jobSpec2.save()
            if executed:
                return None, None
            else:
                return jobSpec.deterministic
        else:
            # never executed, execute once and return none
            # execute once with default name
            self.execute_job(namespace=namespace, repository=repository, repository_url=repository_url,
                             repository_path=unique_path, job_name=job_name, prep_job=True)
            return None

    commit_id_regex = re.compile("commit ([0-9a-f]*)\\\\n")

    def commit_repo(self, repository_path, message='Commit by EduNube', from_func=None, last_exit_code=None):
        command = ["git", "commit", "-m", "'%s'" % message]
        cmd = self.run_command(command=command, cwd=repository_path)
        if cmd[2] != 0:
            if last_exit_code != 128 and cmd[2] == 128:
                git_config_template = ['git', 'config']
                git_config_global_template = git_config_template.copy()
                git_config_global_template.append('--global')
                git_config_email = git_config_global_template.copy()
                git_config_email.append("user.email")
                git_config_email.append('"python3@uwsgi.app.server"')
                git_config_name = git_config_global_template.copy()
                git_config_name.append("user.name")
                git_config_name.append('"Python 3 uWSGI"')
                commit_cmd = cmd
                for git_config_cmd in [git_config_email, git_config_name]:
                    cmd = self.run_command(command=git_config_cmd, cwd=repository_path)
                    if cmd[2] != 0:
                        print(git_config_cmd)
                        print("stdout: '''\n%s\n'''" % cmd[0])
                        print("stderr: '''\n%s\n'''" % cmd[1])
                return self.commit_repo(repository_path=repository_path, message=message, from_func=from_func,
                                        last_exit_code=commit_cmd[2])
                # git config --global user.email "you@example.com"
                # git config --global user.name "Your Name"
            raise ValueError("Failure to commit '%s'" % repository_path)

    def get_id_last_git_commit(self, repository_path, recursive_call=False):
        command = ["git", "show", "HEAD"]
        cmd = self.run_command(command=command, cwd=repository_path)
        if cmd[2] != 0:
            if not recursive_call:
                self.commit_repo(repository_path=repository_path, from_func=self.get_id_last_git_commit)
                return self.get_id_last_git_commit(repository_path=repository_path, recursive_call=True)
            else:
                raise ValueError("Recursive loop in get_id_last_git_commit('%s')" % repository_path)
            # Previously:
            # # No commits yet?
            # return None
        return self.commit_id_regex.findall(str(cmd[0]))[0]

    def build_unique_name(self, namespace, repository):
        return "%s-%s" % (namespace, repository)

    def build_job_name(self, unique_name, commit_id):
        if commit_id is None:
            return unique_name
        return "%s-%s" % (unique_name, commit_id)

    def build_full_job_name(self, namespace, repository, commit_id):
        return "%s-%s" % (self.build_unique_name(namespace=namespace, repository=repository), commit_id)

    def build_git_base_url(self):
        return build_git_base_http_url()

    def prepare_job(self, namespace, repository, repository_url):
        unique_name = self.build_unique_name(namespace=namespace, repository=repository)
        unique_path = "%s/%s" % (self.get_tmp_repo_path(), unique_name)
        self.build_exec_repo(repository=repository_url, repo_path=unique_path)
        unique_backup_path = "%s/%s" % (self.get_tmp_backup_repo_path(), unique_name)
        command = ['rsync', '-av', '--progress', unique_path, unique_backup_path, '--exclude=".git"']
        cmd = self.run_command(command=command)
        if cmd[2] == 0:
            command = ['rm', '-rdfv', unique_path]
            cmd = self.run_command(command=command)
        remote_namespace = self.get_remote_execution_namespace()
        git_exec_repo_url = "%s/%s/%s.git" % (self.build_git_base_url(), remote_namespace, unique_name)
        print(git_exec_repo_url)
        print(unique_path)
        command = ['git', 'clone', git_exec_repo_url, unique_path]
        cmd = self.run_command(command=command)
        not_cloned = False
        if cmd[2] != 0:
            # Failure to clone
            os.makedirs(unique_path, self.dir_mode, exist_ok=True)
            not_cloned = True
        command = ['rsync', '-av', '--progress', unique_backup_path, unique_path, '--exclude=".git"']
        cmd = self.run_command(command=command)
        if not_cloned:
            command = ['git', 'init']
            cmd = self.run_command(command=command, cwd=unique_path)
            command = ['git', 'remote', 'add', 'origin', git_exec_repo_url]
            cmd = self.run_command(command=command, cwd=unique_path)
            repoGitSrvHTTPepConsumer = RepositoryGitSrvHTTPEpConsumer()
            repoGitSrvHTTPepConsumer.create_call(namespace=remote_namespace, repository=unique_name)
        command = ['git', 'add', '.']
        cmd = self.run_command(command=command, cwd=unique_path)
        command = ['git', 'commit', '-m', '"Update to Exec Repo"']
        cmd = self.run_command(command=command, cwd=unique_path)
        git_ssh_url = "%s/%s/%s.git" % (self.build_git_base_url_ssh('bare'), remote_namespace, unique_name)
        command = ['git', 'remote', 'add', 'save', git_ssh_url]
        cmd = self.run_command(command=command, cwd=unique_path)
        command = ['git', 'push', 'save', 'master']
        cmd = self.run_command(command=command, cwd=unique_path)
        #print(cmd)
        exec_repo_url = git_exec_repo_url
        return {
            'unique_name': unique_name,
            'unique_path': unique_path,
            'exec_repo_url': exec_repo_url
        }

    def execute_job(self, namespace, repository, repository_url, job_name, repository_path=None, prep_job=False,
                    overwrite_manifest=False):
        if prep_job and repository_path is None:
            raise ValueError('Repository_Path can\'t be None if Prep_Job is True')
        if not prep_job:
            prep_job = self.prepare_job(namespace=namespace, repository=repository, repository_url=repository_url)
            job_name = prep_job.get('unique_name')
            repository_path = prep_job.get('unique_path')
            repository_url = prep_job.get('exec_repo_url')
        try:
            job_spec = models.JobSpec.objects.get(job_name=job_name)
        except models.JobSpec.DoesNotExist:
            job_spec = None
        existed_previously = job_spec is not None
        manifest = self.build_job_template(job_name=job_name, git_repo=repository_url)
        manifest_path = "%s/%s.json" % (self.get_tmp_base_path(), job_name)
        self.write_json_manifest(path=manifest_path, json_data=manifest, overwrite=overwrite_manifest)
        self.kubectl_create_from_manifest_file(manifest_path=manifest_path)
        job_spec = models.JobSpec.objects.get_or_create(job_name=job_name)[0]
        job_spec.docker_image = self.build_docker_string()
        job_spec.git_repo = repository_url
        job_spec.deterministic = None
        job_spec.save()
        commit_id = self.get_id_last_git_commit(repository_path=repository_path)
        orig_job_name = self.build_full_job_name(namespace=namespace, repository=repository, commit_id=commit_id)
        if not existed_previously:
            job_count = models.JobNameCounter.objects.get_or_create(orig_job_name=orig_job_name)[0]
            job_count.job_count += 1
            job_count.save()
        else:
            job_count = models.JobNameCounter.objects.get(orig_job_name=orig_job_name)
        jlp = JobLoggingProcess(virt_backend=self, job_id=job_name, namespace=namespace, repository=repository,
                                commit_id=commit_id, execution_number=job_count.job_count)
        jlp.start()
        self.processes.append(jlp)

    def create_job(self, namespace, repository, repository_url):
        prep_job = self.prepare_job(namespace=namespace, repository=repository, repository_url=repository_url)
        unique_name = prep_job.get('unique_name')
        unique_path = prep_job.get('unique_path')
        exec_repo_url = prep_job.get('exec_repo_url')
        commit_id = self.get_id_last_git_commit(repository_path=unique_path)
        job_name = self.build_job_name(unique_name=unique_name, commit_id=commit_id)
        if self.always_execute():
            job_status = self.job_status(job_id=job_name)
            if job_status.get('exists'):
                self.job_delete(job_id=job_name)
            self.execute_job(namespace=namespace, repository=repository, repository_url=exec_repo_url,
                             repository_path=unique_path, job_name=job_name, prep_job=True)
            return {
                'id': job_name
            }
        else:
            if self.always_deterministic():
                job_status = self.job_status(job_id=job_name)
                job_status['id'] = job_name
                if job_status.get('exists'):
                    if job_status.get('finished'):
                        job_status['log'] = self.job_logs(job_id=job_name)
                else:
                    manifest = self.build_job_template(job_name=job_name, git_repo=exec_repo_url)
                    manifest_path = self.get_tmp_manifest_path() + "/" + job_name + ".json"
                    self.write_json_manifest(path=manifest_path, json_data=manifest, overwrite=True)
                    self.kubectl_create_from_manifest_file(manifest_path=manifest_path)
                    job_status = self.job_status(job_id=job_name)
                return job_status
            else:
                determinism = self.is_deterministic(namespace=namespace, repository=repository,
                                                    repository_url=exec_repo_url, unique_path=unique_path,
                                                    unique_name=unique_name)
                if determinism is None:
                    job_status = self.job_status(job_id=job_name)
                    job_status['id'] = job_name
                    job_status['log'] = self.job_logs(job_id=job_name)
                    return job_status
                elif type(determinism) == tuple and determinism == (None, None):
                    job_name = self.build_new_name(name=job_name, index=2)
                    job_status = self.job_status(job_id=job_name)
                    job_status['id'] = job_name
                    job_status['log'] = self.job_logs(job_id=job_name)
                    return job_status
                elif type(determinism) == bool:
                    if determinism:
                        job_status = self.job_status(job_id=job_name)
                        job_status['exec_log'] = self.job_logs(job_id=job_name)
                        return job_status
                    else:
                        job_counter = models.JobNameCounter.objects.get(orig_job_name=job_name)
                        if job_counter is None:
                            job_counter = models.JobNameCounter(job_name=job_name, job_count=0)
                            jobs = models.JobSpec.objects.filter(job_name__startswith=job_name)
                            job_counter.job_count = jobs.count()
                            job_counter.save()
                        job_counter.job_count += 1
                        job_counter.save()
                        job_name = self.build_new_name(name=job_name, index=job_counter.job_count)
                        self.execute_job(namespace=namespace, repository=repository, repository_url=exec_repo_url,
                                         repository_path=unique_path, job_name=job_name, prep_job=True)
                        return {
                            'id': job_name
                        }
                else:
                    raise ValueError("Invalid or Unimplemented Response from is_deterministic: %s" % determinism)

    def write_json_manifest(self, path, json_data, overwrite=False):
        file_path = pathlib.Path(path)
        if overwrite:
            if file_path.exists() and not file_path.is_file():
                if file_path.is_dir():
                    os.rmdir(path)
                else:
                    os.remove(path)
        else:
            if file_path.exists():
                raise ValueError("Path %s already exists and we don't have permision to overwrite!" % path)
        with open(path, mode='w') as json_manifest:
            json_manifest.write(json.dumps(json_data))

    def kubectl__manifest_file(self, verb, manifest_path):
        command = ['kubectl', verb, '-f', manifest_path]
        return self.run_command(command=command)

    def kubectl_create_from_manifest_file(self, manifest_path):
        return self.kubectl__manifest_file(verb='create', manifest_path=manifest_path)

    def kubectl_delete_from_manifest_file(self, manifest_path):
        return self.kubectl__manifest_file(verb='delete', manifest_path=manifest_path)

    def kubectl__job_id(self, verb, job_id):
        command = ['kubectl', verb, 'job/%s' % job_id]
        return self.run_command(command=command)

    def job_describe(self, job_id):
        response = {
            'id': job_id,
            'logs': self.kubectl__job_id(verb='describe', job_id=job_id)
        }
        return response

    def job_get(self, job_id):
        response = {
            'id': job_id,
            'logs': self.kubectl__job_id(verb='get', job_id=job_id)
        }
        return response

    def job_logs(self, job_id):
        response = {
            "id": job_id,
            "logs": self.kubectl__job_id(verb='logs', job_id=job_id)
        }
        return response

    def job_delete(self, job_id):
        response = {
            "id": job_id,
            "logs": self.kubectl__job_id(verb='delete', job_id=job_id)
        }
        return response

    executing_regex = re.compile("  0  ")

    def job_status(self, job_id):
        get_job = self.job_get(job_id=job_id).get("logs")
        status = {
            'id': job_id,
            'exists': False
        }
        if get_job[2] == 0:
            status['exists'] = True
            get_job_str = str(get_job[0])
            status['finished'] = self.executing_regex.search(get_job_str) is None
        status['logs'] = get_job
        return status

    def job_exists(self, job_id):
        return self.job_status(job_id=job_id).get('exists')

    def job_finished(self, job_id):
        return self.job_status(job_id=job_id).get('finished')

    def execute(self, namespace, repository, repository_url):
        return self.create_job(namespace=namespace, repository=repository, repository_url=repository_url)

    def status(self, id):
        return self.job_status(job_id=id)

    def result(self, id):
        return self.job_logs(job_id=id)

    def build_git_base_url_ssh(self, repo_type):
        return build_git_base_url_ssh(repo_type=repo_type)


class Py3KubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'python3'


class PGSQLKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'postgresql'

    def always_deterministic(self):
        return True


class ShellKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'shell'
