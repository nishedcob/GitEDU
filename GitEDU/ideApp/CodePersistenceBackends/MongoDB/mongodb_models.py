
from pymongo.operations import IndexModel
from pymongo import TEXT
from pymodm import MongoModel
from pymodm.fields import CharField, ReferenceField, TimestampField

from bson import Timestamp

from ideApp import constants
from ideApp.CodePersistenceBackends.MongoDB import auto_connect
# from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, MONGODB_CONNECT_TO


class NamespaceModel(MongoModel):
    name = CharField()

    class Meta:
        indexes = [IndexModel('name', unique=True)]
        #connection_alias = 'mongo_000'

    def __str__(self):
        return "NamespaceMongoModel: %s" % self.name


class RepositoryModel(MongoModel):
    combo_id = CharField()
    name = CharField()
    namespace = ReferenceField(NamespaceModel)

    class Meta:
        #indexes = [IndexModel([('name', TEXT), ('namespace', TEXT)], unique=True)]
        #connection_alias = 'mongo_000'
        indexes = [IndexModel('combo_id', unique=True)]

    def __str__(self):
        return "RepositoryMongoModel: %s [%s]" % (self.name, self.namespace)

    @classmethod
    def build_combo_id(cls, name, namespace):
        if name is None:
            raise ValueError("Name can't be None")
        if namespace is None:
            raise ValueError("Namespace can't be None")
        return "%s/%s" % (namespace, name)

    def _build_combo_id(self):
        return self.build_combo_id(name=self.name, namespace=self.namespace.name)

    def set_combo_id(self):
        self.combo_id = self._build_combo_id()

    def save(self, cascade=None, full_clean=True, force_insert=False):
        self.set_combo_id()
        super().save(cascade=cascade, full_clean=full_clean, force_insert=force_insert)


class RepositoryFileModel(MongoModel):
    contents = CharField(required=False, blank=True)
    repository = ReferenceField(RepositoryModel)
    prog_language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()
    current_change_file = ReferenceField("ChangeFileModel", blank=True)

    class Meta:
        indexes = [IndexModel([('file_path', TEXT), ('repository', TEXT)], unique=True)]
        #connection_alias = 'mongo_000'

    '''
    class Meta:
        connection_alias = CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile']
    '''

    def __str__(self):
        return "RepositoryFileMongoModel: %s :: %s :: [%s] :: %s" % (self.file_path, self.prog_language,
                                                                     self.repository, self.contents)


class ChangeModel(MongoModel):
    change_id = CharField()
    comment = CharField()
    author = CharField()
    timestamp = TimestampField()
    repository = ReferenceField(RepositoryModel)
    parent_change = ReferenceField("ChangeModel", blank=True)

    class Meta:
        pass
        #connection_alias = 'mongo_000'

    def __str__(self):
        if isinstance(self.timestamp, Timestamp):
            timestamp = self.timestamp.as_datetime().__str__()
        else:
            timestamp = self.timestamp
        return "ChangeMongoModel: %s :: \"%s\" :: %s :: %s :: [%s]" % (self.change_id, self.comment, self.author,
                                                                       timestamp, self.repository)


class ChangeFileModel(MongoModel):
    contents = CharField()
    change = ReferenceField(ChangeModel)
    prog_language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()
    file = ReferenceField(RepositoryFileModel)

    class Meta:
        pass
        #connection_alias = 'mongo_000'

    def __str__(self):
        return "ChangeFileMongoModel: [%s] :: %s :: %s :: %s" % (self.change, self.file_path, self.prog_language,
                                                                 self.contents)


class TemporaryChangeFileModel(MongoModel):
    contents = CharField()
    repository = ReferenceField(RepositoryModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()

    class Meta:
        pass
        #connection_alias = 'mongo_000'

    def __str__(self):
        return "TemporaryChangeFileMongoModel: [%s] :: %s :: %s :: %s" % (self.repository, self.file_path,
                                                                          self.language, self.contents)
