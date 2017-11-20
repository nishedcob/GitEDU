
from GitEDU.settings import EDUNUBE_CONFIG
import requests

url_template = "%s://%s:%d/api/execute/%s/%s/%s/%s"

lang = 'python3'
namespace = 'nishedcob'
repository = 'test'
file_path = 'folder/hello.py'

url = url_template % (EDUNUBE_CONFIG.get('protocol'), EDUNUBE_CONFIG.get('host'), EDUNUBE_CONFIG.get('port'), lang,
                      namespace, repository, file_path)

payload = {'token': EDUNUBE_CONFIG.get('token')}

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
