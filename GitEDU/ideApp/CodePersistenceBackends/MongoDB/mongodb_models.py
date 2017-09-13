
from pymodm import MongoModel
from pymodm.fields import CharField, ReferenceField, TimestampField

from ideApp import constants
# from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, MONGODB_CONNECT_TO


class NamespaceModel(MongoModel):
    name = CharField()

    def __str__(self):
        return "NamespaceMongoModel: %s" % self.name


class RepositoryModel(MongoModel):
    name = CharField()
    namespace = ReferenceField(NamespaceModel)

    def __str__(self):
        return "RepositoryMongoModel: %s [%s]" % (self.name, self.namespace)


class RepositoryFileModel(MongoModel):
    contents = CharField()
    repository = ReferenceField(RepositoryModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()

    '''
    class Meta:
        connection_alias = CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile']
    '''

    def __str__(self):
        return "RepositoryFileMongoModel: %s :: %s :: [%s] :: %s" % (self.file_path, self.language, self.repository,
                                                                     self.contents)


class ChangeModel(MongoModel):
    comment = CharField()
    author = CharField()
    timestamp = TimestampField()
    repository = ReferenceField(RepositoryModel)

    def __str__(self):
        return "ChangeMongoModel: \"%s\" :: %s :: %s :: [%s]" % (self.comment, self.author, self.timestamp,
                                                                 self.repository)


class ChangeFileModel(MongoModel):
    contents = CharField()
    change = ReferenceField(ChangeModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()

    def __str__(self):
        return "ChangeFileMongoModel: [%s] :: %s :: %s :: %s" % (self.change, self.file_path, self.language,
                                                                 self.contents)

class TemporaryChangeFileModel(MongoModel):
    contents = CharField()
    repository = ReferenceField(RepositoryModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()

    def __str__(self):
        return "TemporaryChangeFileMongoModel: [%s] :: %s :: %s :: %s" % (self.repository, self.file_path,
                                                                          self.language, self.contents)
