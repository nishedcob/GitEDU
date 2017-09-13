
from pymodm import MongoModel
from pymodm.fields import CharField, ReferenceField, TimestampField

from ideApp import constants
# from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, MONGODB_CONNECT_TO


class NamespaceModel(MongoModel):
    name = CharField()


class RepositoryModel(MongoModel):
    name = CharField()
    namespace = ReferenceField(NamespaceModel)


class RepositoryFileModel(MongoModel):
    contents = CharField()
    repository = ReferenceField(RepositoryModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()

    '''
    class Meta:
        connection_alias = CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile']
    '''


class ChangeModel(MongoModel):
    comment = CharField()
    author = CharField()
    timestamp = TimestampField()
    repository = ReferenceField(RepositoryModel)


class ChangeFileModel(MongoModel):
    contents = CharField()
    change = ReferenceField(ChangeModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()


class TemporaryChangeFileModel(MongoModel):
    contents = CharField()
    repository = ReferenceField(RepositoryModel)
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_path = CharField()
