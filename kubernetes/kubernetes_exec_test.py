# coding: utf-8

import time

from apiApp.VirtualizationBackends.Kubernetes import Py3KubernetesVirtualizationBackend

# values for test:
kvb = Py3KubernetesVirtualizationBackend()
job_name = 'py3-pytest-3'
git_repo = 'https://gitlab.com/nishedcob/python3-code-executor-template.git'
kubernetes_working_tmp_dir = '/tmp'

# prepare test manifest
manifest = kvb.build_job_template(job_name=job_name, git_repo=git_repo)
manifest_path = '%s/%s.json' % (kubernetes_working_tmp_dir, job_name)
kvb.write_json_manifest(path=manifest_path, json_data=manifest, overwrite=True)

# create job with manifest
print(kvb.job_status(job_id=job_name))
print(kvb.kubectl_create_from_manifest_file(manifest_path=manifest_path))

# job info
print(kvb.job_describe(job_id=job_name))

# get job status & wait until job completion
print(kvb.job_get(job_id=job_name))
while not kvb.job_finished(job_id=job_name):
    print(kvb.job_status(job_id=job_name))
    time.sleep(1)
print(kvb.job_status(job_id=job_name))
print(kvb.job_get(job_id=job_name))

# job info
print(kvb.job_describe(job_id=job_name))

# job output
print(kvb.job_logs(job_id=job_name))

# delete job
print(kvb.kubectl_delete_from_manifest_file(manifest_path=manifest_path))
