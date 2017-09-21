import time
import datetime
import re

from ideApp.models import Backend


def validate_string(value, parameter_name=None):
    if value is None:
        raise ValueError("%s can't be None" % (parameter_name if parameter_name else "Parameter"))
    if not isinstance(value, str):
        raise ValueError("%s should be a String" % (parameter_name if parameter_name else "Parameter"))


def validate_repository(repository):
    if repository is None:
        raise ValueError("Repository can't be None")
    if not isinstance(repository, GenericRepository):
        raise ValueError("Repository should be a Repository Object")


class GenericNamespace:
    namespace = None

    def __init__(self, namespace):
        validate_string(namespace, "Namespace")
        self.namespace = namespace
        self.save()

    def set_namespace(self, namespace):
        validate_string(namespace, "Namespace")
        self.namespace = namespace
        self.save()

    def get_namespace(self):
        return self.namespace

    def save(self):
        pass

    def __str__(self):
        return "NSPC: %s" % self.namespace


class GenericRepository:
    namespace = None
    repository = None

    def validate_namespace(self, namespace):
        if namespace is None:
            raise ValueError("Namespace can't be None")
        if not isinstance(namespace, GenericNamespace):
            raise ValueError("Namespace should be a Namespace Object")

    def __init__(self, namespace, repository):
        self.validate_namespace(namespace)
        self.namespace = namespace
        validate_string(repository, "Repository")
        self.repository = repository
        self.save()

    def set_namespace(self, namespace):
        self.validate_namespace(namespace)
        self.namespace = namespace
        self.save()

    def get_namespace(self):
        return self.namespace

    def set_repository(self, repository):
        validate_string(repository, "Repository")
        self.repository = repository
        self.save()

    def get_repository(self):
        return self.repository

    def save(self):
        pass

    def __str__(self):
        return "REPO: (%s) :: %s" % (self.namespace, self.repository)


class GenericRepositoryFile:
    repository = None
    file_path = None

    def validate_repository(self, repository):
        validate_repository(repository)

    def __init__(self, repository, file_path):
        self.validate_repository(repository)
        self.repository = repository
        validate_string(file_path, "File_Path")
        self.file_path = file_path
        self.save()

    def set_repository(self, repository):
        self.validate_repository(repository)
        self.repository = repository
        self.save()

    def get_repository(self):
        return self.repository

    def set_file_path(self, file_path):
        validate_string(file_path, "File_Path")
        self.file_path = file_path
        self.save()

    def get_file_path(self):
        return self.file_path

    def save(self):
        pass

    def __str__(self):
        return "RepoFile: (%s) :: %s" % (self.repository, self.file_path)


class GenericChange:
    id = None
    repository = None
    comment = None
    timestamp = None
    author = None

    def validate_timestamp(self, timestamp):
        validate_string(timestamp, "Timestamp")

    def validate_author(self, author):
        validate_string(author, "Author")

    def validate_repository(self, repository):
        validate_repository(repository)

    def __init__(self, repository, id, comment, timestamp, author):
        self.validate_repository(repository)
        self.repository = repository
        validate_string(id, "ID")
        self.id = id
        validate_string(comment, "Comment")
        self.comment = comment
        self.validate_timestamp(timestamp)
        self.timestamp = timestamp
        validate_string(author)
        self.author = author
        self.save()

    def set_repository(self, repository):
        self.validate_repository(repository)
        self.repository = repository
        self.save()

    def get_repository(self):
        return self.repository

    def set_id(self, id):
        validate_string(id, "ID")
        self.id = id

    def get_id(self):
        return self.id

    def set_comment(self, comment):
        validate_string(comment, "Comment")
        self.comment = comment
        self.save()

    def get_comment(self):
        return self.comment

    def set_timestamp(self, timestamp):
        self.validate_timestamp(timestamp)
        self.timestamp = timestamp
        self.save()

    def get_timestamp(self):
        return self.timestamp

    def set_author(self, author):
        self.validate_author(author)
        self.author = author
        self.save()

    def save(self):
        pass

    def __str__(self):
        return "Change: (%s) :: \"%s\" :: %s :: %s" % (self.repository, self.comment, self.author, self.timestamp)


class GenericChangeFile:
    change = None
    file_path = None

    def validate_change(self, change):
        if change is None:
            raise ValueError("Change can't be None")
        if not isinstance(change, GenericChange):
            raise ValueError("Change should be a Change Object")

    def __init__(self, change, file_path):
        self.validate_change(change)
        self.change = change
        validate_string(file_path, "File_Path")
        self.file_path = file_path
        self.save()

    def set_change(self, change):
        self.validate_change(change)
        self.change = change
        self.save()

    def get_change(self):
        return self.change

    def set_file_path(self, file_path):
        validate_string(file_path, "File_Path")
        self.file_path = file_path
        self.save()

    def get_file_path(self):
        return self.file_path

    def save(self):
        pass

    def __str__(self):
        return "ChangeFile: (%s) :: %s" % (self.change, self.file_path)


