# coding: utf-8
from apiApp.VirtualizationBackends.Kubernetes import KubernetesVirtualizationBackend
kvb = KubernetesVirtualizationBackend()
kvb.prepare_job(namespace='nishedcob', repository='test', repository_url='http://10.10.10.1/nishedcob/test.git')
