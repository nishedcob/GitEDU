
from ideApp.models import BackendType

from ideApp.CodePersistenceBackends.generics import GenericNamespace, GenericRepository, GenericRepositoryFile,\
    GenericChange, GenericChangeFile, CodePersistenceBackend, validate_string

from ideApp.CodePersistenceBackends.MongoDB import mongodb_models, mongodb_connect

from pymodm.queryset import QuerySet

from GitEDU.settings import CODE_PERSISTENCE_BACKENDS


def validate_mongo_repository(repository):
    if repository is None:
        raise ValueError("Repository can't be None")
    if not isinstance(repository, MongoRepository):
        raise ValueError("Repository should be a Repository Object")


class MongoNamespace(GenericNamespace):

    persistence_class = mongodb_models.NamespaceModel
    persistence_object = None

    def retrieve(self, id=None, namespace=None):
        if id is None:
            if namespace is None:
                raise ValueError("ID and Namespace can't be None")
            else:
                self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace}).first()
        else:
            if namespace is None:
                self.persistence_object = self.persistence_class.objects.raw({'_id': id}).first()
            else:
                self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace}).first()
        self.load_persisted_values()

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.name = self.namespace
        self.persistence_object.save()

    def __str__(self):
        return "MongoNSPC: %s [%s]" % (self.namespace, self.persistence_object)

    def load_persisted_values(self):
        self.set_namespace(self.persistence_object.name)


class MongoRepository(GenericRepository):

    persistence_class = mongodb_models.RepositoryModel
    persistence_object = None

    def validate_namespace(self, namespace):
        if namespace is None:
            raise ValueError("Namespace can't be None")
        if not isinstance(namespace, MongoNamespace):
            raise ValueError("Namespace should be a Namespace Object")

    def retrieve(self, id=None, namespace=None, repository=None):
        if id is None:
            if namespace is None:
                if repository is None:
                    raise ValueError("ID, Namespace and Repository can't be None")
                else:
                    print("WARNING: Only searching for repositories based on Repository, may find more than 1," +
                          " will only use the first found")
                    self.persistence_object = self.persistence_class.objects.raw({'repository': repository}).first()
            else:
                if repository is None:
                    print("WARNING: Only searching for repositories based on Namespace, may find more than 1," +
                          " will only use the first found")
                    self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace}).first()
                else:
                    self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                  'repository': repository}).first()
        else:
            if namespace is None:
                if repository is None:
                    self.persistence_object = self.persistence_class.objects.raw({'_id': id}).first()
            else:
                if repository is None:
                    self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace})\
                        .first()
                else:
                    self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                  'repository': repository}).first()
        self.load_persisted_values()

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.namespace = self.namespace.persistence_object
        self.persistence_object.name = self.repository
        self.persistence_object.save()

    def __str__(self):
        return "MongoREPO: (%s) :: %s [%s]" % (self.namespace, self.repository, self.persistence_object)

    def load_persisted_values(self):
        self.set_namespace(self.persistence_object.namespace)
        self.set_repository(self.persistence_object.name)


