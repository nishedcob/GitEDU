
from ideApp.CodePersistenceBackends.generics import CodePersistenceBackend
from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, CODE_PERSISTENCE_BACKEND_READ_PREFERENCE, CODE_PERSISTENCE_BACKEND_WRITE_OUT

class CodePersistenceBackendManager(CodePersistenceBackend):

    code_persistence_backends = {}
    code_persistence_backends_read = []
    code_persistence_backends_write = []

    def __init__(self):
        for backend_key, backend_config in CODE_PERSISTENCE_BACKENDS.items():
            if backend_config['use']:
                connection_profile = backend_config['connection_profiles'][backend_config['connection_profile']]
                backend_class = backend_config['backend']
                #print(backend_class)
                self.code_persistence_backends[backend_key] = backend_class(profile=connection_profile)
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

    def list_repositories(self, namespace, include_read=True, include_write=True):
        repositories = {}
        if include_read:
            if include_write:
                repositories['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories['read'][backend_key] = backend['backend'].list_repositories(namespace)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].list_repositories(namespace)
        if include_write:
            if include_read:
                repositories['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories['write'][backend_key] = backend['backend'].list_repositories(namespace)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].list_repositories(namespace)
        return repositories

    def search_repositories(self, namespace, query, include_read=True, include_write=True):
        repositories = {}
        if include_read:
            if include_write:
                repositories['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories['read'][backend_key] = backend['backend'].search_repositories(namespace, query)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].search_repositories(namespace, query)
        if include_write:
            if include_read:
                repositories['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories['write'][backend_key] = backend['backend'].search_repositories(namespace, query)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].search_repositories(namespace, query)
        return repositories

    def repository_exists(self, namespace, repository, include_read=True, include_write=True):
        exists = False
        if include_read:
            for backend in self.code_persistence_backends_read:
                exists = exists or backend['backend'].repository_exists(namespace, repository)
        if include_write:
            for backend in self.code_persistence_backends_write:
                exists = exists or backend['backend'].repository_exists(namespace, repository)
        return exists

    def get_repository(self, namespace, repository, include_read=True, include_write=True):
        repositories = {}
        if include_read:
            if include_write:
                repositories['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories['read'][backend_key] = backend['backend'].get_repository(namespace, repository)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].get_repository(namespace, repository)
        if include_write:
            if include_read:
                repositories['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories['write'][backend_key] = backend['backend'].get_repository(namespace, repository)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].get_repository(namespace, repository)
        return repositories

    def create_repository(self, namespace, repository, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].create_repository(namespace, repository)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].create_repository(namespace, repository)

    def delete_repository(self, namespace, repository, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].delete_repository(namespace, repository)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].delete_repository(namespace, repository)

    def save_repository(self, namespace, repository, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].save_repository(namespace, repository)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].save_repository(namespace, repository)

    def list_files(self, namespace, repository, include_read=True, include_write=True):
        files = {}
        if include_read:
            if include_write:
                files['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files['read'][backend_key] = backend['backend'].list_files(namespace, repository)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].list_files(namespace, repository)
        if include_write:
            if include_read:
                files['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files['write'][backend_key] = backend['backend'].list_files(namespace, repository)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].list_files(namespace, repository)
        return files

    def search_files(self, namespace, repository, query, include_read=True, include_write=True):
        files = {}
        if include_read:
            if include_write:
                files['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files['read'][backend_key] = backend['backend'].search_files(namespace, repository, query)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].search_files(namespace, repository, query)
        if include_write:
            if include_read:
                files['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files['write'][backend_key] = backend['backend'].search_files(namespace, repository, query)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].search_files(namespace, repository, query)
        return files

    def file_exists(self, namespace, respository, file_path, include_read=True, include_write=True):
        exists = False
        if include_read:
            for backend in self.code_persistence_backends_read:
                exists = exists or backend['backend'].file_exists(namespace, respository, file_path)
        if include_write:
            for backend in self.code_persistence_backends_write:
                exists = exists or backend['backend'].file_exists(namespace, respository, file_path)
        return exists

    def get_file(self, namespace, respository, file_path, include_read=True, include_write=True):
        files = {}
        if include_read:
            if include_write:
                files['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files['read'][backend_key] = backend['backend'].get_file(namespace, respository, file_path)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].get_file(namespace, respository, file_path)
        if include_write:
            if include_read:
                files['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files['write'][backend_key] = backend['backend'].get_file(namespace, respository, file_path)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].get_file(namespace, respository, file_path)
        return files

    def create_file(self, namespace, repository, file_path, file_contents, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].create_file(namespace, repository, file_path, file_contents)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].create_file(namespace, repository, file_path, file_contents)

    def delete_file(self, namespace, repository, file_path, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].delete_file(namespace, repository, file_path)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].delete_file(namespace, repository, file_path)

    def save_file(self, namespace, repository, file_path, file_contents, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].save_file(namespace, repository, file_path, file_contents)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].save_file(namespace, repository, file_path, file_contents)
