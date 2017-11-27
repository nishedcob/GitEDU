
from GitEDU.settings import GIT_SERVER_HTTP_ENDPOINT_CONFIG
import requests

url_template = "%s://%s:%d/api/%s/%s/%s"

#object_type = 'ns'
object_type = 'repo'
#operation = 'create'
operation = 'edit'
namespace = 'nishedcob2'
#new_namespace = None
new_namespace = 'nishedcob3'
repository = 'test'
new_repository = 'test2'
#object_path = "%s/" % namespace
object_path = "%s/%s/" % (namespace, repository)

url = url_template % (GIT_SERVER_HTTP_ENDPOINT_CONFIG.get('protocol'), GIT_SERVER_HTTP_ENDPOINT_CONFIG.get('host'),
                      GIT_SERVER_HTTP_ENDPOINT_CONFIG.get('port'), object_type, operation, object_path)

#payload = {'token': GIT_SERVER_HTTP_ENDPOINT_CONFIG.get('token')}
#payload = {'token': GIT_SERVER_HTTP_ENDPOINT_CONFIG.get('token'), 'new_namespace': new_namespace}
payload = {'token': GIT_SERVER_HTTP_ENDPOINT_CONFIG.get('token'), 'new_namespace': new_namespace, 'new_repository': new_repository}

print('url: %s' % url)
print('data: %s' % payload)

# Get CSRF Token -- No Longer Necessary
#r = requests.get(url=url)
#print("GET %s : %s" % (url, r))
#print("text: %s" % r.text)
#print("cookies: %s" % r.cookies)

# Failure
#payload['csrf_token'] = r.text
# Load CSRF Cookie from GET -- No Longer Necessary
#cookies = r.cookies
# Failure
#cookies['csrf'] = r.text

#print("new data: %s" % payload)

# Send CSRF Token in Payload -- No Longer Necessary
#r = requests.post(url=url, data=payload, cookies=cookies)
# Should return 200, everything OK
r = requests.post(url=url, data=payload)
# Should return 403 (because we don't send with JWT auth token)
#r = requests.post(url=url)
print("POST %s: %s" % (url, r))
