# coding: utf-8
import time

from apiApp.VirtualizationBackends.Kubernetes import Py3KubernetesVirtualizationBackend
kvb = Py3KubernetesVirtualizationBackend()
#kvb.prepare_job(namespace='nishedcob', repository='test', repository_url='http://10.10.10.1/nishedcob/test.git')
#kvb.execute_job(namespace='nishedcob', repository='test', repository_url='http://10.10.10.1/nishedcob/test.git',
#                job_name='nishedcob-test')
#kvb.execute_job(namespace='parent', repository='py3-test',
#                repository_url='http://10.10.10.1/python3-code-executor-template.git', job_name='parent-py3-test')
#kvb.execute_job(namespace='nishedcob', repository='py3-parent-test',
#                repository_url='http://10.10.10.1/nishedcob/test.git', job_name='nishedcob-py3-parent-test')
inicial_execution = kvb.create_job(namespace='nishedcob', repository='test',
                                   repository_url='http://10.10.10.1/nishedcob/test.git')
job_id = inicial_execution.get("job_id")
job_status = kvb.status(id=job_id)
while not job_status.get("finished"):
    print(job_status)
    time.sleep(5)
    job_status = kvb.status(id=job_id)
print(kvb.job_logs(job_id=job_id))
second_execution = kvb.create_job(namespace='nishedcob', repository='test',
                                  repository_url='http://10.10.10.1/nishedcob/test.git')
job_id = second_execution.get("job_id")
job_status = kvb.status(id=job_id)
while not job_status.get("finished"):
    print(job_status)
    time.sleep(5)
    job_status = kvb.status(id=job_id)
print(kvb.job_logs(job_id=job_id))
third_execution = kvb.create_job(namespace='nishedcob', repository='test',
                                 repository_url='http://10.10.10.1/nishedcob/test.git')
job_id = third_execution.get("job_id")
job_status = kvb.status(id=job_id)
while not job_status.get("finished"):
    print(job_status)
    time.sleep(5)
    job_status = kvb.status(id=job_id)
print(kvb.job_logs(job_id=job_id))
forth_execution = kvb.create_job(namespace='nishedcob', repository='test',
                                 repository_url='http://10.10.10.1/nishedcob/test.git')
job_id = forth_execution.get("job_id")
job_status = kvb.status(id=job_id)
while not job_status.get("finished"):
    print(job_status)
    time.sleep(5)
    job_status = kvb.status(id=job_id)
print(kvb.job_logs(job_id=job_id))
