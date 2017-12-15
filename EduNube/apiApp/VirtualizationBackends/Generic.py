
from EduNube.settings import VIRTUALIZATION_BACKEND_TMP_PATHS, VIRTUALIZATION_BACKEND_MANIFEST_SUBPATH,\
    VIRTUALIZATION_BACKEND_REPO_SUBPATH

class GenericVirtualizationBackend:

    path_class = 'generic'

    def get_tmp_base_path(self):
        path = VIRTUALIZATION_BACKEND_TMP_PATHS.get(self.path_class)
        if path is None:
            path = VIRTUALIZATION_BACKEND_TMP_PATHS.get('default')
        if path is None:
            path = VIRTUALIZATION_BACKEND_TMP_PATHS.get('base')
        if path is None:
            path = '/tmp'
        return path

    def get_tmp_repo_path(self):
        return self.get_tmp_base_path() + VIRTUALIZATION_BACKEND_REPO_SUBPATH

    def get_tmp_manifest_path(self):
        return self.get_tmp_base_path() + VIRTUALIZATION_BACKEND_MANIFEST_SUBPATH

    prog_language = None

    def execute(self, repo):
        # TODO: execute repo + return id
        pass

    def status(self, id):
        # TODO: return execution status
        pass

    def result(self, id):
        # TODO: return execution result
        pass
