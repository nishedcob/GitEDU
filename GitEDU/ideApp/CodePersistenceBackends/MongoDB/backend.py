
from ideApp.models import BackendType

from ideApp.CodePersistenceBackends.generics import GenericNamespace, GenericRepository, GenericRepositoryFile,\
    GenericChange, GenericChangeFile, CodePersistenceBackend, validate_string

from ideApp.CodePersistenceBackends.MongoDB import mongodb_models, mongodb_connect

from pymodm.queryset import QuerySet
from pymodm.errors import DoesNotExist

from GitEDU.settings import CODE_PERSISTENCE_BACKENDS


def validate_mongo_repository(repository):
    if repository is None:
        raise ValueError("Repository can't be None")
    if not isinstance(repository, MongoRepository):
        raise ValueError("Repository should be a Repository Object")


def validate_mongo_change(change):
    if change is None:
        raise ValueError("Change can't be None")
    if not isinstance(change, MongoChange):
        raise ValueError("Change should be a Change Object")


class MongoNamespace(GenericNamespace):

    persistence_class = mongodb_models.NamespaceModel
    persistence_object = None

    def retrieve(self, id=None, namespace=None):
        if id is None:
            if namespace is None:
                raise ValueError("ID and Namespace can't be None")
            else:
                try:
                    namespace_db_obj = self.persistence_class.objects.raw({
                        'name': namespace
                    }).first()
                except DoesNotExist:
                    namespace_db_obj = self.persistence_class(name=namespace).save()
                self.persistence_object = namespace_db_obj
        else:
            if namespace is None:
                try:
                    namespace_db_obj = self.persistence_class.objects.raw({
                        '_id': id
                    }).first()
                except DoesNotExist:
                    namespace_db_obj = self.persistence_class(name=namespace).save()
                self.persistence_object = namespace_db_obj
            else:
                try:
                    namespace_db_obj = self.persistence_class.objects.raw({
                        '_id': id,
                        'name': namespace
                    }).first()
                except DoesNotExist:
                    namespace_db_obj = self.persistence_class(name=namespace).save()
                self.persistence_object = namespace_db_obj
        self.load_persisted_values()

    def save(self):
        self.retrieve(namespace=self.get_namespace())
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
        namespace_str = ""
        namespace_db_id = None
        if namespace is not None:
            if isinstance(namespace, str):
                namespace_str = namespace
            elif isinstance(namespace, MongoNamespace) or isinstance(namespace, GenericNamespace):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, MongoNamespace.persistence_class):
                namespace_str = namespace.name
            try:
                namespace_db_obj = mongodb_models.NamespaceModel.objects.raw({
                    'name': namespace_str
                }).first()
            except DoesNotExist:
                namespace_db_obj = MongoNamespace.persistence_class(name=namespace_str).save()
            namespace_db_id = namespace_db_obj._id
        if id is None:
            if namespace is None:
                if repository is None:
                    raise ValueError("ID, Namespace and Repository can't be None")
                else:
                    print("WARNING: Only searching for repositories based on Repository, may find more than 1," +
                          " will only use the first found")
                    try:
                        repository_db_obj = self.persistence_class.objects.raw({
                            'name': repository
                        }).first()
                    except DoesNotExist:
                        if repository is None:
                            raise ValueError("Can't create new repository without a Name")
                        if namespace_db_id is None:
                            raise ValueError("Can't create new repository without a Namespace")
                        repository_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
                    self.persistence_object = repository_db_obj
            else:
                if repository is None:
                    print("WARNING: Only searching for repositories based on Namespace, may find more than 1," +
                          " will only use the first found")
                    try:
                        repository_db_obj = self.persistence_class.objects.raw({
                            'namespace': namespace_db_id
                        }).first()
                    except DoesNotExist:
                        if namespace_db_id is None:
                            raise ValueError("Can't create new repository without a Namespace")
                        if repository is None:
                            raise ValueError("Can't create new repository without a Name")
                        repository_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
                    self.persistence_object = repository_db_obj
                else:
                    try:
                        repository_db_obj = self.persistence_class.objects.raw({
                            'namespace': namespace_db_id,
                            'name': repository
                        }).first()
                    except DoesNotExist:
                        if namespace_db_id is None:
                            raise ValueError("Can't create new repository without a Namespace")
                        if repository is None:
                            raise ValueError("Can't create new repository without a Name")
                        repository_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
                    self.persistence_object = repository_db_obj
        else:
            if namespace is None:
                if repository is None:
                    try:
                        repository_db_obj = self.persistence_class.objects.raw({
                            '_id': id
                        }).first()
                    except DoesNotExist:
                        if namespace_db_id is None:
                            raise ValueError("Can't create new repository without a Namespace")
                        if repository is None:
                            raise ValueError("Can't create new repository without a Name")
                        repository_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
                    self.persistence_object = repository_db_obj
            else:
                if repository is None:
                    try:
                        repository_db_obj = self.persistence_class.objects.raw({
                            '_id': id,
                            'namespace': namespace_db_id
                        }).first()
                    except DoesNotExist:
                        if namespace_db_id is None:
                            raise ValueError("Can't create new repository without a Namespace")
                        if repository is None:
                            raise ValueError("Can't create new repository without a Name")
                        repository_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
                    self.persistence_object = repository_db_obj
                else:
                    try:
                        repository_db_obj = self.persistence_class.objects.raw({
                            '_id': id,
                            'namespace': namespace_db_id,
                            'name': repository
                        }).first()
                    except DoesNotExist:
                        if namespace_db_id is None:
                            raise ValueError("Can't create new repository without a Namespace")
                        if repository is None:
                            raise ValueError("Can't create new repository without a Name")
                        repository_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
                    self.persistence_object = repository_db_obj
        self.load_persisted_values()

    def save(self):
        #print("namespace: %s" % self.get_namespace())
        self.retrieve(namespace=self.get_namespace(), repository=self.get_repository())
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.namespace = self.namespace.persistence_object
        self.persistence_object.name = self.repository
        self.persistence_object.save()

    def set_namespace(self, namespace):
        if isinstance(namespace, mongodb_models.NamespaceModel):
            new_namespace = create_dto_object_from_persistence_object(type="N", persistence_object=namespace,
                                                                      local_persistence_classes=
                                                                      global_persistence_classes,
                                                                      local_backend_data_classes=
                                                                      global_backend_data_classes)
            self.validate_namespace(namespace=new_namespace)
            self.namespace = new_namespace
        else:
            super(MongoRepository, self).set_namespace(namespace)

    def __str__(self):
        return "MongoREPO: (%s) :: %s [%s]" % (self.namespace, self.repository, self.persistence_object)

    def load_persisted_values(self):
        namespace = create_dto_object_from_persistence_object(type="N",
                                                              persistence_object=self.persistence_object.namespace)
        self.set_namespace(namespace)
        self.set_repository(self.persistence_object.name)


