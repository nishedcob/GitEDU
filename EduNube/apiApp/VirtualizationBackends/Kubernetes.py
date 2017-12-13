
from EduNube.settings import DEFAULT_DOCKER_REGISTRY, DEFAULT_DOCKER_TAGS
from apiApp.VirtualizationBackends.Generic import GenericVirtualizationBackend


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

    def create_job(self, repository):
        pass

    def job_get(self, job_id):
        pass

    def job_log(self, job_id):
        pass


class Py3KubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'python3'


class PGSQLKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'postgresql'


class ShellKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):

    executor_name = 'shell'
