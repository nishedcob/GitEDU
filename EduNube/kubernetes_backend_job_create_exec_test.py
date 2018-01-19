# coding: utf-8
from apiApp.VirtualizationBackends.Kubernetes import Py3KubernetesVirtualizationBackend
kvb = Py3KubernetesVirtualizationBackend()
#kvb.prepare_job(namespace='nishedcob', repository='test', repository_url='http://10.10.10.1/nishedcob/test.git')
#kvb.execute_job(namespace='nishedcob', repository='test', repository_url='http://10.10.10.1/nishedcob/test.git',
#                job_name='nishedcob-test')
#kvb.execute_job(namespace='parent', repository='py3-test',
#                repository_url='http://10.10.10.1/python3-code-executor-template.git', job_name='parent-py3-test')
kvb.execute_job(namespace='nishedcob', repository='py3-parent-test',
                repository_url='http://10.10.10.1/nishedcob/test.git', job_name='nishedcob-py3-parent-test')
