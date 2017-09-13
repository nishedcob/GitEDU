
from ideApp.CodePersistenceBackends.generics import GenericNamespace, GenericRepository, GenericRepositoryFile,\
    GenericChange, GenericChangeFile, CodePersistenceBackend, validate_string

#from ideApp.CodePersistenceBackends.MongoDB import mongodb_models, connect

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
        database = 'gitEduDB'
        if id is None:
            if namespace is None:
                raise ValueError("ID and Namespace can't be None")
            else:
                self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'namespace':'%s'})"
                                                   % (database, namespace)).first()
        else:
            if namespace is None:
                self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s'})"
                                                   % (database, id)).first()
            else:
                self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s', 'namespace':'%s'})"
                                                   % (database, id, namespace)).first()
        self.set_namespace(self.persistence_object.namespace)

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.namespace = self.namespace
        self.persistence_object.save()

    def __str__(self):
        return "MongoNSPC: %s [%s]" % (self.namespace, self.persistence_object)


class MongoRepository(GenericRepository):

    persistence_class = mongodb_models.RepositoryModel
    persistence_object = None

    def validate_namespace(self, namespace):
        if namespace is None:
            raise ValueError("Namespace can't be None")
        if not isinstance(namespace, MongoNamespace):
            raise ValueError("Namespace should be a Namespace Object")

    def retrieve(self, id=None, namespace=None, repository=None):
        database = 'gitEduDB'
        if id is None:
            if namespace is None:
                if repository is None:
                    raise ValueError("ID, Namespace and Repository can't be None")
                else:
                    self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'repository':'%s'})"
                                                       % (database, repository)).first()
            else:
                if repository is None:
                    self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'namespace':'%s'})"
                                                       % (database, namespace)).first()
                else:
                    self.persistence_object = QuerySet(self.persistence_class,
                                                       "db.%s.find({'namespace':'%s', 'repository':'%s'})"
                                                       % (database, namespace, repository)).first()
        else:
            if namespace is None:
                if repository is None:
                    self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s'})"
                                                       % (database, id)).first()
            else:
                if repository is None:
                    self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s', 'namespace':'%s'})"
                                                       % (database, id, namespace)).first()
                else:
                    self.persistence_object = QuerySet(self.persistence_class,
                                                       "db.%s.find({'_id':'%s', 'namespace':'%s', 'repository':'%s'})"
                                                       % (database, id, namespace, repository)).first()
        self.set_namespace(self.persistence_object.namespace)
        self.set_repository(self.persistence_object.repository)

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.namespace = self.namespace
        self.persistence_object.repository = self.repository
        self.persistence_object.save()

    def __str__(self):
        return "MongoREPO: (%s) :: %s [%s]" % (self.namespace, self.repository, self.persistence_object)


class MongoRepositoryFile(GenericRepositoryFile):

    contents = None
    language = None

    persistence_class = mongodb_models.RepositoryFileModel
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

    def retrieve(self, id=None, namespace=None, repository=None, file_path=None):
        database = 'gitEduDB'
        # TODO

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.file_path = self.file_path
        self.persistence_object.repository = self.repository
        self.persistence_object.contents = self.contents
        self.persistence_object.language = self.language
        self.persistence_object.save()

    def __str__(self):
        return "MongoRepoFile: (%s) :: %s :: %s :: %s [%s]" % (self.repository, self.file_path, self.language,
                                                               self.contents, self.persistence_object)


class MongoChange(GenericChange):

    persistence_class = mongodb_models.ChangeModel
    persistence_object = None

    def validate_repository(self, repository):
        validate_mongo_repository(repository)

    def retrieve(self, id=None, namespace=None, repository=None, change=None):
        database = 'gitEduDB'
        # TODO

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.timestamp = self.timestamp
        self.persistence_object.repository = self.repository
        self.persistence_object.author = self.author
        self.persistence_object.comment = self.comment
        self.persistence_object.save()

    def __str__(self):
        return "MongoChange: (%s) :: \"%s\" :: %s :: %s :: [%s]" % (self.repository, self.comment, self.author,
                                                                    self.timestamp, self.persistence_object)


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

    def retrieve(self, id=None, namespace=None, repository=None, change=None):
        database = 'gitEduDB'
        # TODO

    def save(self):
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.file_path = self.file_path
        self.persistence_object.change = self.change
        self.persistence_object.language = self.language
        self.persistence_object.contents = self.contents
        self.persistence_object.save()

    def __str__(self):
        return "MongoChangeFile: (%s) :: %s :: %s :: %s [%s]" % (self.change, self.file_path, self.language,
                                                               self.contents, self.persistence_object)


mongo_num_conn = 0

class MongoDBCodePersistenceBackend(CodePersistenceBackend):

    namespace_class = MongoNamespace
    repository_class = MongoRepository
    repository_file_class = MongoRepositoryFile
    change_class = MongoChange
    change_file_class = MongoChangeFile

    def __init__(self, profile=None):
        global mongo_num_conn
        if profile is None:
            raise ValueError("Connection Parameters can not be None")
        mongodb_connect.build_connection_from_settings(profile, 'mongo_%03d' % mongo_num_conn)
        mongo_num_conn = mongo_num_conn + 1

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
