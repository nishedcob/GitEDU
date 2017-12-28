# coding: utf-8
from apiApp.VirtualizationBackends.Kubernetes import KubernetesVirtualizationBackend
kvb = KubernetesVirtualizationBackend()
kvb.get_id_last_git_commit(repository_path='/home/nyx/GitEDU')
kvb.get_id_last_git_commit(repository_path='/home/nyx/GitEDU-copy')