num_backend = 0


class CodePersistenceBackend:
    namespace_class = GenericNamespace
    repository_class = GenericRepository
    repository_file_class = GenericRepositoryFile
    change_class = GenericChange
    change_file_class = GenericChangeFile

    ALIAS_FORMAT = "CPB_%03d"
    alias = None

    backend_db_object = None

    namespaces = []
    repositories = {}
    repository_files = {}
    changes = {}
    change_files = {}

    def get_alias_format(self):
        return self.ALIAS_FORMAT

    def get_alias(self):
        return self.alias

    def load_backend_db_object(self):
        self.backend_db_object = Backend.objects.get_or_create(alias=self.alias)

    def get_backend_db_object(self):
        if self.backend_db_object is None:
            self.load_backend_db_object()
        return self.backend_db_object

    def __init__(self, profile=None):
        global num_backend
        self.alias = self.ALIAS_FORMAT % num_backend
        num_backend = num_backend + 1
        self.load_backend_db_object()

    '''
    Type is a String that contains characters to activate/deactivate what should be synced with this call.
    Capital Letters activate types of Sync
    Lowercase Letters deactivate types of Sync
    The letters are:
        a / A = Everything
        n / N = Namespaces
        r / R = Repositories
        f / F = Repository Files
        c / C = Changes
        h / H = Change Files
    '''

    def sync(self, type):
        should_sync_all = False
        should_sync_namespaces = False
        should_sync_repositories = False
        should_sync_repository_files = False
        should_sync_changes = False
        should_sync_change_files = False
        for flag in type:
            if flag == 'A':
                should_sync_all = True
                should_sync_namespaces = True
                should_sync_repositories = True
                should_sync_repository_files = True
                should_sync_changes = True
                should_sync_change_files = True
            elif flag == 'a':
                should_sync_all = False
                should_sync_namespaces = False
                should_sync_repositories = False
                should_sync_repository_files = False
                should_sync_changes = False
                should_sync_change_files = False
            elif flag == 'N':
                should_sync_namespaces = True
            elif flag == 'n':
                should_sync_namespaces = False
                should_sync_all = False
            elif flag == 'R':
                should_sync_repositories = True
            elif flag == 'r':
                should_sync_repositories = False
                should_sync_all = False
            elif flag == 'F':
                should_sync_repository_files = True
            elif flag == 'f':
                should_sync_repository_files = False
                should_sync_all = False
            elif flag == 'C':
                should_sync_changes = True
            elif flag == 'c':
                should_sync_changes = False
                should_sync_all = False
            elif flag == 'H':
                should_sync_change_files = True
            elif flag == 'h':
                should_sync_change_files = False
                should_sync_all = False
            else:
                raise ValueError(''''%c' is an unrecognized flag.
                Recognized Flags (lowercase to deactivate, uppercase to activate):
                a / A = Everything
                n / N = Namespaces
                r / R = Repositories
                f / F = Repository Files
                c / C = Changes
                h / H = Change Files''' % flag)
        if should_sync_all:
            self.sync_all()
        else:
            if should_sync_namespaces:
                self.sync_namespaces()
            if should_sync_repositories:
                self.sync_repositories()
            if should_sync_repository_files:
                self.sync_repository_files()
            if should_sync_changes:
                self.sync_changes()
            if should_sync_change_files:
                self.sync_change_files()

    def sync_all(self):
        self.sync_namespaces()
        self.sync_repositories()
        self.sync_repository_files()
        self.sync_changes()
        self.sync_change_files()

    def sync_namespaces(self):
        pass

    def sync_repositories(self):
        pass

    def sync_repository_files(self):
        pass

    def sync_changes(self):
        pass

    def sync_change_files(self):
        pass

    def list_namespaces(self):
        return self.namespaces

    def search_namespaces(self, query, regex=False):
        regex_string = query if regex else "^%s$" % query
        pattern = re.compile(regex_string)
        found = []
        for namespace in self.list_namespaces():
            if pattern.match(namespace.get_namespace()):
                found.append(namespace)
        return found

    def namespace_exists(self, namespace):
        try:
            return namespace in self.namespaces
        except TypeError:
            self.namespaces = []
            return False

    def get_namespace(self, namespace):
        try:
            return self.search_namespaces(namespace)[0]
        except IndexError:
            return None

    def create_namespace(self, namespace):
        if self.namespace_exists(namespace):
            self.namespaces.append(namespace)

    def delete_namespace(self, namespace):
        if self.namespace_exists(namespace):
            self.namespaces.remove(namespace)

    def save_namespace(self, namespace):
        pass

    def list_repositories(self, namespace):
        return self.repositories[namespace]

    def search_repositories(self, namespace, query, regex=False):
        if self.namespace_exists(namespace):
            regex_string = query if regex else "^%s$" % query
            pattern = re.compile(regex_string)
            found = []
            for repository in self.list_repositories(namespace):
                if pattern.match(repository.get_repository()):
                    found.append(repository)
            return found
        else:
            return None

    def repository_exists(self, namespace, repository):
        try:
            return self.namespace_exists(namespace) and repository in self.repositories[namespace]
        except TypeError:
            try:
                self.repositories[namespace] = []
            except TypeError:
                self.repositories = {namespace: []}
            return False

    def get_repository(self, namespace, repository):
        try:
            return self.search_repositories(namespace, repository)[0]
        except IndexError:
            return None

    def create_repository(self, namespace, repository):
        if not self.namespace_exists(namespace):
            self.create_namespace(namespace)
        if not self.repository_exists(namespace, repository):
            self.repositories[namespace].append(repository)

    def delete_repository(self, namespace, repository):
        if self.repository_exists(namespace, repository):
            self.repositories[namespace].remove(repository)

    def save_repository(self, namespace, repository):
        pass

    def list_files(self, namespace, repository):
        return self.repository_files[namespace][repository]

    def search_files(self, namespace, repository, query, regex=False):
        if self.repository_exists(namespace, repository):
            regex_string = query if regex else "^%s$" % query
            pattern = re.compile(regex_string)
            found = []
            for file in self.list_files(namespace, repository):
                if pattern.match(file.get_file_path()):
                    found.append(file)
            return found
        else:
            return None

    def file_exists(self, namespace, respository, file_path):
        if self.repository_exists(namespace, respository):
            try:
                respository not in self.repository_files[namespace]
            except TypeError:
                self.repository_files = {}
            try:
                file_path not in self.repository_files[namespace][respository]
            except TypeError:
                self.repository_files[namespace][respository] = []
            return file_path in self.repository_files[namespace][respository]
        else:
            return False

    def get_file(self, namespace, respository, file_path):
        try:
            return self.search_files(namespace, respository, file_path)[0]
        except IndexError:
            return None

    def create_file(self, namespace, repository, file_path, file_contents):
        if not self.namespace_exists(namespace):
            self.create_namespace(namespace)
        if not self.repository_exists(namespace, repository):
            self.create_repository(namespace, repository)
        if not self.file_exists(namespace, repository, file_path):
            self.repository_files[namespace][repository].append(file_path)

    def delete_file(self, namespace, repository, file_path):
        if self.file_exists(namespace, repository, file_path):
            self.repository_files[namespace][repository].remove(file_path)

    def save_file(self, namespace, repository, file_path, file_contents):
        pass

    def list_changes(self, namespace, repository):
        return self.changes

    def search_changes(self, namespace, repository, query, regex=False):
        if self.repository_exists(namespace, repository):
            regex_string = query if regex else "^%s$" % query
            pattern = re.compile(regex_string)
            found = []
            for change in self.list_changes(namespace, repository):
                if pattern.match(change.get_id()):
                    found.append(change)
            return found
        else:
            return None

    def change_exists(self, namespace, respository, change):
        if self.repository_exists(namespace, respository):
            try:
                respository not in self.changes[namespace]
            except TypeError:
                self.changes = {}
            try:
                change not in self.changes[namespace][respository]
            except TypeError:
                self.changes[namespace][respository] = []
            return change in self.changes[namespace][respository]
        else:
            return False

    def get_change(self, namespace, respository, change):
        try:
            return self.search_changes(namespace, respository, change)[0]
        except IndexError:
            return None

    def create_change(self, namespace, repository, id, author, comment=None,
                      timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')):
        if not self.namespace_exists(namespace):
            self.create_namespace(namespace)
        if not self.repository_exists(namespace, repository):
            self.create_repository(namespace, repository)
        if not self.change_exists(namespace, repository, id):
            self.changes[namespace][repository].append(id)

    def delete_change(self, namespace, repository, change):
        if self.change_exists(namespace, repository, change):
            self.changes[namespace][repository].remove(change)

    def save_change(self, namespace, repository, change):
        pass