class MongoRepositoryFile(GenericRepositoryFile):
    language = None

    persistence_class = mongodb_models.RepositoryFileModel
    persistence_object = None

    def validate_repository(self, repository):
        validate_mongo_repository(repository)

    def set_language(self, language):
        validate_string(language)
        self.language = language

    def get_language(self):
        return self.language

    def retrieve(self, id=None, namespace=None, repository=None, file_path=None):
        if id is None:
            if namespace is None:
                if repository is None:
                    if file_path is None:
                        raise ValueError("ID, Namespace, Repository and File_Path can't be None")
                    else:
                        print("WARNING: Only searching for files based on File_Path, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'file_path': file_path}).first()
                else:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Repository, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'repository': repository}).first()
                    else:
                        print("WARNING: Only searching for files based on Repository and File_Path," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'repository': repository,
                                                                                      'file_path': file_path}).first()
            else:
                if repository is None:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Namespace, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace}).first()
                    else:
                        print("WARNING: Only searching for files based on Namespace and File_Path," +
                              "may find more than 1, will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                      'file_path': file_path}).first()
                else:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Namespace and Repository," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                      'repository': repository}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                      'repository': repository,
                                                                                      'file_path': file_path}).first()
        else:
            if namespace is None:
                if repository is None:
                    if file_path is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'file_path': file_path
                                                                                      }).first()
                else:
                    if file_path is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id,
                                                                                      'repository': repository}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id,
                                                                                      'repository': repository,
                                                                                      'file_path': file_path}).first()
            else:
                if repository is None:
                    if file_path is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace
                                                                                      }).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      'file_path': file_path}).first()
                else:
                    if file_path is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      'repository': repository}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      'repository': repository,
                                                                                      'file_path': file_path}).first()
            self.load_persisted_values()

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.file_path = self.file_path
        self.persistence_object.repository = self.repository.persistence_object
        self.persistence_object.contents = self.contents
        self.persistence_object.language = self.language
        self.persistence_object.save()

    def __str__(self):
        return "MongoRepoFile: (%s) :: %s :: %s :: %s [%s]" % (self.repository, self.file_path, self.language,
                                                               self.contents, self.persistence_object)

    def load_persisted_values(self):
        self.set_repository(self.persistence_object.repository)
        self.set_contents(self.persistence_object.contents)
        self.set_file_path(self.persistence_object.file_path)
        self.set_language(self.persistence_object.language)


class MongoChange(GenericChange):

    persistence_class = mongodb_models.ChangeModel
    persistence_object = None

    def validate_repository(self, repository):
        validate_mongo_repository(repository)

    def retrieve(self, id=None, namespace=None, repository=None, change=None):
        database = 'gitEduDB'
        if id is None:
            if namespace is None:
                if repository is None:
                    if change is None:
                        raise ValueError("ID, Namespace, Repository and Change can't be None")
                    else:
                        print("WARNING: Only searching for changes based on Change, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'change': change}).first()
                else:
                    if change is None:
                        print("WARNING: Only searching for changes based on Repository, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'repository': repository}).first()
                    else:
                        print("WARNING: Only searching for files based on Repository and Change," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'repository': repository,
                                                                                      'change': change}).first()
            else:
                if repository is None:
                    if change is None:
                        print("WARNING: Only searching for changes based on Namespace, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'namespace':'%s'})"
                                                           % (database, namespace)).first()
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace}).first()
                    else:
                        print("WARNING: Only searching for changes based on Namespace and Change," +
                              "may find more than 1, will only use the first found")
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                      'change': change}).first()
                else:
                    if change is None:
                        print("WARNING: Only searching for changes based on Namespace and Repository," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'namespace':'%s', 'repository':'%s'})"
                                                           % (database, namespace, repository)).first()
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                      'repository': repository,
                                                                                      'change': change}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'namespace': namespace,
                                                                                      'repository': repository}).first()
        else:
            if namespace is None:
                if repository is None:
                    if change is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'change': change
                                                                                      }).first()
                else:
                    if change is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id,
                                                                                      'repository': repository}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id,
                                                                                      'repository': repository,
                                                                                      'change': change}).first()
            else:
                if repository is None:
                    if change is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      }).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      'change': change}).first()
                else:
                    if change is None:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      'repository': repository}).first()
                    else:
                        self.persistence_object = self.persistence_class.objects.raw({'_id': id, 'namespace': namespace,
                                                                                      'repository': repository,
                                                                                      'change': change}).first()
        self.load_persisted_values()

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.timestamp = self.timestamp
        self.persistence_object.repository = self.repository.persistence_object
        self.persistence_object.author = self.author
        self.persistence_object.comment = self.comment
        self.persistence_object.save()

    def __str__(self):
        return "MongoChange: (%s) :: \"%s\" :: %s :: %s :: [%s]" % (self.repository, self.comment, self.author,
                                                                    self.timestamp, self.persistence_object)

    def load_persisted_values(self):
        self.set_repository(self.persistence_object.repository)
        self.set_author(self.persistence_object.author)
        self.set_comment(self.persistence_object.comment)
        self.set_id(self.persistence_object.implicit_id)


