
import time
import datetime

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

    def __init__(self, repository, comment, timestamp, author):
        self.validate_repository(repository)
        self.repository = repository
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

    def list_namespaces(self):
        pass

    def search_namespaces(self, query):
        pass

    def namespace_exists(self, namespace):
        return False

    def get_namespace(self, namespace):
        pass

    def create_namespace(self, namespace):
        pass

    def delete_namespace(self, namespace):
        pass

    def save_namespace(self, namespace):
        pass

    def list_repositories(self, namespace):
        pass

    def search_repositories(self, namespace, query):
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

    def search_files(self, namespace, repository, query):
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

    def list_changes(self, namespace, repository):
        pass

    def search_changes(self, namespace, repository, query):
        pass

    def change_exists(self, namespace, respository, change):
        return False

    def get_change(self, namespace, respository, change):
        pass

    def create_change(self, namespace, repository, author, comment=None, timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')):
        pass

    def delete_change(self, namespace, repository, change):
        pass

    def save_change(self, namespace, repository, change):
        pass