class MongoRepositoryFile(GenericRepositoryFile):

    persistence_class = mongodb_models.RepositoryFileModel
    persistence_object = None

    def validate_repository(self, repository):
        validate_mongo_repository(repository)

    def retrieve(self, id=None, namespace=None, repository=None, file_path=None):
        namespace_db_id = None
        namespace_str = None
        if namespace is not None:
            if isinstance(namespace, MongoNamespace) or isinstance(namespace, GenericNamespace):
                namespace_str = namespace.get_namespace()
            elif isinstance(namespace, mongodb_models.NamespaceModel):
                namespace_str = namespace.name
            elif isinstance(namespace, str):
                namespace_str = namespace
            else:
                raise ValueError("%s is an unrecognized type" % namespace)
            try:
                namespace_db_obj = mongodb_models.NamespaceModel.objects.raw({
                    'name': namespace_str
                }).first()
            except DoesNotExist:
                namespace_db_obj = MongoNamespace.persistence_class(name=namespace_str).save()
            namespace_db_id = namespace_db_obj._id
        repo_db_id = None
        if repository is not None:
            if isinstance(repository, MongoRepository) or isinstance(repository, GenericRepository):
                repository_str = repository.get_repository()
                repo_namespace = repository.get_namespace()
            elif isinstance(repository, mongodb_models.RepositoryModel):
                repository_str = repository.name
                repo_namespace = repository.namespace
            elif isinstance(repository, str):
                repository_str = repository
            else:
                raise ValueError("%s is an unrecognized type" % repository)
            if repo_namespace is not None:
                if namespace is not None:
                    if isinstance(repo_namespace, MongoNamespace) or isinstance(repo_namespace, GenericNamespace):
                        repo_namespace_str = repo_namespace.get_namespace()
                    elif isinstance(repo_namespace, mongodb_models.NamespaceModel):
                        repo_namespace_str = repo_namespace.name
                    elif isinstance(repo_namespace, str):
                        repo_namespace_str = repo_namespace
                    else:
                        raise ValueError("%s is an invalid type as the namespace for %s" % (repo_namespace, repository))
                    if namespace_str is not None and namespace_str != "" and namespace_str != repo_namespace_str:
                        raise ValueError("""%s and %s do not match in referenced namespace and therefore the current
                                            query is invalid""" % (namespace_str, repo_namespace_str))
            repo_db_obj = None
            if namespace_db_id is not None:
                try:
                    repo_db_obj = mongodb_models.RepositoryModel.objects.raw({
                        'name': repository_str,
                        'namespace': namespace_db_id
                    }).first()
                except DoesNotExist:
                    if namespace_db_id is None:
                        raise ValueError("Can't create new repository without a Namespace")
                    if repository is None:
                        raise ValueError("Can't create new repository without a Name")
                    repo_db_obj = self.persistence_class(name=repository, namespace=namespace_db_id).save()
            else:
                try:
                    repo_db_obj = self.persistence_class.objects.raw({
                        'name': repository_str
                    }).first()
                except DoesNotExist:
                    if namespace_db_id is None:
                        raise ValueError("Can't create new repository without a Namespace")
                    if repository is None:
                        raise ValueError("Can't create new repository without a Name")
            repo_db_id = repo_db_obj._id
        if id is None:
            if namespace is None:
                if repository is None:
                    if file_path is None:
                        raise ValueError("ID, Namespace, Repository and File_Path can't be None")
                    else:
                        print("WARNING: Only searching for files based on File_Path, may find more than 1," +
                              " will only use the first found")
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                else:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Repository, may find more than 1," +
                              " will only use the first found")
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'repository': repo_db_id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        print("WARNING: Only searching for files based on Repository and File_Path," +
                              " may find more than 1, will only use the first found")
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'repository': repo_db_id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
            else:
                if repository is None:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Namespace, may find more than 1," +
                              " will only use the first found")
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'repository': repo_db_id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        print("WARNING: Only searching for files based on Namespace and File_Path," +
                              "may find more than 1, will only use the first found")
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'repository': repo_db_id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                else:
                    if file_path is None:
                        print("WARNING: Only searching for files based on Namespace and Repository," +
                              " may find more than 1, will only use the first found")
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'repository': repo_db_id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                'repository': repo_db_id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
        else:
            if namespace is None:
                if repository is None:
                    if file_path is None:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                else:
                    if file_path is None:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repo_db_id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repo_db_id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
            else:
                if repository is None:
                    if file_path is None:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repo_db_id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repo_db_id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                else:
                    if file_path is None:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repo_db_id
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
                    else:
                        try:
                            repofile_db_obj = self.persistence_class.objects.raw({
                                '_id': id,
                                'repository': repo_db_id,
                                'file_path': file_path
                            }).first()
                        except DoesNotExist:
                            if repo_db_id is None:
                                raise ValueError("Can't create new RepositoryFile without a Repository")
                            if file_path is None:
                                raise ValueError("Can't create new RepositoryFile without a File_Path")
                            repofile_db_obj = self.persistence_class(repository=repo_db_id, file_path=file_path,
                                                                     contents='', prog_language='ot').save()
                        self.persistence_object = repofile_db_obj
            self.load_persisted_values()

    def save(self):
        if self.persistence_object is not None:
            persist_id = self.persistence_object._id
        else:
            persist_id = None
        self.retrieve(id=persist_id, namespace=self.get_repository().get_namespace(), repository=self.get_repository(),
                      file_path=self.get_file_path())
        if self.persistence_object is None:
            self.persistence_object = self.persistence_class()
        self.persistence_object.file_path = self.file_path
        self.persistence_object.repository = self.repository.persistence_object
        self.persistence_object.contents = self.contents
        self.persistence_object.language = self.language
        self.persistence_object.save()

    def set_repository(self, repository):
        if isinstance(repository, mongodb_models.RepositoryModel):
            new_repository = create_dto_object_from_persistence_object(type="R", persistence_object=repository,
                                                                       local_persistence_classes=
                                                                       global_persistence_classes,
                                                                       local_backend_data_classes=
                                                                       global_backend_data_classes)
            self.validate_repository(repository=new_repository)
            self.repository = new_repository
        else:
            super(MongoRepositoryFile, self).set_repository(repository)

    def __str__(self):
        return "MongoRepoFile: (%s) :: %s :: %s :: %s [%s]" % (self.repository, self.file_path, self.language,
                                                               self.contents, self.persistence_object)

    def load_persisted_values(self):
        self.set_repository(self.persistence_object.repository)
        self.set_contents(self.persistence_object.contents)
        self.set_file_path(self.persistence_object.file_path)
        self.set_language(self.persistence_object.prog_language)


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

    def set_repository(self, repository):
        if isinstance(repository, mongodb_models.RepositoryModel):
            new_repository = create_dto_object_from_persistence_object(type="R", persistence_object=repository,
                                                                       local_persistence_classes=
                                                                       global_persistence_classes,
                                                                       local_backend_data_classes=
                                                                       global_backend_data_classes)
            self.validate_repository(repository=new_repository)
            self.repository = new_repository
        else:
            super(MongoChange, self).set_repository(repository)

    def __str__(self):
        return "MongoChange: (%s) :: \"%s\" :: %s :: %s :: [%s]" % (self.repository, self.comment, self.author,
                                                                    self.timestamp, self.persistence_object)

    def load_persisted_values(self):
        self.set_repository(self.persistence_object.repository)
        self.set_author(self.persistence_object.author)
        self.set_comment(self.persistence_object.comment)
        self.set_id(self.persistence_object.implicit_id)


