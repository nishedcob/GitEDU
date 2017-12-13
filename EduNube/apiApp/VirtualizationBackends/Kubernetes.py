
import subprocess

from EduNube.settings import DEFAULT_DOCKER_REGISTRY, DEFAULT_DOCKER_TAGS
from apiApp.VirtualizationBackends.Generic import GenericVirtualizationBackend
from apiApp.Validation import RepoSpec


class KubernetesVirtualizationBackend(GenericVirtualizationBackend):

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

    docker_image = get_full_docker_image_string()
    docker_tag = DEFAULT_DOCKER_TAGS.get('default', None) if DEFAULT_DOCKER_TAGS.get(executor_name, None) is None\
        else DEFAULT_DOCKER_TAGS.get(executor_name)

    def build_docker_string(self):
        if not self.docker_image:
            raise ValueError('Docker_Image can\'t be None')
        if self.docker_tag:
            return "%s:%s" % (self.docker_image, self.docker_tag)
        return self.docker_image

    def format_command_result(self, command_proc):
        return command_proc.stdout, command_proc.stderr, command_proc.exitcode

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

    def create_job(self, namespace, repository, repository_url):
        unique_path = "%s-%s" % (namespace, repository)
        self.build_exec_repo(repository=repository_url, path=unique_path)
        # TODO: create new repo & commit built exec repo & push to remote repo
        # TODO: build template and call kubernetes
        # TODO: return job id

    def kubectl__job_id(self, verb, job_id):
        command = ['kubectl', verb, 'job/%s' % job_id]
        cmd = subprocess.run(command, stdout=subprocess.PIPE)
        return self.format_command_result(command_proc=cmd)

    def job_describe(self, job_id):
        return self.kubectl__job_id(verb='describe', job_id=job_id)

    def job_get(self, job_id):
        return self.kubectl__job_id(verb='get', job_id=job_id)

    def job_logs(self, job_id):
        return self.kubectl__job_id(verb='logs', job_id=job_id)


class Py3KubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'python3'


class PGSQLKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'postgresql'


class ShellKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'shell'