class MongoChangeFile(GenericChangeFile):

    contents = None
    language = None

    persistence_class = mongodb_models.ChangeFileModel
    persistence_object = None

    def validate_repository(self, repository):
        validate_mongo_repository(repository)

    def set_contents(self, contents):
        validate_string(contents)
        self.contents = contents

    def get_contents(self):
        return self.contents

    def set_language(self, language):
        validate_string(language)
        self.language = language

    def get_language(self):
        return self.language

    def retrieve(self, id=None, namespace=None, repository=None, change=None, file_path=None):
        database = 'gitEduDB'
        if id is None:
            if namespace is None:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            raise ValueError("ID, Namespace, Repository, Change and File_Path can't be None")
                        else:
                            print("WARNING: Only searching for change files based on File_Path, may find more than 1," +
                                  " will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Change, may find more than 1," +
                                  " will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'change': change
                            }).first()
                        else:
                            print("WARNING: Only searching for change files based on Change and File_Path, " +
                                  "may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'change': change,
                                'file_path': file_path
                            }).first()
                else:
                    if change is None:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Repository," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'repository': repository
                            }).first()
                        else:
                            print("WARNING: Only searching for change files based on Repository and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'repository': repository,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Repository and Change," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'repository': repository,
                                'change': change
                            }).first()
                        else:
                            print("WARNING: Only searching for change files based on Repository, Change and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'repository': repository,
                                'change': change,
                                'file_path': file_path
                            }).first()
            else:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Namespace, may find more than 1," +
                                  " will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace
                            }).first()
                        else:
                            print("WARNING: Only searching for change files based on Namespace and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Namespace and Change," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'change': change
                            }).first()
                        else:
                            print("WARNING: Only searching for change files based on Namespace, Change and File_Path, " +
                                  "may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'change': change,
                                'file_path': file_path
                            }).first()
                else:
                    if change is None:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Namespace and Repository," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'repository': repository,
                            }).first()
                        else:
                            print("WARNING: Only searching for change files based on Namespace, Repository and" +
                                  "File_Path, may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'repository': repository,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for change files based on Namespace, Repository and "
                                  "Change, may find more than 1, will only use the first found")
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'repository': repository,
                                'change': change,
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                'namespace': namespace,
                                'repository': repository,
                                'change': change,
                                'file_path': file_path
                            }).first()
        else:
            if namespace is None:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'change': change
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'change': change,
                                'file_path': file_path
                            }).first()
                else:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repository
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repository,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repository,
                                'change': change
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repository,
                                'change': change,
                                'file_path': file_path
                            }).first()
            else:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'change': change
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'change': change,
                                'file_path': file_path
                            }).first()
                else:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'repository': repository
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'repository': repository,
                                'file_path': file_path
                            }).first()
                    else:
                        if file_path is None:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'repository': repository,
                                'change': change
                            }).first()
                        else:
                            self.persistence_object = self.persistence_class.objects.raw({
                                '_id': id,
                                'namespace': namespace,
                                'repository': repository,
                                'change': change,
                                'file_path': file_path
                            }).first()
        self.load_persisted_values()

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.file_path = self.file_path
        self.persistence_object.change = self.change.persistence_object
        self.persistence_object.language = self.language
        self.persistence_object.contents = self.contents
        self.persistence_object.save()

    def __str__(self):
        return "MongoChangeFile: (%s) :: %s :: %s :: %s [%s]" % (self.change, self.file_path, self.language,
                                                               self.contents, self.persistence_object)

    def load_persisted_values(self):
        self.set_language(self.persistence_object.language)
        self.set_file_path(self.persistence_object.file_path)
        self.set_contents(self.persistence_object.contents)
        self.set_change(self.persistence_object.change)