class MongoChangeFile(GenericChangeFile):

    persistence_class = mongodb_models.ChangeFileModel
    persistence_object = None

    def validate_change(self, change):
        validate_mongo_change(change)

    def retrieve(self, id=None, namespace=None, repository=None, change=None, file_path=None):
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

    def set_change(self, change):
        if isinstance(change, mongodb_models.ChangeModel):
            new_change = create_dto_object_from_persistence_object(type="C", persistence_object=change,
                                                                   local_persistence_classes=
                                                                   global_persistence_classes,
                                                                   local_backend_data_classes=
                                                                   global_backend_data_classes)
            self.validate_change(new_change)
            self.change = new_change
        else:
            super(MongoChangeFile, self).set_change(change)

    def __str__(self):
        return "MongoChangeFile: (%s) :: %s :: %s :: %s [%s]" % (self.change, self.file_path, self.language,
                                                               self.contents, self.persistence_object)

    def load_persisted_values(self):
        self.set_language(self.persistence_object.language)
        self.set_file_path(self.persistence_object.file_path)
        self.set_contents(self.persistence_object.contents)
        self.set_change(self.persistence_object.change)

global_persistence_classes = {
    'N': mongodb_models.NamespaceModel,
    'R': mongodb_models.RepositoryModel,
    'F': mongodb_models.RepositoryFileModel,
    'C': mongodb_models.ChangeModel,
    'f': mongodb_models.ChangeFileModel
}

