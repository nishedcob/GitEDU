
from pymodm import MongoModel
from pymodm.fields import CharField, IntegerField

from ideApp import constants
from GitEDU.settings import CODE_PERSISTENCE_BACKENDS, MONGODB_CONNECT_TO

class CodeModel(MongoModel):
    cmid = CharField()
    orig_cmid = CharField()
    uid = IntegerField()
    username = CharField()
    code = CharField()
    language = CharField(choices=constants.LANGUAGE_NAMES)
    file_name = CharField()

    class Meta:
        connection_alias = CODE_PERSISTENCE_BACKENDS[MONGODB_CONNECT_TO]['connection_profile']
