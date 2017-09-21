
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
                    print("WARNING: Only searching for repositories based on Repository, may find more than 1," +
                          " will only use the first found")
                    self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'repository':'%s'})"
                                                       % (database, repository)).first()
            else:
                if repository is None:
                    print("WARNING: Only searching for repositories based on Namespace, may find more than 1," +
                          " will only use the first found")
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
                    self.persistence_object = QuerySet(self.persistence_class,
                                                       "db.%s.find({'_id':'%s', 'namespace':'%s'})"
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
        database = 'gitEduDB'
        if id is None:
            if namespace is None:
                if repository is None:
                    if file_path is None:
                        raise ValueError("ID, Namespace, Repository and File_Path can't be None")
                    else:
                        print("WARNING: Only searching for files based on File_Path, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'file_path':'%s'})"
                                                           % (database, file_path)).first()
                else:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Repository, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'repository':'%s'})"
                                                           % (database, repository)).first()
                    else:
                        print("WARNING: Only searching for files based on Repository and File_Path," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'repository':'%s', 'file_path':'%s'})"
                                                           % (database, repository, file_path)).first()
            else:
                if repository is None:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Namespace, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'namespace':'%s'})"
                                                           % (database, namespace)).first()
                    else:
                        print("WARNING: Only searching for files based on Namespace and File_Path," +
                              "may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'namespace':'%s', 'file_path':'%s'})"
                                                           % (database, namespace, file_path)).first()
                else:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Namespace and Repository," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'namespace':'%s', 'repository':'%s'})"
                                                           % (database, namespace, repository)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'namespace':'%s', 'repository':'%s',
                                                           'file_path':'%s'})'''
                                                           % (database, namespace, repository, file_path)).first()
        else:
            if namespace is None:
                if repository is None:
                    if file_path is None:
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s'})"
                                                           % (database, id)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id':'%s',
                                                            'file_path':'%s'})'''
                                                           % (database, id, file_path)).first()
                else:
                    if file_path is None:
                        self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id':'%s',
                                                            'repository':'%s'})'''
                                                           % (database, id, repository)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'repository':'%s',
                                                           'file_path':'%s'})'''
                                                           % (database, id, repository, file_path)).first()
            else:
                if repository is None:
                    if file_path is None:
                        self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id':'%s',
                                                            'namespace':'%s'})'''
                                                           % (database, id, namespace)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'namespace':'%s',
                                                           'file_path':'%s'})'''
                                                           % (database, id, namespace, file_path)).first()
                else:
                    if file_path is None:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'namespace':'%s',
                                                           'repository':'%s'})'''
                                                           % (database, id, namespace, repository)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'namespace':'%s',
                                                           'repository':'%s', 'file_path':'%s'})'''
                                                           % (database, id, namespace, repository, file_path)).first()

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
        if id is None:
            if namespace is None:
                if repository is None:
                    if change is None:
                        raise ValueError("ID, Namespace, Repository and Change can't be None")
                    else:
                        print("WARNING: Only searching for files based on Change, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'change':'%s'})"
                                                           % (database, change)).first()
                else:
                    if change is None:
                        print("WARNING: Only searching for files based on Repository, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'repository':'%s'})"
                                                           % (database, repository)).first()
                    else:
                        print("WARNING: Only searching for files based on Repository and Change," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'repository':'%s', 'change':'%s'})"
                                                           % (database, repository, change)).first()
            else:
                if repository is None:
                    if change is None:
                        print("WARNING: Only searching for files based on Namespace, may find more than 1," +
                              " will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'namespace':'%s'})"
                                                           % (database, namespace)).first()
                    else:
                        print("WARNING: Only searching for files based on Namespace and Change," +
                              "may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'namespace':'%s', 'change':'%s'})"
                                                           % (database, namespace, change)).first()
                else:
                    if change is None:
                        print("WARNING: Only searching for files based on Namespace and Repository," +
                              " may find more than 1, will only use the first found")
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           "db.%s.find({'namespace':'%s', 'repository':'%s'})"
                                                           % (database, namespace, repository)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'namespace':'%s', 'repository':'%s',
                                                           'change':'%s'})'''
                                                           % (database, namespace, repository, change)).first()
        else:
            if namespace is None:
                if repository is None:
                    if change is None:
                        self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s'})"
                                                           % (database, id)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id':'%s',
                                                            'change':'%s'})'''
                                                           % (database, id, change)).first()
                else:
                    if change is None:
                        self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id':'%s',
                                                            'repository':'%s'})'''
                                                           % (database, id, repository)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'repository':'%s',
                                                           'change':'%s'})'''
                                                           % (database, id, repository, change)).first()
            else:
                if repository is None:
                    if change is None:
                        self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id':'%s',
                                                            'namespace':'%s'})'''
                                                           % (database, id, namespace)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'namespace':'%s',
                                                           'change':'%s'})'''
                                                           % (database, id, namespace, change)).first()
                else:
                    if change is None:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'namespace':'%s',
                                                           'repository':'%s'})'''
                                                           % (database, id, namespace, repository)).first()
                    else:
                        self.persistence_object = QuerySet(self.persistence_class,
                                                           '''db.%s.find({'_id':'%s', 'namespace':'%s',
                                                           'repository':'%s', 'change':'%s'})'''
                                                           % (database, id, namespace, repository, change)).first()

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

    def retrieve(self, id=None, namespace=None, repository=None, change=None, file_path=None):
        database = 'gitEduDB'
        if id is None:
            if namespace is None:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            raise ValueError("ID, Namespace, Repository, Change and File_Path can't be None")
                        else:
                            print("WARNING: Only searching for files based on File_Path, may find more than 1," +
                                  " will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'file_path':'%s'})"
                                                               % (database, file_path)).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Change, may find more than 1," +
                                  " will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'change':'%s'})"
                                                               % (database, change)).first()
                        else:
                            print("WARNING: Only searching for files based on Change and File_Path, " +
                                  "may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'change':'%s',
                                                                                        'file_path': '%s'})'''
                                                               % (database, change, file_path)).first()
                else:
                    if change is None:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Repository," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               "db.%s.find({'repository':'%s'})"
                                                               % (database, repository)).first()
                        else:
                            print("WARNING: Only searching for files based on Repository and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               "db.%s.find({'repository':'%s', 'file_path':'%s'})"
                                                               % (database, repository, file_path)).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Repository and Change," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               "db.%s.find({'repository':'%s', 'change': '%s'})"
                                                               % (database, repository, change)).first()
                        else:
                            print("WARNING: Only searching for files based on Repository, Change and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'repository':'%s', 'change': '%s',
                                                                    'file_path':'%s'})'''
                                                               % (database, repository, change, file_path)).first()
            else:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Namespace, may find more than 1," +
                                  " will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'namespace':'%s'})"
                                                               % (database, namespace)).first()
                        else:
                            print("WARNING: Only searching for files based on Namespace and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({
                                                                                            'namespace': '%s',
                                                                                            'file_path':'%s'})'''
                                                               % (database, namespace, file_path)).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Namespace and Change," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({
                                                                                            'namespace': '%s',
                                                                                            'change':'%s'})'''
                                                               % (database, namespace, change)).first()
                        else:
                            print("WARNING: Only searching for files based on Namespace, Change and File_Path, " +
                                  "may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({
                                                                                        'namespace': '%s',
                                                                                        'change':'%s',
                                                                                        'file_path': '%s'})'''
                                                               % (database, namespace, change, file_path)).first()
                else:
                    if change is None:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Namespace and Repository," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               "db.%s.find({'namespace': '%s', 'repository':'%s'})"
                                                               % (database, namespace, repository)).first()
                        else:
                            print("WARNING: Only searching for files based on Namespace, Repository and File_Path," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'namespace': '%s', 'repository':'%s',
                                                                    'file_path':'%s'})'''
                                                               % (database, namespace, repository, file_path)).first()
                    else:
                        if file_path is None:
                            print("WARNING: Only searching for files based on Namespace, Repository and Change," +
                                  " may find more than 1, will only use the first found")
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'namespace': '%s', 'repository':'%s',
                                                                    'change': '%s'})'''
                                                               % (database, namespace, repository, change)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'namespace': '%s', 'repository':'%s',
                                                                    'change': '%s', 'file_path':'%s'})'''
                                                               % (database, namespace, repository, change, file_path))\
                                                                    .first()
        else:
            if namespace is None:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'_id':'%s'})"
                                                               % (database, id)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id': '%s',"
                                                                                            'file_path':'%s'})'''
                                                               % (database, id, file_path)).first()
                    else:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class, "db.%s.find({'change':'%s'})"
                                                               % (database, change)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({'_id': '%s',
                                                                                        'change':'%s',
                                                                                        'file_path': '%s'})'''
                                                               % (database, id, change, file_path)).first()
                else:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               "db.%s.find({'_id': '%s', 'repository':'%s'})"
                                                               % (database, id, repository)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'repository':'%s',
                                                                    'file_path':'%s'})'''
                                                               % (database, id, repository, file_path)).first()
                    else:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'repository':'%s',
                                                                    'change': '%s'})'''
                                                               % (database, id, repository, change)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'repository':'%s',
                                                                    'change': '%s', 'file_path':'%s'})'''
                                                               % (database, id, repository, change, file_path)).first()
            else:
                if repository is None:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               "db.%s.find({'_id': '%s', 'namespace':'%s'})"
                                                               % (database, id, namespace)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({
                                                                                            'namespace': '%s',
                                                                                            'file_path':'%s'})'''
                                                               % (database, namespace, file_path)).first()
                    else:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({
                                                                                            '_id': '%s', 
                                                                                            'namespace': '%s',
                                                                                            'change':'%s'})'''
                                                               % (database, id, namespace, change)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class, '''db.%s.find({
                                                                                        '_id': '%s', 
                                                                                        'namespace': '%s',
                                                                                        'change':'%s',
                                                                                        'file_path': '%s'})'''
                                                               % (database, id, namespace, change, file_path)).first()
                else:
                    if change is None:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'namespace': '%s',
                                                                           'repository':'%s'})'''
                                                               % (database, id, namespace, repository)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'namespace': '%s',
                                                                    'repository':'%s',
                                                                    'file_path':'%s'})'''
                                                               % (database, id, namespace, repository, file_path))\
                                .first()
                    else:
                        if file_path is None:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'namespace': '%s',
                                                                    'repository':'%s', 'change': '%s'})'''
                                                               % (database, id, namespace, repository, change)).first()
                        else:
                            self.persistence_object = QuerySet(self.persistence_class,
                                                               '''db.%s.find({'_id': '%s', 'namespace': '%s',
                                                                    'repository':'%s', 'change': '%s',
                                                                    'file_path':'%s'})'''
                                                               % (database, id, namespace, repository, change,
                                                                  file_path)) \
                                .first()

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

    ALIAS_FORMAT = "mongo_%03d"

    def __init__(self, profile=None):
        global mongo_num_conn
        if profile is None:
            raise ValueError("Connection Parameters can not be None")
        self.alias = self.ALIAS_FORMAT % mongo_num_conn
        mongodb_connect.build_connection_from_settings(profile, self.alias)
        mongo_num_conn = mongo_num_conn + 1
        self.load_backend_db_object()

    def sync_namespaces(self):
        database = "gitEduDB"
        for namespace in self.namespaces:
            namespace.save()
        self.namespaces = QuerySet(mongodb_models.NamespaceModel, "db.%s.find({})" % database)

    def sync_repositories(self):
        database = "gitEduDB"
        for namespace, repositories in self.repositories.items():
            for repository in repositories:
                repository.save()
            self.repositories[namespace] = QuerySet(mongodb_models.RepositoryModel, "db.%s.find({})" % database)

    def sync_repository_files(self):
        database = "gitEduDB"
        for namespace, repositories in self.repository_files.items():
            for repository, repository_files in repositories.items():
                for repository_file in repository_files:
                    repository_file.save()
                self.repository_files[namespace][repository] = QuerySet(mongodb_models.RepositoryFileModel,
                                                                        "db.%s.find({})" % database)

    def sync_changes(self):
        database = "gitEduDB"
        for namespace, repositories in self.changes.items():
            for repository, changes in repositories.items():
                for change in changes:
                    change.save()
                self.changes[namespace][repository] = QuerySet(mongodb_models.ChangeModel, "db.%s.find({})" % database)

    def sync_change_files(self):
        database = "gitEduDB"
        for namespace, repositories in self.change_files.items():
            for repository, changes in repositories.items():
                for change, change_files in changes.items():
                    for change_file in change_files:
                        change_file.save()
                    self.change_files[namespace][repository][change] = QuerySet(mongodb_models.ChangeFileModel,
                                                                                "db.%s.find({})" % database)
