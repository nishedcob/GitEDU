
import requests
import json

# Would normally be imported from settings, but for demonstration purposes:
#from EduNube.settings import EDUNUBE_CONFIG
EDUNUBE_CONFIG = {
    "protocol": "http",
    "host": "10.10.10.1",
    "port": 8010,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBfbmFtZSI6IkdpdEVEVSIsImV4cGlyZXMiOmZhbHNlLCJjcmVhdGVkX2RhdGUi"
             "OiIyMDE3LTExLTEyIDE3OjMzOjE3LjY0MTY4MSIsImVkaXRfZGF0ZSI6IjIwMTctMTEtMTIgMjA6MzY6NDAuMjc5NDAyIn0.825oh2rZU"
             "lIPZFaP_UbYPDpdsXTE0XCaNsia-3NnGuc"
}

base_url = "%s://%s:%d/api/execute" % (EDUNUBE_CONFIG.get('protocol'), EDUNUBE_CONFIG.get('host'), EDUNUBE_CONFIG.get('port'))

payload = {
    "token": EDUNUBE_CONFIG.get('token')
}

action = 'create'
language = 'python3'
namespace = 'nishedcob'
repository = 'test'

inicial_execution_url_repo_suffix = "%s/%s/%s/" % (language, namespace, repository)

inicial_execution_create_url = "%s/%s/%s" % (base_url, action, inicial_execution_url_repo_suffix)
print("Inicial Exec Create: POST %s" % inicial_execution_create_url)
inicial_execution_create = requests.post(inicial_execution_create_url, data=payload)
print("Inicial Exec Create Code: %d" % inicial_execution_create.status_code)
print("Inicial Exec Create Reply Data: %s" % inicial_execution_create.text)
inicial_execution_create_reply_data = json.loads(inicial_execution_create.text)
print("Inicial Exec Create Reply Data (JSON Loads): %s" % inicial_execution_create_reply_data)

print()
print("-------------------------------------------------------------------------")
print()

inicial_execution_id = inicial_execution_create_reply_data.get('id')
action = 'status'
inicial_execution_url_id_suffix = "%s/%s/" % (language, inicial_execution_id)

inicial_execution_status_url = "%s/%s/%s" % (base_url, action, inicial_execution_url_id_suffix)
print("Inicial Exec Status: POST %s" % inicial_execution_status_url)
inicial_execution_status = requests.post(inicial_execution_status_url, data=payload)
print("Inicial Exec Status Code: %d" % inicial_execution_status.status_code)
print("Inicial Exec Status Reply Data: %s" % inicial_execution_status.text)
inicial_execution_status_reply_data = json.loads(inicial_execution_status.text)
print("Inicial Exec Status Reply Data (JSON Loads): %s" % inicial_execution_status_reply_data)

print()
print("-------------------------------------------------------------------------")
print()

action = 'result'

inicial_execution_result_url = "%s/%s/%s" % (base_url, action, inicial_execution_url_id_suffix)
print("Inicial Exec Result: POST %s" % inicial_execution_result_url)
inicial_execution_result = requests.post(inicial_execution_result_url, data=payload)
print("Initial Exec Result Code: %d" % inicial_execution_result.status_code)
print("Inicial Exec Result Reply Data: %s" % inicial_execution_result.text)
inicial_execution_result_reply_data = json.loads(inicial_execution_result.text)
print("Inicial Exec Result Reply Data (JSON Loads): %s" % inicial_execution_result_reply_data)

