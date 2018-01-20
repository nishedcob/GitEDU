
import time
import datetime
from multiprocessing import Process

#from apiApp.VirtualizationBackends.Kubernetes import KubernetesVirtualizationBackend


class JobLoggingProcess(Process):

    virt_backend = None     # KubernetesVirtualizationBackend()
    pause = 5
    job_id = None
    namespace = None
    repository = None
    commit_id = None
    execution_number = None
    execution_time = None

    def __init__(self, virt_backend, job_id, namespace, repository, commit_id, execution_number, execution_time=None,
                 pause=5):
        super().__init__()
        self.virt_backend = virt_backend
        self.job_id = job_id
        self.namespace = namespace
        self.repository = repository
        self.commit_id = commit_id
        self.execution_number = execution_number
        if execution_time is None:
            self.execution_time = datetime.datetime.now()
        if pause is not None:
            self.pause = pause

    def run(self):
        from apiApp.mongodb_models import ExecutionLogModel
        if self.job_id is not None:
            status = self.virt_backend.status(id=self.job_id)
            if status.get('exists'):
                while not status.get('finished'):
                    time.sleep(self.pause)
                    status = self.virt_backend.status(id=self.job_id)
                params = {
                    'namespace': self.namespace,
                    'repository': self.repository,
                    'commit_id': self.commit_id,
                    'execution_number': self.execution_number
                }
                try:
                    log = ExecutionLogModel.objects.get(params)
                except ExecutionLogModel.DoesNotExist:
                    log = ExecutionLogModel(**params)
                log.execution_time = self.execution_time
                log.stdout = self.virt_backend.result(id=self.job_id)
                log.save()
