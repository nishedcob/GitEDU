
from ideApp.CodePersistenceBackends.generics import GenericNamespace, GenericRepository, GenericRepositoryFile,\
    GenericChange, GenericChangeFile,CodePersistenceBackend

from ideApp.CodePersistenceBackends.MongoDB import mongodb_models, mongodb_connect


class MongoNamespace(GenericNamespace):

    def save(self):
        pass

    def __str__(self):
        return "MongoNSPC: %s" % self.namespace


class MongoRepository(GenericRepository):

    def save(self):
        pass

    def __str__(self):
        return "MongoREPO: (%s) :: %s" % (self.namespace, self.repository)


class MongoRepositoryFile(GenericRepositoryFile):

    def save(self):
        pass

    def __str__(self):
        return "MongoRepoFile: (%s) :: %s" % (self.repository, self.file_path)


class MongoChange(GenericChange):

    def save(self):
        pass

    def __str__(self):
        return "Change: (%s) :: \"%s\" :: %s :: %s" % (self.repository, self.comment, self.author, self.timestamp)


class MongoChangeFile(GenericChangeFile):

    def save(self):
        pass

    def __str__(self):
        return "ChangeFile: (%s) :: %s" % (self.change, self.file_path)


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
