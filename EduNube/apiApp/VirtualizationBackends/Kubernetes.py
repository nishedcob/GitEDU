
import subprocess
import json
import pathlib
import os
import re

from EduNube.settings import DEFAULT_DOCKER_REGISTRY, DEFAULT_DOCKER_TAGS
from apiApp.VirtualizationBackends.Generic import GenericVirtualizationBackend
from apiApp.Validation import RepoSpec


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
        return DEFAULT_DOCKER_REGISTRY.get('base', 'registry.gitlab.com')

    def get_docker_registry_user(self):
        return DEFAULT_DOCKER_REGISTRY.get('user', 'nishedcob')

    def get_docker_registry_repo(self):
        return '%s/%s' % (self.get_docker_registry_user(), DEFAULT_DOCKER_REGISTRY.get('repository', 'gitedu'))

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

    def run_command(self, command, cwd=None):
        if cwd is None:
            cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        return self.format_command_result(command_proc=cmd)

    def get_repospec(self, repository):
        # TODO: request GET git_domain?p=repo w/o domain;a=blob_plain;f=.repospec;hb=HEAD
        # TODO: if request == 404 raise error
        # TODO: return request text
        pass

    def clone_or_pull(self, repository):
        # TODO: test for repo in temp folder
        # TODO:     if is git repo:
        # TODO:         git checkout
        # TODO:         git clean
        # TODO:         git pull
        # TODO:         on success:
        # TODO:             return repo path
        # TODO:         on failure:
        # TODO:             rm -rdf repo path
        # TODO:     else:
        # TODO:         rm -rdf repo path
        # TODO: clone repository in temp folder
        # TODO: return repo path
        pass

    def build_edunube_ignore(self, repo_path, full_ignore_path, parent_repo_path):
        # TODO: if parent_repo_path is None then copy repo_path/.edunubeignore -> full_ignore_path & return
        # TODO: test for existence of file parent_repo_path.edunubeignore
        # TODO: if doesn't exist generate recursively
        # TODO: concat repo_path/.edunubeignore and parent_repo_path.edunubeignore as full_ignore_path.unsorted
        # TODO: sort full_ignore_path.unsorted as full_ignore_path.sorted and rm full_ignore_path.unsorted
        # TODO: uniq full_ignore_path.sorted as full_ignore_path and rm full_ignore_path.sorted
        pass

    def repo_sync(self, origin_repo, dest_repo, ignore):
        # TODO: rsync -a origin_repo/ dest_repo/ --ignore-from ignore
        pass

    def build_exec_repo(self, repository, path):
        if repository is None:
            return None
        if type(repository) == list:
            for repo in repository:
                self.build_exec_repo(repository=repo, path=path)
        repospec = self.get_repospec(repository=repository)
        RepoSpec.validate_repospec(repospec=repospec)
        decoded_repospec = RepoSpec.decode(repospec=repospec)
        parent_path = self.build_exec_repo(repository=decoded_repospec.get('parent'), path=path)[0]
        repo_path = self.clone_or_pull(repository=repository)
        edunube_ignore_path = "%s.edunubeignore" % repo_path
        self.build_edunube_ignore(repo_path=repo_path, full_ignore_path=edunube_ignore_path,
                                  parent_repo_path=parent_path)
        self.repo_sync(origin_repo=repo_path, dest_repo=path, ignore=edunube_ignore_path)
        return repo_path, path

    def always_deterministic(self):
        return False

    def is_deterministic(self, namespace, repository, repository_url):
        # TODO: look for job with default name
        # TODO: if job does not exist, execute with default name
        # TODO: look for job with secondary name
        # TODO: if secondary name job doesn't exist, re-execute with second name
        # TODO: compare logs, if == return true, else return false
        pass

    commit_id_regex = re.compile("commit ([0-9a-f]*)\\\\n")

    def get_id_last_git_commit(self, repository_path):
        command = ["git", "show", "HEAD"]
        cmd = self.run_command(command=command, cwd=repository_path)
        return self.commit_id_regex.findall(str(cmd[0]))[0]

    def create_job(self, namespace, repository, repository_url):
        unique_name = "%s-%s" % (namespace, repository)
        unique_path = "%s/%s" % (self.get_tmp_repo_path(), unique_name)
        self.build_exec_repo(repository=repository_url, path=unique_path)
        # TODO: create new repo & commit built exec repo & push to remote repo
        exec_repo_url = ''
        commit_id = self.get_id_last_git_commit(repository_path=unique_path)
        job_name = "%s-%s" % (unique_name, commit_id)
        if self.always_deterministic():
            job_status = self.job_status(job_id=job_name)
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
            if self.is_deterministic(namespace=namespace, repository=repository, repository_url=repository_url):
                # TODO: return log
                pass
            else:
                # TODO: re-execute and return execution in progress
                pass
            pass
        # TODO: build template and call kubernetes
        # TODO: return job id and log
        pass

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
        return self.kubectl__job_id(verb='describe', job_id=job_id)

    def job_get(self, job_id):
        return self.kubectl__job_id(verb='get', job_id=job_id)

    def job_logs(self, job_id):
        return self.kubectl__job_id(verb='logs', job_id=job_id)

    executing_regex = re.compile("  0  ")

    def job_status(self, job_id):
        get_job = self.job_get(job_id=job_id)
        status = {
            'exists': False
        }
        if get_job[2] == 0:
            status['exists'] = True
            get_job_str = str(get_job[0])
            status['finished'] = self.executing_regex.search(get_job_str) is None
        return status

    def job_exists(self, job_id):
        return self.job_status(job_id=job_id).get('exists')

    def job_finished(self, job_id):
        return self.job_status(job_id=job_id).get('finished')


class Py3KubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'python3'


class PGSQLKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'postgresql'

    def always_deterministic(self):
        return True


class ShellKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'shell'
