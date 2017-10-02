import time
import datetime
import re

from ideApp.models import Backend, BackendType


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
    contents = None

    def validate_repository(self, repository):
        validate_repository(repository)

    def __init__(self, repository, file_path, file_contents):
        self.validate_repository(repository)
        self.repository = repository
        validate_string(file_path, "File_Path")
        self.file_path = file_path
        validate_string(file_contents, "Contents")
        self.contents = file_contents
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

    def set_contents(self, contents):
        validate_string(contents, "Contents")
        self.contents = contents

    def get_contents(self):
        return self.contents

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

    backend_type = BackendType.objects.get_or_create(name="GenericCodePersistenceBackend")

    backend_db_object = None

    namespaces = []
    repositories = {}
    repository_files = {}
    changes = {}
    change_files = {}

    def get_namespace_class(self):
        return self.namespace_class

    def get_repository_class(self):
        return self.repository_class

    def get_repository_file_class(self):
        return self.repository_file_class

    def get_change_class(self):
        return self.change_class

    def get_change_file_class(self):
        return self.change_file_class

    def __str__(self):
        return "%s" % self.backend_db_object[0]

    def get_alias_format(self):
        return self.ALIAS_FORMAT

    def get_alias(self):
        return self.alias

    def load_backend_db_object(self):
        #print(self.backend_type)
        self.backend_db_object = Backend.objects.get_or_create(alias=self.alias, type=self.backend_type[0])

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
            if isinstance(namespace, self.namespace_class):
                for nsp in self.list_namespaces():
                    if isinstance(nsp, self.namespace_class):
                        if nsp.get_namespace() == namespace.get_namespace():
                            return True
                    elif isinstance(nsp, str):
                        if nsp == namespace.get_namespace():
                            return True
                return False
            else:
                if isinstance(namespace, str):
                    for nsp in self.list_namespaces():
                        if isinstance(nsp, self.namespace_class):
                            if nsp.get_namespace() == namespace:
                                return True
                        elif isinstance(nsp, str):
                            if nsp == namespace:
                                return True
                return False
        except TypeError:
            self.namespaces = []
            return False

    def get_namespace(self, namespace):
        try:
            return self.search_namespaces(namespace)[0]
        except IndexError:
            return None

    def build_namespace(self, namespace):
        if isinstance(namespace, str):
            return self.get_namespace_class()(namespace=namespace)
        elif isinstance(namespace, self.get_namespace_class()):
            return namespace
        else:
            raise ValueError("Namespace is an Invalid Type")

    def create_namespace(self, namespace):
        if not self.namespace_exists(namespace):
            if isinstance(namespace, str):
                namespace_obj = self.build_namespace(namespace=namespace)
            elif isinstance(namespace, self.get_namespace_class()):
                namespace_obj = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            self.namespaces.append(namespace_obj)
            return namespace_obj
        else:
            return None

    def delete_namespace(self, namespace):
        if self.namespace_exists(namespace):
            if isinstance(namespace, str):
                namespace_delete = self.build_namespace(namespace=namespace)
            elif isinstance(namespace, self.get_namespace_class()):
                namespace_delete = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            self.namespaces.remove(namespace_delete)

    def save_namespace(self, namespace):
        self.create_namespace(namespace)
        if isinstance(namespace, str):
            namespace_save = self.build_namespace(namespace=namespace)
        elif isinstance(namespace, self.get_namespace_class()):
            namespace_save = namespace
        else:
            raise ValueError("Namespace is an Invalid Type")
        namespace_save.save()

    def list_repositories(self, namespace):
        if isinstance(namespace, self.get_namespace_class()):
            namespace_str = namespace.get_namespace()
        elif isinstance(namespace, str):
            namespace_str = namespace
        else:
            raise ValueError("Namespace is an Invalid Type")
        return self.repositories[namespace_str]

    def search_repositories(self, namespace, query, regex=False):
        if self.namespace_exists(namespace):
            regex_string = query if regex else "^%s$" % query
            pattern = re.compile(regex_string)
            found = []
            for repository in self.list_repositories(namespace):
                if isinstance(repository, self.get_repository_class()):
                    if pattern.match(repository.get_repository()):
                        found.append(repository)
                elif isinstance(repository, str):
                    if pattern.match(repository):
                        found.append(repository)
            return found
        else:
            return None

    def repository_exists(self, namespace, repository):
        try:
            if isinstance(repository, self.repository_class):
                if not self.namespace_exists(namespace):
                    return False
                for repo in self.list_repositories(namespace):
                    if isinstance(repo, self.repository_class):
                        if repo.get_repository() == repository:
                            return True
                    elif isinstance(repo, str):
                        if repo == repository:
                            return True
                return False
            else:
                if self.namespace_exists(namespace):
                    if isinstance(repository, str):
                        for nsp, repos in self.repositories.items():
                            for repo in repos:
                                if isinstance(repo, self.repository_class):
                                    if repo.get_repository() == repository:
                                        return True
                                elif isinstance(repo, str):
                                    if repo == repository:
                                        return True
                return False
        except TypeError:
            try:
                if isinstance(namespace, self.get_namespace_class()):
                    namespace_str = namespace.get_namespace()
                elif isinstance(namespace, str):
                    namespace_str = namespace
                else:
                    raise ValueError("Namespace is an Invalid Type")
                self.repositories[namespace_str] = []
            except TypeError:
                if isinstance(namespace, self.get_namespace_class()):
                    namespace_str = namespace.get_namespace()
                elif isinstance(namespace, str):
                    namespace_str = namespace
                else:
                    raise ValueError("Namespace is an Invalid Type")
                self.repositories = {namespace_str: []}
            return False

    def get_repository(self, namespace, repository):
        try:
            return self.search_repositories(namespace, repository)[0]
        except IndexError:
            return None

    def build_repository(self, namespace, repository):
        if isinstance(repository, self.get_repository_class()):
            return repository
        namespace_obj = self.build_namespace(namespace=namespace)
        if isinstance(repository, str):
            return self.get_repository_class()(namespace=namespace_obj, repository=repository)
        else:
            raise ValueError("Repository is an Invalid Type")

    def create_repository(self, namespace, repository):
        if not self.namespace_exists(namespace):
            self.create_namespace(namespace)
        if isinstance(namespace, self.get_namespace_class()):
            namespace_str = namespace.get_namespace()
        elif isinstance(namespace, str):
            namespace_str = namespace
        else:
            raise ValueError("Namespace is an Invalid Type")
        if not self.repository_exists(namespace, repository):
            if self.repositories.get(namespace, None) is None:
                self.repositories[namespace_str] = []
            repository_obj = self.build_repository(namespace, repository)
            self.repositories[namespace_str].append(repository_obj)

    def delete_repository(self, namespace, repository):
        if self.repository_exists(namespace, repository):
            if isinstance(namespace, self.get_namespace_class()):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            repository_obj = self.build_repository(namespace=namespace, repository=repository)
            self.repositories[namespace_str].remove(repository_obj)

    def save_repository(self, namespace, repository):
        self.save_namespace(namespace)
        self.create_repository(namespace, repository)
        repository_obj = self.build_repository(namespace=namespace, repository=repository)
        repository_obj.save()

    def list_files(self, namespace, repository):
        if isinstance(namespace, self.get_namespace_class()):
            namespace_str = namespace.get_namespace()
        elif isinstance(namespace, str):
            namespace_str = namespace
        else:
            raise ValueError("Namespace is an Invalid Type")
        if isinstance(repository, self.get_repository_class()):
            repository_str = repository.get_repository()
        elif isinstance(repository, str):
            repository_str = repository
        else:
            raise ValueError("Repository is an Invalid Type")
        return self.repository_files[namespace_str][repository_str]

    def search_files(self, namespace, repository, query, regex=False):
        if self.repository_exists(namespace, repository):
            regex_string = query if regex else "^%s$" % query
            pattern = re.compile(regex_string)
            found = []
            for file in self.list_files(namespace, repository):
                if isinstance(file, self.repository_file_class):
                    if pattern.match(file.get_file_path()):
                        found.append(file)
                if isinstance(file, str):
                    if pattern.match(file):
                        found.append(file)
            return found
        else:
            return None

    def file_exists(self, namespace, repository, file_path):
        if self.repository_exists(namespace, repository):
            try:
                if self.repository_files.get(namespace, None) is None:
                    self.repository_files[namespace] = {}
                if repository not in self.repository_files[namespace]:
                    return False
            except TypeError:
                self.repository_files = {}
            if isinstance(file_path, self.repository_file_class):
                try:
                    found = False
                    if isinstance(namespace, self.get_namespace_class()):
                        namespace_str = namespace.get_namespace()
                    elif isinstance(namespace, str):
                        namespace_str = namespace
                    else:
                        raise ValueError("Namespace is an Invalid Type")
                    if isinstance(repository, self.get_repository_class()):
                        repository_str = repository.get_repository()
                    elif isinstance(repository, str):
                        repository_str = repository
                    else:
                        raise ValueError("Repository is an Invalid Type")
                    for repo_file in self.repository_files[namespace_str][repository_str]:
                        if isinstance(repo_file, self.repository_file_class):
                            if file_path.get_file_path() == repo_file.get_file_path():
                                found = True
                        elif isinstance(repo_file, str):
                            if file_path.get_file_path() == repo_file:
                                found = True
                    if not found:
                        return False
                except TypeError:
                    if isinstance(namespace, self.get_namespace_class()):
                        namespace_str = namespace.get_namespace()
                    elif isinstance(namespace, str):
                        namespace_str = namespace
                    else:
                        raise ValueError("Namespace is an Invalid Type")
                    if isinstance(repository, self.get_repository_class()):
                        repository_str = repository.get_repository()
                    elif isinstance(repository, str):
                        repository_str = repository
                    else:
                        raise ValueError("Repository is an Invalid Type")
                    self.repository_files[namespace_str][repository_str] = []
                    for repo_file in self.repository_files[namespace_str][repository_str]:
                        if isinstance(repo_file, self.repository_file_class):
                            if file_path.get_file_path() == repo_file.get_file_path():
                                return True
                        elif isinstance(repo_file, str):
                            if file_path.get_file_path() == repo_file:
                                return True
                    return False
            else:
                if isinstance(file_path, str):
                    for nsp, repos in self.repository_files.items():
                        for repo, files in repos.items():
                            for file in files:
                                if isinstance(file, self.repository_file_class):
                                    if file.get_file_path() == file_path:
                                        return True
                                elif isinstance(file, str):
                                    if file == file_path:
                                        return True
                return False
        else:
            return False

    def get_file(self, namespace, repository, file_path):
        result = self.search_files(namespace, repository, file_path)
        try:
            return result[0]
        except IndexError:
            return None
        except TypeError:
            return None

    def build_file(self, namespace, repository, file_path, file_contents):
        repository_obj = self.build_repository(namespace=namespace, repository=repository)
        if not isinstance(file_path, str):
            raise ValueError("File_Path must be a String")
        if not isinstance(file_contents, str):
            raise ValueError("File_Contents must be a String")
        return self.get_repository_file_class()(repository=repository_obj, file_path=file_path,
                                                file_contents=file_contents)

    def create_file(self, namespace, repository, file_path, file_contents):
        if not self.namespace_exists(namespace):
            self.create_namespace(namespace)
        if not self.repository_exists(namespace, repository):
            self.create_repository(namespace, repository)
        if not self.file_exists(namespace, repository, file_path):
            if isinstance(namespace, self.get_namespace_class()):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            if isinstance(repository, self.get_repository_class()):
                repository_str = repository.get_repository()
            elif isinstance(repository, str):
                repository_str = repository
            else:
                raise ValueError("Repository is an Invalid Type")
            if self.repository_files.get(namespace_str, None) is None:
                self.repository_files[namespace_str] = {}
            if self.repository_files[namespace_str].get(repository_str, None) is None:
                self.repository_files[namespace_str][repository_str] = []
            file_obj = self.build_file(namespace=namespace, repository=repository, file_path=file_path,
                                       file_contents=file_contents)
            self.repository_files[namespace_str][repository_str].append(file_obj)

    def delete_file(self, namespace, repository, file_path):
        if self.file_exists(namespace, repository, file_path):
            if isinstance(namespace, self.get_namespace_class()):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            if isinstance(repository, self.get_repository_class()):
                repository_str = repository.get_repository()
            elif isinstance(repository, str):
                repository_str = repository
            else:
                raise ValueError("Repository is an Invalid Type")
            if isinstance(file_path, self.get_repository_file_class()):
                delete_file_path = file_path.get_file_path()
            elif isinstance(file_path, str):
                delete_file_path = file_path
            else:
                raise ValueError("File_Path is an Invalid Type")
            marked_for_deletion = []
            for file in self.list_files(namespace=namespace, repository=repository):
                if isinstance(file, self.get_repository_file_class()):
                    if file.get_file_path() == delete_file_path:
                        marked_for_deletion.append(file)
                elif isinstance(file, str):
                    if file == delete_file_path:
                        marked_for_deletion.append(file)
            for delete_file in marked_for_deletion:
                self.repository_files[namespace_str][repository_str].remove(delete_file)

    def save_file(self, namespace, repository, file_path, file_contents):
        self.save_namespace(namespace)
        self.save_repository(namespace, repository)
        self.create_file(namespace, repository, file_path, file_contents)
        file_obj = self.build_file(namespace=namespace, repository=repository, file_path=file_path,
                                   file_contents=file_contents)
        file_obj.save()

    def save_existent_file(self, namespace, repository, file):
        self.save_namespace(namespace=namespace)
        self.save_repository(namespace=namespace, repository=repository)
        if file is not None:
            repo_file_class = self.get_repository_file_class()
            if isinstance(namespace, self.get_namespace_class()):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            if isinstance(repository, self.get_repository_class()):
                repository_str = repository.get_repository()
            elif isinstance(repository, str):
                repository_str = repository
            else:
                raise ValueError("Repository is an Invalid Type")
            if isinstance(file, repo_file_class):
                index = 0
                broken = False
                for repo_file in self.repository_files[namespace_str][repository_str]:
                    if isinstance(repo_file, repo_file_class):
                        if repo_file.get_file_path() == file.get_file_path():
                            self.repository_files[namespace_str][repository_str][index] = file
                            broken = True
                            break
                    elif isinstance(repo_file, str):
                        if repo_file == file.get_file_path():
                            self.repository_files[namespace_str][repository_str][index] = file
                            broken = True
                            break
                    index = index + 1
                if not broken:
                    self.repository_files[namespace_str][repository_str].append(file)
            elif isinstance(file, str):
                index = 0
                broken = False
                for repo_file in self.repository_files[namespace_str][repository_str]:
                    if isinstance(repo_file, repo_file_class):
                        if repo_file.get_file_path() == file:
                            self.repository_files[namespace_str][repository_str][index] = file
                            broken = True
                            break
                    elif isinstance(repo_file, str):
                        if repo_file == file:
                            self.repository_files[namespace_str][repository_str][index] = file
                            broken = True
                            break
                    index = index + 1
                if not broken:
                    self.repository_files[namespace_str][repository_str].append(file)
            else:
                raise ValueError("File must be some sort of Repository File Object or a String")

    def list_changes(self, namespace, repository):
        if isinstance(namespace, self.get_namespace_class()):
            namespace_str = namespace.get_namespace()
        elif isinstance(namespace, str):
            namespace_str = namespace
        else:
            raise ValueError("Namespace is an Invalid Type")
        if isinstance(repository, self.get_repository_class()):
            repository_str = repository.get_repository()
        elif isinstance(repository, str):
            repository_str = repository
        else:
            raise ValueError("Repository is an Invalid Type")
        return self.changes[namespace_str][repository_str]

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

    def build_change(self, namespace, repository, id, author, comment=None,
                     timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')):
        repository_obj = self.build_repository(namespace=namespace, repository=repository)
        return self.get_change_class()(repository=repository_obj, id=id, author=author, comment=comment,
                                       timestamp=timestamp)

    def change_exists(self, namespace, repository, change):
        if self.repository_exists(namespace, repository):
            if isinstance(change, self.get_change_class()):
                change_str = change.get_id()
            elif isinstance(change, str):
                change_str = change
            else:
                raise ValueError("Change in an Invalid Type")
            for chg in self.list_changes(namespace=namespace, repository=repository):
                if isinstance(chg, self.get_change_class()):
                    if chg.get_id() == change_str:
                        return True
                elif isinstance(chg, str):
                    if chg == change_str:
                        return True
            return False
        else:
            return False

    def get_change(self, namespace, repository, change):
        result = self.search_changes(namespace=namespace, repository=repository, query=change)
        try:
            return result[0]
        except IndexError:
            return None
        except TypeError:
            return None

    def create_change(self, namespace, repository, id, author, comment=None,
                      timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')):
        if not self.namespace_exists(namespace):
            self.create_namespace(namespace)
        if not self.repository_exists(namespace, repository):
            self.create_repository(namespace, repository)
        if not self.change_exists(namespace, repository, id):
            if isinstance(namespace, self.get_namespace_class()):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            if isinstance(repository, self.get_repository_class()):
                repository_str = repository.get_repository()
            elif isinstance(repository, str):
                repository_str = repository
            else:
                raise ValueError("Repository is an Invalid Type")
            change = self.build_change(namespace=namespace, repository=repository, id=id, author=author,
                                       comment=comment, timestamp=timestamp)
            self.changes[namespace_str][repository_str].append(change)

    def delete_change(self, namespace, repository, change):
        if self.change_exists(namespace, repository, change):
            if isinstance(namespace, self.get_namespace_class()):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("Namespace is an Invalid Type")
            if isinstance(repository, self.get_repository_class()):
                repository_str = repository.get_repository()
            elif isinstance(repository, str):
                repository_str = repository
            else:
                raise ValueError("Repository is an Invalid Type")
            if isinstance(change, self.get_change_class()):
                change_str = change.get_id()
            elif isinstance(change, str):
                change_str = change
            else:
                raise ValueError("Change is an Invalid Type")
            marked_for_deletion = []
            for chg in self.list_changes(namespace=namespace, repository=repository):
                if isinstance(chg, self.get_change_class()):
                    if chg.get_id() == change_str:
                        marked_for_deletion.append(chg)
                elif isinstance(chg, str):
                    if chg == change_str:
                        marked_for_deletion.append(chg)
            for chg in marked_for_deletion:
                self.changes[namespace_str][repository_str].remove(chg)

    def save_change(self, namespace, repository, change):
        self.save_namespace(namespace)
        self.save_repository(namespace, repository)
        if isinstance(change, self.get_change_class()):
            change_obj = change
        elif isinstance(change, dict):
            repository_obj = self.build_repository(namespace=namespace, repository=repository)
            id = change.get('id', None)
            author = change.get('author', None)
            comment = change.get('comment', None)
            timestamp = change.get('timestamp', None)
            change_obj = self.get_change_class()(repository=repository_obj, id=id, author=author, comment=comment,
                                                 timestamp=timestamp)
        self.create_change(namespace, repository, change_obj.get_id(), change_obj.get_author(),
                           change_obj.get_comment(), change_obj.get_timestamp())
        change_obj.save()
