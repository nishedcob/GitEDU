
import time
import datetime
import importlib

from ideApp.models import BackendType
from ideApp.CodePersistenceBackends.generics import CodePersistenceBackend
from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, CODE_PERSISTENCE_BACKEND_READ_PREFERENCE, CODE_PERSISTENCE_BACKEND_WRITE_OUT

num_cpbm = 0


class CodePersistenceBackendManager(CodePersistenceBackend):

    code_persistence_backends = {}
    code_persistence_backends_read = []
    code_persistence_backends_write = []

    ALIAS_FORMAT = "CPBM_%03d"
    backend_type = BackendType.objects.get_or_create(name="CodePersistenceBackendManager")

    def get_namespace_class(self, include_read=True, include_write=True):
        classes = {}
        if include_read:
            if include_write:
                classes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    classes['read'][backend['key']] = backend['backend'].get_namespace_class()
            else:
                for backend in self.code_persistence_backends_read:
                    classes[backend['key']] = backend['backend'].get_namespace_class()
        if include_write:
            if include_read:
                classes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    classes['write'][backend['key']] = backend['backend'].get_namespace_class()
            else:
                for backend in self.code_persistence_backends_write:
                    classes[backend['key']] = backend['backend'].get_namespace_class()
        return classes

    def get_repository_class(self, include_read=True, include_write=True):
        classes = {}
        if include_read:
            if include_write:
                classes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    classes['read'][backend['key']] = backend['backend'].get_repository_class()
            else:
                for backend in self.code_persistence_backends_read:
                    classes[backend['key']] = backend['backend'].get_repository_class()
        if include_write:
            if include_read:
                classes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    classes['write'][backend['key']] = backend['backend'].get_repository_class()
            else:
                for backend in self.code_persistence_backends_write:
                    classes[backend['key']] = backend['backend'].get_repository_class()
        return classes

    def get_repository_file_class(self, include_read=True, include_write=True):
        classes = {}
        if include_read:
            if include_write:
                classes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    classes['read'][backend['key']] = backend['backend'].get_repository_file_class()
            else:
                for backend in self.code_persistence_backends_read:
                    classes[backend['key']] = backend['backend'].get_repository_file_class()
        if include_write:
            if include_read:
                classes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    classes['write'][backend['key']] = backend['backend'].get_repository_file_class()
            else:
                for backend in self.code_persistence_backends_write:
                    classes[backend['key']] = backend['backend'].get_repository_file_class()
        return classes

    def get_change_class(self, include_read=True, include_write=True):
        classes = {}
        if include_read:
            if include_write:
                classes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    classes['read'][backend['key']] = backend['backend'].get_change_class()
            else:
                for backend in self.code_persistence_backends_read:
                    classes[backend['key']] = backend['backend'].get_change_class()
        if include_write:
            if include_read:
                classes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    classes['write'][backend['key']] = backend['backend'].get_change_class()
            else:
                for backend in self.code_persistence_backends_write:
                    classes[backend['key']] = backend['backend'].get_change_class()
        return classes

    def get_change_file_class(self, include_read=True, include_write=True):
        classes = {}
        if include_read:
            if include_write:
                classes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    classes['read'][backend['key']] = backend['backend'].get_change_file_class()
            else:
                for backend in self.code_persistence_backends_read:
                    classes[backend['key']] = backend['backend'].get_change_file_class()
        if include_write:
            if include_read:
                classes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    classes['write'][backend['key']] = backend['backend'].get_change_file_class()
            else:
                for backend in self.code_persistence_backends_write:
                    classes[backend['key']] = backend['backend'].get_change_file_class()
        return classes

    def __init__(self):
        global num_cpbm
        self.alias = self.ALIAS_FORMAT % num_cpbm
        num_cpbm = num_cpbm + 1
        for backend_key, backend_config in CODE_PERSISTENCE_BACKENDS.items():
            if backend_config['use']:
                connection_profile = backend_config['connection_profiles'][backend_config['connection_profile']]
                backend_class_name = backend_config['backend']
                module_path, class_name = backend_class_name.rsplit('.', 1)
                module = importlib.import_module(module_path)
                backend_class = getattr(module, class_name)
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
        self.load_backend_db_object()

    def __str__(self):
        backend_template = "< %s >"
        write = ""
        for backend in self.code_persistence_backends_write:
            if write != "":
                write += ", "
            write += backend_template % backend['backend']
        read = ""
        for backend in self.code_persistence_backends_read:
            if read != "":
                read += ", "
            read += backend_template % backend['backend']
        return "%s :: {\n\tw: [ %s ]; \n\tr: [ %s ]\n}" % (super(CodePersistenceBackendManager, self).__str__(), write, read)

    def get_preferred_read_backend(self):
        return self.get_preferred_backend(backend_type="read")

    def get_preferred_write_backend(self):
        return self.get_preferred_backend(backend_type="write")

    def get_preferred_backend(self, backend_type="read", not_backend=None):
        if not_backend is None and backend_type is None:
            for key, value in self.code_persistence_backends:
                return key
        if backend_type == "read":
            backend_priority_list = self.code_persistence_backends_read
        elif backend_type == "write":
            backend_priority_list = self.code_persistence_backends_write
        else:
            raise ValueError("Invalid value '%s' for Backend_Type" % backend_type)
        if not_backend is None:
            not_backend = []
        for backend_canidate in backend_priority_list:
            if backend_canidate['key'] not in not_backend:
                return backend_canidate['key']
        return None

    def select_preferred_backend_object(self, result_set=None, backend_type="read", not_backend=None):
        preferred_backend = self.get_preferred_backend(backend_type=backend_type, not_backend=not_backend)
        if result_set is None:
            return None
        if backend_type is not None:
            result_set = result_set.get(backend_type, None)
        if result_set is None:
            return None
        return result_set.get(preferred_backend, None)

    def sync(self, type, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync(type=type)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync(type=type)

    def sync_all(self, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync_all()
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync_all()

    def sync_namespaces(self, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync_namespaces()
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync_namespaces()

    def sync_repositories(self, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync_repositories()
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync_repositories()

    def sync_repository_files(self, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync_repository_files()
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync_repository_files()

    def sync_changes(self, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync_changes()
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync_changes()

    def sync_change_files(self, include_read=True, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].sync_change_files()
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].sync_change_files()

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

    def search_namespaces(self, query, regex=False, include_read=True, include_write=True):
        namespaces = {}
        if include_read:
            if include_write:
                namespaces['read'] = {}
                for backend in self.code_persistence_backends_read:
                    namespaces['read'][backend['key']] = backend['backend'].search_namespaces(query, regex=regex)
            else:
                for backend in self.code_persistence_backends_read:
                    namespaces[backend['key']] = backend['backend'].search_namespaces(query, regex=regex)
        if include_write:
            if include_read:
                namespaces['write'] = {}
                for backend in self.code_persistence_backends_write:
                    namespaces['write'][backend['key']] = backend['backend'].search_namespaces(query, regex=regex)
            else:
                for backend in self.code_persistence_backends_write:
                    namespaces[backend['key']] = backend['backend'].search_namespaces(query, regex=regex)
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

    def search_repositories(self, namespace, query, regex=False, include_read=True, include_write=True):
        repositories = {}
        if include_read:
            if include_write:
                repositories['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories['read'][backend_key] = backend['backend'].search_repositories(namespace, query,
                                                                                               regex=regex)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].search_repositories(namespace, query, regex=regex)
        if include_write:
            if include_read:
                repositories['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories['write'][backend_key] = backend['backend'].search_repositories(namespace, query,
                                                                                                regex=regex)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    repositories[backend_key] = backend['backend'].search_repositories(namespace, query, regex=regex)
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

    def search_files(self, namespace, repository, query, regex=False, include_read=True, include_write=True):
        files = {}
        if include_read:
            if include_write:
                files['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files['read'][backend_key] = backend['backend'].search_files(namespace, repository, query,
                                                                                 regex=regex)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].search_files(namespace, repository, query, regex=regex)
        if include_write:
            if include_read:
                files['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files['write'][backend_key] = backend['backend'].search_files(namespace, repository, query,
                                                                                  regex=regex)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].search_files(namespace, repository, query, regex=regex)
        return files

    def file_exists(self, namespace, repository, file_path, include_read=True, include_write=True):
        exists = False
        if include_read:
            for backend in self.code_persistence_backends_read:
                exists = exists or backend['backend'].file_exists(namespace, repository, file_path)
        if include_write:
            for backend in self.code_persistence_backends_write:
                exists = exists or backend['backend'].file_exists(namespace, repository, file_path)
        return exists

    def get_file(self, namespace, repository, file_path, include_read=True, include_write=True):
        files = {}
        if include_read:
            if include_write:
                files['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files['read'][backend_key] = backend['backend'].get_file(namespace, repository, file_path)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].get_file(namespace, repository, file_path)
        if include_write:
            if include_read:
                files['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files['write'][backend_key] = backend['backend'].get_file(namespace, repository, file_path)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    files[backend_key] = backend['backend'].get_file(namespace, repository, file_path)
        return files

    def create_file(self, namespace, repository, file_path, file_contents, language, include_read=False,
                    include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].create_file(namespace, repository, file_path, file_contents, language)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].create_file(namespace, repository, file_path, file_contents, language)

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

    def save_existent_file(self, namespace, repository, file, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].save_existent_file(namespace, repository, file)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].save_existent_file(namespace, repository, file)

    def list_changes(self, namespace, repository, include_read=True, include_write=True):
        changes = {}
        if include_read:
            if include_write:
                changes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    changes[backend_key] = backend['read']['backend'].list_changes(namespace, repository)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    changes[backend_key] = backend['backend'].list_changes(namespace, repository)
        if include_write:
            if include_read:
                changes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    changes[backend_key] = backend['write']['backend'].list_changes(namespace, repository)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    changes[backend_key] = backend['backend'].list_changes(namespace, repository)
        return changes

    def search_changes(self, namespace, repository, query, regex=False, include_read=True, include_write=True):
        changes = {}
        if include_read:
            if include_write:
                changes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    changes[backend_key] = backend['read']['backend'].search_changes(namespace, repository, query,
                                                                                     regex=regex)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    changes[backend_key] = backend['backend'].search_changes(namespace, repository, query, regex=regex)
        if include_write:
            if include_read:
                changes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    changes[backend_key] = backend['write']['backend'].search_changes(namespace, repository, query,
                                                                                      regex=regex)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    changes[backend_key] = backend['backend'].search_changes(namespace, repository, query, regex=regex)
        return changes

    def change_exists(self, namespace, repository, change, include_read=True, include_write=True):
        exists = False
        if include_read:
            for backend in self.code_persistence_backends_read:
                exists = exists or backend['backend'].change_exists(namespace, repository, change)
        if include_write:
            for backend in self.code_persistence_backends_write:
                exists = exists or backend['backend'].change_exists(namespace, repository, change)
        return exists

    def get_change(self, namespace, repository, change, include_read=True, include_write=True):
        changes = {}
        if include_read:
            if include_write:
                changes['read'] = {}
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    changes['read'][backend_key] = backend['backend'].get_change(namespace, repository, change)
            else:
                for backend in self.code_persistence_backends_read:
                    backend_key = backend['key']
                    changes[backend_key] = backend['backend'].get_change(namespace, repository, change)
        if include_write:
            if include_read:
                changes['write'] = {}
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    changes['write'][backend_key] = backend['backend'].get_change(namespace, repository, change)
            else:
                for backend in self.code_persistence_backends_write:
                    backend_key = backend['key']
                    changes[backend_key] = backend['backend'].get_change(namespace, repository, change)
        return changes

    def create_change(self, namespace, repository, author, comment=None,
                      timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                      include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].create_change(namespace, repository, author, comment, timestamp)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].create_change(namespace, repository, author, comment, timestamp)

    def delete_change(self, namespace, repository, change, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].delete_change(namespace, repository, change)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].delete_change(namespace, repository, change)

    def save_change(self, namespace, repository, change, include_read=False, include_write=True):
        if include_read:
            for backend in self.code_persistence_backends_read:
                backend['backend'].save_change(namespace, repository, change)
        if include_write:
            for backend in self.code_persistence_backends_write:
                backend['backend'].save_change(namespace, repository, change)
