
def validate_string(value, parameter_name=None):
    if value is None:
        raise ValueError("%s can't be None" % (parameter_name if parameter_name else "Parameter"))
    if not isinstance(value, str):
        raise ValueError("%s should be a String" % (parameter_name if parameter_name else "Parameter"))


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
        if repository is None:
            raise ValueError("Repository can't be None")
        if not isinstance(repository, GenericRepository):
            raise ValueError("Repository should be a Repository Object")

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


class CodePersistenceBackend:

    namespace_class = GenericNamespace
    repository_class = GenericRepository
    repository_file_class = GenericRepositoryFile

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