mongo_num_conn = 0


class MongoDBCodePersistenceBackend(CodePersistenceBackend):

    namespace_class = MongoNamespace
    repository_class = MongoRepository
    repository_file_class = MongoRepositoryFile
    change_class = MongoChange
    change_file_class = MongoChangeFile

    ALIAS_FORMAT = "mongo_%03d"
    backend_type = BackendType.objects.get_or_create(name="MongoDBCodePersistenceBackend")

    def __init__(self, profile=None):
        global mongo_num_conn
        if profile is None:
            raise ValueError("Connection Parameters can not be None")
        self.alias = self.ALIAS_FORMAT % mongo_num_conn
        mongodb_connect.build_connection_from_settings(profile, self.alias)
        mongo_num_conn = mongo_num_conn + 1
        self.load_backend_db_object()

    def sync_namespaces(self):
        print("Namespaces: %s" % self.namespaces)
        for namespace in self.namespaces:
            namespace.save()
        self.namespaces = list(mongodb_models.NamespaceModel.objects.raw({}))
        print("Namespaces: %s" % self.namespaces)

    def sync_repositories(self):
        print("Repositories: %s" % self.repositories)
        for namespace in self.namespaces:
            if self.repositories.get(namespace, None) is None:
                self.repositories[namespace] = []
        for namespace, repositories in self.repositories.items():
            for repository in repositories:
                repository.save()
            self.repositories[namespace] = list(mongodb_models.RepositoryModel.objects.raw({'namespace': namespace}))
        print("Repositories: %s" % self.repositories)

    def sync_repository_files(self):
        print("Repository Files: %s" % self.repository_files)
        for namespace in self.list_namespaces():
            if self.repository_files.get(namespace, None) is None:
                self.repository_files[namespace] = {}
            for repository in self.list_repositories(namespace):
                if self.repository_files[namespace].get(repository, None) is None:
                    self.repository_files[namespace][repository] = []
        for namespace, repositories in self.repository_files.items():
            for repository, repository_files in repositories.items():
                for repository_file in repository_files:
                    repository_file.save()
                self.repository_files[namespace][repository] = list(mongodb_models.RepositoryFileModel.object
                                                                    .raw({'repository': repository}))
        print("Repository Files: %s" % self.repository_files)

    def sync_changes(self):
        print("Changes: %s" % self.changes)
        for namespace in self.list_namespaces():
            if self.changes.get(namespace, None) is None:
                self.changes[namespace] = {}
            for repository in self.list_repositories(namespace):
                if self.changes[namespace].get(repository, None) is None:
                    self.changes[namespace][repository] = []
        for namespace, repositories in self.changes.items():
            for repository, changes in repositories.items():
                for change in changes:
                    change.save()
                self.changes[namespace][repository] = list(mongodb_models.ChangeModel.objects.raw({
                    'repository': repository
                }))
        print("Changes: %s" % self.changes)

    def sync_change_files(self):
        print("Change Files: %s" % self.change_files)
        for namespace in self.list_namespaces():
            if self.change_files.get(namespace, None) is None:
                self.change_files[namespace] = {}
            for repository in self.list_repositories(namespace):
                if self.change_files[namespace].get(repository, None) is None:
                    self.change_files[namespace][repository] = {}
                for change in self.list_changes(namespace, repository):
                    if self.change_files[namespace][repository].get(change, None) is None:
                        self.change_files[namespace][repository][change] = []
        for namespace, repositories in self.change_files.items():
            for repository, changes in repositories.items():
                for change, change_files in changes.items():
                    for change_file in change_files:
                        change_file.save()
                    self.change_files[namespace][repository][change] = list(mongodb_models.ChangeFileModel.objects.raw(
                        {'change': change}
                    ))
        print("Change Files: %s" % self.change_files)
