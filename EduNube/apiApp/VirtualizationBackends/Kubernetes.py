
from apiApp.VirtualizationBackends.Generic import GenericVirtualizationBackend


class KubernetesVirtualizationBackend(GenericVirtualizationBackend):
    pass


class Py3KubernetesVirtualizationBackend(KubernetesVirtualizationBackend):
    pass


class PGSQLKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):
    pass


class ShellKubernetesVirtualizationBackend(KubernetesVirtualizationBackend):
    pass
