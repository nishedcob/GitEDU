
import json

from execute_status_example_client import EduNubePy3ExecuteStatusConsumer

en_py3_es_consumer = EduNubePy3ExecuteStatusConsumer()

namespace = 'nishedcob'
repository = 'test'

inicial_execution_create = en_py3_es_consumer.create(namespace=namespace, repository=repository)

print("Inicial Exec Create Code: %d" % inicial_execution_create.status_code)
print("Inicial Exec Create Reply Data: %s" % inicial_execution_create.text)
inicial_execution_create_reply_data = json.loads(inicial_execution_create.text)
print("Inicial Exec Create Reply Data (JSON Loads): %s" % inicial_execution_create_reply_data)

print()
print("-------------------------------------------------------------------------")
print()

inicial_execution_id = inicial_execution_create_reply_data.get('id')

inicial_execution_status = en_py3_es_consumer.status(id=inicial_execution_id)

print("Inicial Exec Status Code: %d" % inicial_execution_status.status_code)
print("Inicial Exec Status Reply Data: %s" % inicial_execution_status.text)
inicial_execution_status_reply_data = json.loads(inicial_execution_status.text)
print("Inicial Exec Status Reply Data (JSON Loads): %s" % inicial_execution_status_reply_data)

print()
print("-------------------------------------------------------------------------")
print()

inicial_execution_result = en_py3_es_consumer.result(id=inicial_execution_id)
print("Initial Exec Result Code: %d" % inicial_execution_result.status_code)
print("Inicial Exec Result Reply Data: %s" % inicial_execution_result.text)
inicial_execution_result_reply_data = json.loads(inicial_execution_result.text)
print("Inicial Exec Result Reply Data (JSON Loads): %s" % inicial_execution_result_reply_data)

