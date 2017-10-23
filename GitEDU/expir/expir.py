
from ideApp.CodePersistenceBackends.MongoDB.mongodb_models import ChangeModel, ChangeFileModel, NamespaceModel,\
    RepositoryModel, RepositoryFileModel
from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager

manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)

print("code persistence backend manager: <%s>" % manager)

namespace = "nishedcob"
repository = "test"
file_path = "folder/hello.py"

manager.sync_all()

namespace_objs = manager.get_namespace(namespace=namespace)
