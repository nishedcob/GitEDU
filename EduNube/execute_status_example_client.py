
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


class EduNubeExecuteStatusHTTPConsumer:

    create_operation = 'create'
    status_operation = 'status'
    result_operation = 'result'

    url_template = "%s://%s:%d/api/execute/%s"

    def build_base_url(self, protocol, host, port, operation):
        return self.url_template % (protocol, host, port, operation)

    def build_inicial_payload(self):
        return dict()

    def post_url(self, url, payload):
        return requests.post(url, data=payload)

    def validate_url(self, url):
        return url


class ConfigEduNubeExecuteStatusHTTPConsumer(EduNubeExecuteStatusHTTPConsumer):

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

    def build_base_config_url(self, operation):
        return self.build_base_url(protocol=self.protocol, host=self.host, port=self.port, operation=operation)


class DefaultConfigEduNubeExecuteStatusHTTPConsumer(ConfigEduNubeExecuteStatusHTTPConsumer):
    protocol = EDUNUBE_CONFIG.get('protocol')
    host = EDUNUBE_CONFIG.get('host')
    port = EDUNUBE_CONFIG.get('port')
    token = EDUNUBE_CONFIG.get('token')


class EduNubeExecuteStatusConsumer(DefaultConfigEduNubeExecuteStatusHTTPConsumer):

    def _prepare_repo_suffix(self, language, namespace, repository):
        return "%s/%s/%s/" % (language, namespace, repository)

    def _prepare_id_suffix(self, language, id):
        return "%s/%s/" % (language, id)

    def _make_call(self, operation, suffix, payload=None):
        if payload is None:
            payload = self.build_inicial_payload()
        url = "%s/%s" % (self.build_base_config_url(operation=operation), suffix)
        return self.post_url(url=url, payload=payload)

    def create(self, language, namespace, repository):
        return self._make_call(
            operation=self.create_operation,
            suffix=self._prepare_repo_suffix(language=language, namespace=namespace, repository=repository)
        )

    def status(self, language, id):
        return self._make_call(
            operation=self.status_operation,
            suffix=self._prepare_id_suffix(language=language, id=id)
        )

    def result(self, language, id):
        return self._make_call(
            operation=self.result_operation,
            suffix=self._prepare_id_suffix(language=language, id=id)
        )


class EduNubeLanguageExecuteStatusConsumer(EduNubeExecuteStatusConsumer):

    language = None

    def create(self, namespace, repository, language=None):
        if language is None:
            language = self.language
        return super().create(language=language, namespace=namespace, repository=repository)

    def status(self, id, language=None):
        if language is None:
            language = self.language
        return super().status(language=language, id=id)

    def result(self, id, language=None):
        if language is None:
            language = self.language
        return super().result(language=language, id=id)


class EduNubeShellExecuteStatusConsumer(EduNubeLanguageExecuteStatusConsumer):
    language = 'shell'


class EduNubePy3ExecuteStatusConsumer(EduNubeLanguageExecuteStatusConsumer):
    language = 'python3'


class EduNubePGSQLExecuteStatusConsumer(EduNubeLanguageExecuteStatusConsumer):
    language = 'postgresql'