global_backend_data_classes = {
    'N': MongoNamespace,
    'R': MongoRepository,
    'F': MongoRepositoryFile,
    'C': MongoChange,
    'f': MongoChangeFile
}

def create_list_from_persistence_list(type=None, persistence_list=None,
                                      local_persistence_classes=global_persistence_classes,
                                      local_backend_data_classes=global_backend_data_classes):
    if type is None:
        raise ValueError("Type can't be None")
    if persistence_list is None:
        raise ValueError("Persistence_List can't be None")
    if len(persistence_list):
        return []
    if isinstance(type, str):
        created_list = []
        # persistence_class = local_persistence_classes.get(type, None)
        backend_data_class = local_backend_data_classes.get(type, None)
        if backend_data_class is None:
            raise ValueError("Unrecognized Type '%s'" % type)
        for persistence_object in persistence_list:
            new_object = create_dto_object_from_persistence_object(type=type, persistence_object=persistence_object,
                                                                   local_persistence_classes=local_persistence_classes,
                                                                   local_backend_data_classes=local_backend_data_classes
                                                                   )
            created_list.append(new_object)
        return created_list
    else:
        raise ValueError("Type must be a string")


def create_dto_object_from_persistence_object(type=None, persistence_object=None,
                                              local_persistence_classes=global_persistence_classes,
                                              local_backend_data_classes=global_backend_data_classes):
    if type is None:
        raise ValueError("Type can't be None")
    if persistence_object is None:
        raise ValueError("Persistence_Object can't be None")
    if isinstance(type, str):
        # persistence_class = local_persistence_classes.get(type, None)
        backend_data_class = local_backend_data_classes.get(type, None)
        if backend_data_class is None:
            raise ValueError("Unrecognized Type '%s'" % type)
        attributes = {}
        if type == "N":
            # Namespace
            attributes['namespace'] = persistence_object.name
        elif type == "R":
            # Repository
            attributes['namespace'] = create_dto_object_from_persistence_object(type="N",
                                                                                persistence_object=persistence_object
                                                                                .namespace,
                                                                                local_persistence_classes=
                                                                                local_persistence_classes,
                                                                                local_backend_data_classes=
                                                                                local_backend_data_classes)
            attributes['repository'] = persistence_object.name
        elif type == "F":
            # Repository File
            attributes['repository'] = create_dto_object_from_persistence_object(type="R",
                                                                                 persistence_object=persistence_object
                                                                                 .repository,
                                                                                 local_persistence_classes=
                                                                                 local_persistence_classes,
                                                                                 local_backend_data_classes=
                                                                                 local_backend_data_classes)
            attributes['file_path'] = persistence_object.file_path
            attributes['contents'] = persistence_object.contents
            attributes['language'] = persistence_object.language
        elif type == "C":
            # Change
            attributes['id'] = persistence_object.id
            attributes['comment'] = persistence_object.comment
            attributes['author'] = persistence_object.author
            attributes['timestamp'] = persistence_object.timestamp
            attributes['repository'] = create_dto_object_from_persistence_object(type="R",
                                                                                 persistence_object=persistence_object
                                                                                 .repository,
                                                                                 local_persistence_classes=
                                                                                 local_persistence_classes,
                                                                                 local_backend_data_classes=
                                                                                 local_backend_data_classes)
        elif type == "f":
            # Change File
            attributes['file_path'] = persistence_object.file_path
            attributes['contents'] = persistence_object.contents
            attributes['language'] = persistence_object.language
            attributes['change'] = create_dto_object_from_persistence_object(type="C",
                                                                             persistence_object=persistence_object
                                                                             .change,
                                                                             local_persistence_classes=
                                                                             local_persistence_classes,
                                                                             local_backend_data_classes=
                                                                             local_backend_data_classes)
        new_object = backend_data_class(**attributes)
        new_object.persistence_object = persistence_object
        return new_object
    else:
        raise ValueError("Type must be a string")


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

    persistence_classes = {
        'N': mongodb_models.NamespaceModel,
        'R': mongodb_models.RepositoryModel,
        'F': mongodb_models.RepositoryFileModel,
        'C': mongodb_models.ChangeModel,
        'f': mongodb_models.ChangeFileModel
    }

    backend_data_classes = {
        'N': namespace_class,
        'R': repository_class,
        'F': repository_file_class,
        'C': change_class,
        'f': change_file_class
    }

    def create_dto_object_from_persistence_object(self, type=None, persistence_object=None,
                                                  local_persistence_classes=None, local_backend_data_classes=None):
        if local_persistence_classes is None:
            local_persistence_classes = self.persistence_classes
        if local_backend_data_classes is None:
            local_backend_data_classes = self.backend_data_classes
        return create_dto_object_from_persistence_object(type=type, persistence_object=persistence_object,
                                                         local_persistence_classes=local_persistence_classes,
                                                         local_backend_data_classes=local_backend_data_classes)

    def create_list_from_persistence_list(self, type=None, persistence_list=None, local_persistence_classes=None,
                                          local_backend_data_classes=None):
        if local_persistence_classes is None:
            local_persistence_classes = self.persistence_classes
        if local_backend_data_classes is None:
            local_backend_data_classes = self.backend_data_classes
        return create_list_from_persistence_list(type=type, persistence_list=persistence_list,
                                                 local_persistence_classes=local_persistence_classes,
                                                 local_backend_data_classes=local_backend_data_classes)

    def sync_namespaces(self):
        print("Namespaces: %s" % self.namespaces)
        for namespace in self.namespaces:
            namespace.save()
        persisted_namespaces = list(mongodb_models.NamespaceModel.objects.raw({}))
        self.namespaces = self.create_list_from_persistence_list(type="N", persistence_list=persisted_namespaces)
        print("Namespaces: %s" % self.namespaces)

    def sync_repositories(self):
        print("Repositories: %s" % self.repositories)
        for namespace in self.namespaces:
            if self.repositories.get(namespace, None) is None:
                self.repositories[namespace.namespace] = []
        for namespace, repositories in self.repositories.items():
            for repository in repositories:
                repository.save()
            #print("Namespace = %s", namespace)
            if isinstance(namespace, str):
                namespace_str = namespace
            elif isinstance(namespace, self.namespace_class):
                namespace_str = namespace.namespace
            else:
                print("WARNING: Namespace is an Invalid Type (%s)" % namespace)
                continue
            print("Namespace_Str = %s" % namespace_str)
            persisted_nspc_repos = list(mongodb_models.RepositoryModel.objects.raw({'namespace.name': namespace_str}))
            self.repositories[namespace_str] = self.create_list_from_persistence_list(type="R",
                                                                                  persistence_list=persisted_nspc_repos)
        print("Repositories: %s" % self.repositories)

    def sync_repository_files(self):
        print("Repository Files: %s" % self.repository_files)
        for namespace in self.list_namespaces():
            if self.repository_files.get(namespace, None) is None:
                self.repository_files[namespace] = {}
            print("namespace = %s" % namespace)
            for repository in self.list_repositories(namespace.namespace):
                if self.repository_files[namespace.namespace].get(repository.repository, None) is None:
                    self.repository_files[namespace.namespace][repository.repository] = []
        for namespace, repositories in self.repository_files.items():
            for repository, repository_files in repositories.items():
                for repository_file in repository_files:
                    repository_file.save()
                if isinstance(repository, str):
                    repository = self.build_repository(namespace=namespace, repository=repository)
                persisted_nspc_repo_files = list(mongodb_models.RepositoryFileModel.objects.raw({
                    'repository.name': repository.repository
                }))
                self.repository_files[namespace][repository.repository] = self.create_list_from_persistence_list(
                    type="F", persistence_list=persisted_nspc_repo_files)
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
                persisted_nspc_repo_changes = list(mongodb_models.ChangeModel.objects.raw({
                    'repository': repository
                }))
                self.changes[namespace][repository] = self.create_list_from_persistence_list(type="C", persistence_list=
                                                                                            persisted_nspc_repo_changes)
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
                    persisted_nspc_repo_chg_files = list(mongodb_models.ChangeFileModel.objects.raw(
                        {'change': change}
                    ))
                    self.change_files[namespace][repository][change] = self.create_list_from_persistence_list(type="f",
                                                                                                    persistence_list=
                                                                                        persisted_nspc_repo_chg_files)
        print("Change Files: %s" % self.change_files)
