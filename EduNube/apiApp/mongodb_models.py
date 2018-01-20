
from pymongo.operations import IndexModel
from pymongo import TEXT
from pymodm import MongoModel
from pymodm.fields import CharField, TimestampField, BooleanField, IntegerField

from bson import Timestamp

from apiApp import mongodb_auto_connect


class ExecutionLogModel(MongoModel):
    uniq_combo = CharField(primary_key=True)
    namespace = CharField()
    repository = CharField()
    commit_id = CharField()
    execution_number = IntegerField()
    stdout = CharField()
    stderr = CharField()
    deterministic = BooleanField()
    execution_time = TimestampField()

    class Meta:
        #indexes = [IndexModel([('namespace', TEXT), ('repository', TEXT), ('commit_id', TEXT),
        #                       ('execution_number', TEXT)], unique=True)]
        #connection_alias = 'mongo_000'
        pass

    def __str__(self):
        if isinstance(self.execution_time, Timestamp):
            execution_time = self.execution_time.as_datetime().__str__()
        else:
            execution_time = self.execution_time
        return "ExecutionLogMongoModel: %s/%s@%s#%s: [\"%s\", \"%s\"] %s@%s" % (self.namespace, self.repository,
                                                                                self.commit_id, self.execution_number,
                                                                                self.stdout, self.stderr,
                                                                                self.deterministic, execution_time)

    def build_uniq_combo(self):
        if self.namespace is None:
            raise ValueError("Namespace can't be None")
        if self.repository is None:
            raise ValueError("Repository can't be None")
        if self.commit_id is None:
            raise ValueError("Commit_ID can't be None")
        if self.execution_number is None:
            raise ValueError("Execution_Number can't be None")
        return "%s/%s@%s#%d" % (self.namespace, self.repository, self.commit_id, self.execution_number)

    def save_uniq_combo(self):
        self.uniq_combo = self.build_uniq_combo()

    def save(self, cascade=None, full_clean=True, force_insert=False):
        self.save_uniq_combo()
        super().save(cascade=cascade, full_clean=full_clean, force_insert=force_insert)
