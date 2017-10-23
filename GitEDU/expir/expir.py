
from pymongo import ASCENDING, DESCENDING
from ideApp.CodePersistenceBackends.MongoDB.mongodb_models import ChangeModel, ChangeFileModel, NamespaceModel,\
    RepositoryModel, RepositoryFileModel
from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager

manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)

print("code persistence backend manager: <%s>" % manager)

print("Changes in Ascending Order:")
for change in list(ChangeModel.objects.raw({}).order_by([("timestamp", ASCENDING)])):
    print(change)

print("Changes in Descending Order:")
for change in list(ChangeModel.objects.raw({}).order_by([("timestamp", DESCENDING)])):
    print(change)

namespace = "nishedcob"
repository = "test"
file_path = "folder/hello.py"

manager.sync("NRF")
namespace_objs = manager.get_namespace(namespace=namespace)
print(namespace_objs)
namespace_obj = manager.select_preferred_backend_object(result_set=namespace_objs)
print(namespace_obj)
repository_objs = manager.get_repository(namespace=namespace_obj, repository=repository)
print(repository_objs)
repository_obj = manager.select_preferred_backend_object(result_set=repository_objs)
print(repository_obj)
repository_file_objs = manager.get_file(namespace=namespace_obj, repository=repository_obj, file_path=file_path)
print(repository_file_objs)
repository_file_obj = manager.select_preferred_backend_object(result_set=repository_file_objs)
print(repository_file_obj)
print(repository_file_obj.persistence_object)
print(repository_file_obj.persistence_object.pk)
file_edits = ChangeFileModel.objects.raw({
    'file': repository_file_obj.persistence_object.pk,
    'file_path': file_path
})
print(list(file_edits))
edits = []
for file_edit in file_edits:
    print(file_edit.change.pk)
    change = ChangeModel.objects.raw({'_id': file_edit.change.pk}).first()
    print(change)
    edit = {
        'id': change.change_id,
        'author': change.author,
        'timestamp': change.timestamp.as_datetime().__str__(),
        'namespace': namespace,
        'repository': repository,
        'file_path': file_edit.file_path
    }
    print(edit)
    edits.append(edit)
    print(edits)
print(edits)
edits = edits.sort(key=lambda k: k['timestamp'])
print(edits)

'''
from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager

manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)

print("code persistence backend manager: <%s>" % manager)

namespace = "nishedcob"
repository = "test"
file_path = "folder/hello.py"

manager.sync_all()

namespace_objs = manager.get_namespace(namespace=namespace)
'''
