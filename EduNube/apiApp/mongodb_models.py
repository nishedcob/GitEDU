
from pymongo.operations import IndexModel
from pymongo import TEXT
from pymodm import MongoModel
from pymodm.fields import CharField, TimestampField, BooleanField, IntegerField

from bson import Timestamp

from apiApp import mongodb_auto_connect


class ExecutionLogModel(MongoModel):
    namespace = CharField()
    repository = CharField()
    commit_id = CharField()
    execution_number = IntegerField()
    stdout = CharField()
    stderr = CharField()
    deterministic = BooleanField()
    execution_time = TimestampField()

    class Meta:
        indexes = [IndexModel([('namespace', TEXT), ('repository', TEXT), ('commit_id', TEXT),
                               ('execution_number', TEXT)], unique=True)]
        #connection_alias = 'mongo_000'

    def __str__(self):
        if isinstance(self.execution_time, Timestamp):
            execution_time = self.execution_time.as_datetime().__str__()
        else:
            execution_time = self.execution_time
        return "ExecutionLogMongoModel: %s/%s@%s#%s: [\"%s\", \"%s\"] %s@%s" % (self.namespace, self.repository,
                                                                                self.commit_id, self.execution_number,
                                                                                self.stdout, self.stderr,
                                                                                self.deterministic, execution_time)

