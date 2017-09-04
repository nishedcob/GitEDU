
from ideApp.CodePersistenceBackends.generics import GenericNamespace, GenericRepository, GenericRepositoryFile, CodePersistenceBackend
from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, CODE_PERSISTENCE_BACKEND_READ_PREFERENCE, CODE_PERSISTENCE_BACKEND_WRITE_OUT

class CodePersistenceBackendManager(CodePersistenceBackend):

    code_persistence_backends = {}
    code_persistence_backends_read = []
    code_persistence_backends_write = []

    def __init__(self):
        for backend_key, backend_config in CODE_PERSISTENCE_BACKENDS.items():
            if backend_config['use']:
                connection_profile = backend_config['connection_profiles'][backend_config['connection_profile']]
                self.code_persistence_backends[backend_key] = backend_config['backend'](connection_profile)
        for backend_key in CODE_PERSISTENCE_BACKEND_READ_PREFERENCE:
            connection = self.code_persistence_backends.get(backend_key, None)
            if connection:
                self.code_persistence_backends_read.append({"key": backend_key, "backend": connection})
        for backend_key in CODE_PERSISTENCE_BACKEND_WRITE_OUT:
            connection = self.code_persistence_backends.get(backend_key, None)
            if connection:
                self.code_persistence_backends_write.append({"key": backend_key, "backend": connection})

    def list_namespaces(self, include_read=True, include_write=True):
        namespaces = {}
        if include_read:
            if include_write:
                namespaces['read'] = {}
                for backend in self.code_persistence_backends_read:
                    namespaces['read'][backend['key']] = backend['backend'].list_namespaces()
            else:
                for backend in self.code_persistence_backends_read:
                    namespaces[backend['key']] = backend['backend'].list_namespaces()
        if include_write:
            if include_read:
                namespaces['write'] = {}
                for backend in self.code_persistence_backends_write:
                    namespaces['write'][backend['key']] = backend['backend'].list_namespaces()
            else:
                for backend in self.code_persistence_backends_write:
                    namespaces[backend['key']] = backend['backend'].list_namespaces()
        return namespaces

    def search_namespaces(self, query, include_read=True, include_write=True):
        namespaces = {}
        if include_read:
            if include_write:
                namespaces['read'] = {}
                for backend in self.code_persistence_backends_read:
                    namespaces['read'][backend['key']] = backend['backend'].search_namespaces(query)
            else:
                for backend in self.code_persistence_backends_read:
                    namespaces[backend['key']] = backend['backend'].search_namespaces(query)
        if include_write:
            if include_read:
                namespaces['write'] = {}
                for backend in self.code_persistence_backends_write:
                    namespaces['write'][backend['key']] = backend['backend'].search_namespaces(query)
            else:
                for backend in self.code_persistence_backends_write:
                    namespaces[backend['key']] = backend['backend'].search_namespaces(query)
        return namespaces

    def namespace_exists(self, namespace, include_read=True, include_write=True):
        exists = False
        if include_read:
            for backend in self.code_persistence_backends_read:
                exists = exists or backend['backend'].namespace_exists(namespace)
        if include_write:
            for backend in self.code_persistence_backends_write:
                exists = exists or backend['backend'].namespace_exists(namespace)
        return exists

    def get_namespace(self, namespace, include_read=True, include_write=True):
        namespaces = {}
        if include_read:
            if include_write:
                namespaces['read'] = {}
                for backend in self.code_persistence_backends_read:
                    namespaces['read'][backend['key']] = backend['backend'].get_namespace(namespace)
            else:
                for backend in self.code_persistence_backends_read:
                    namespaces[backend['key']] = backend['backend'].get_namespace(namespace)
        if include_write:
            if include_read:
                namespaces['write'] = {}
                for backend in self.code_persistence_backends_write:
                    namespaces['write'][backend['key']] = backend['backend'].get_namespace(namespace)
            else:
                for backend in self.code_persistence_backends_write:
                    namespaces[backend['key']] = backend['backend'].get_namespace(namespace)
        return namespaces

    def create_namespace(self, namespace, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].create_namespace(namespace)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].create_namespace(namespace)

    def delete_namespace(self, namespace, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].delete_namespace(namespace)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].delete_namespace(namespace)

    def save_namespace(self, namespace, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].save_namespace(namespace)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].save_namespace(namespace)

    def list_repositories(self, namespace):
        pass

    def search_repositories(self, namespace):
        pass

    def repository_exists(self, namespace, repository):
        return False

    def get_repository(self, namespace, repository):
        pass

    def create_repository(self, namespace, repository):
        pass

    def delete_repository(self, namespace, repository):
        pass

    def save_repository(self, namespace, repository):
        pass

    def list_files(self, namespace, repository):
        pass

    def search_files(self, namespace, repository):
        pass

    def file_exists(self, namespace, respository, file_path):
        return False

    def get_file(self, namespace, respository, file_path):
        pass

    def create_file(self, namespace, repository, file_path, file_contents):
        pass

    def delete_file(self, namespace, repository, file_path):
        pass

    def save_file(self, namespace, repository, file_path, file_contents):
        pass
