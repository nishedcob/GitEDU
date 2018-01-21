
import requests

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


class EduNubeRepoSpecHTTPconsumer:

    create_operation = "create"
    get_operation = "get"
    get_or_create_operation = "get_or_create"
    edit_operation = "edit"

    url_template = "%s://%s:%d/api/repospec/%s"

    def build_url(self, protocol, host, port, operation):
        return self.url_template % (protocol, host, port, operation)

    def build_inicial_payload(self):
        return dict()

    def post_url(self, url, payload):
        return requests.post(url, data=payload)

    def validate_url(self, url):
        return url


class ConfigEduNubeRepoSpecHTTPconsumer(EduNubeRepoSpecHTTPconsumer):

    protocol = None
    host = None
    port = None
    object_type = None
    token = None

    def __init__(self, protocol=None, host=None, port=None, object_type=None, token=None):
        self.protocol = self.protocol if protocol is None else protocol
        self.host = self.host if host is None else host
        self.port = self.port if port is None else port
        self.object_type = self.object_type if object_type is None else object_type
        self.token = self.token if token is None else token

    def build_inicial_payload(self):
        return {
            'token': self.token
        }

    def build_config_url(self, operation):
        return self.build_url(protocol=self.protocol, host=self.host, port=self.port, operation=operation)


class DefaultConfigEduNubeRepoSpecHTTPconsumer(ConfigEduNubeRepoSpecHTTPconsumer):
    protocol = EDUNUBE_CONFIG.get('protocol')
    host = EDUNUBE_CONFIG.get('host')
    port = EDUNUBE_CONFIG.get('port')
    token = EDUNUBE_CONFIG.get('token')


class EduNubeRepoSpecConsumer(DefaultConfigEduNubeRepoSpecHTTPconsumer):

    def _validate_findable(self, repo=None, repospec_token=None):
        if repo is None and repospec_token is None:
            raise ValueError("repo and repospec_token can't both be None")

    def _make_call(self, operation, payload):
        url = self.build_config_url(operation=operation)
        return self.post_url(url=url, payload=payload)

    def _if_not_none_add_to_payload(self, payload, payload_index, value):
        if value is not None:
            payload[payload_index] = value
        return payload

    def create(self, repo, parent_repo=None):
        payload = self.build_inicial_payload()
        payload['repo'] = repo
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='parent', value=parent_repo)
        return self._make_call(operation=self.create_operation, payload=payload)

    def get(self, repo=None, repospec_token=None):
        self._validate_findable(repo=repo, repospec_token=repospec_token)
        payload = self.build_inicial_payload()
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='repo', value=repo)
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='repospec_token', value=repospec_token)
        return self._make_call(operation=self.get_operation, payload=payload)

    def get_or_create(self, repo, parent_repo=None, repospec_token=None):
        payload = self.build_inicial_payload()
        payload['repo'] = repo
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='parent', value=parent_repo)
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='repospec_token', value=repospec_token)
        return self._make_call(operation=self.get_or_create_operation, payload=payload)

    def edit(self, repo=None, repospec_token=None, parent_repo=None, new_repo=None, regen_secret_key=False):
        self._validate_findable(repo=repo, repospec_token=repospec_token)
        payload = self.build_inicial_payload()
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='repo', value=repo)
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='repospec_token', value=repospec_token)
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='parent', value=parent_repo)
        payload = self._if_not_none_add_to_payload(payload=payload, payload_index='new_repo', value=new_repo)
        if type(regen_secret_key) == bool:
            payload['regen_secret_key'] = regen_secret_key
        return self._make_call(operation=self.edit_operation, payload=payload)
