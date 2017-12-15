# coding: utf-8
from apiApp.VirtualizationBackends.Kubernetes import Py3KubernetesVirtualizationBackend
kvb = Py3KubernetesVirtualizationBackend()
job_name = 'py3-pytest-3'
git_repo = 'https://gitlab.com/nishedcob/python3-code-executor-template.git'
manifest = kvb.build_job_template(job_name=job_name, git_repo=git_repo)
manifest_path = '/tmp/%s.json' % job_name
kvb.write_json_manifest(path=manifest_path, json_data=manifest)
print(kvb.kubectl_create_from_manifest_file(manifest_path=manifest_path))
print(kvb.job_describe(job_id=job_name))
import re
detect_zero = re.compile(' 0 ')
job_get = kvb.job_get(job_id=job_name)
print(job_get)
job_get_str = str(job_get[0])
import time
while detect_zero.search(job_get_str) is not None:
    time.sleep(1)
    job_get = kvb.job_get(job_id=job_name)
    print(job_get)
    job_get_str = str(job_get[0])
print(kvb.job_describe(job_id=job_name))
print(kvb.job_logs(job_id=job_name))
print(kvb.kubectl_delete_from_manifest_file(manifest_path=manifest_path))
