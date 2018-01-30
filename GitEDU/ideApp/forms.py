from django.forms import Form, IntegerField, CharField, ChoiceField, Textarea, BooleanField, HiddenInput

from . import constants


class CodeForm(Form):
    file_name = CharField(label="Nombre de Archivo:")
    language = ChoiceField(label="Lenguage de Programacion:", choices=constants.LANGUAGE_NAMES)
    code = CharField(label="", widget=Textarea({'hidden': ''}))

    class Meta:
        widgets = {

        }


class CodeGlobalPermissionsForm(Form):
    onlyAuthUsers = BooleanField(label="Solo permitir acceso por usuarios autenticados?", required=False)
    onlyCollaborators = BooleanField(label="Solo permitir acceso por usuarios explicitamente permitidos?", required=False)
    globalCanWrite = BooleanField(label="Acceso global al grupo definido anteriormente de escritura?", required=False)
    globalCanRead = BooleanField(label="Acceso global al grupo definido anteriormente de lectura?", required=False)
    globalCanExecute = BooleanField(label="Acceso global al grupo definido anteriormente de ejecucion?", required=False)
    globalCanDownload = BooleanField(label="Acceso global al grupo definido anteriormente de descargar?", required=False)


class AddCollaboratorForm(Form):
    user = CharField(label="Nombre de Usuario")
    canWrite = BooleanField(label="Permitir Escritura?", required=False)
    canRead = BooleanField(label="Permitir Lectura?", required=False)
    canExecute = BooleanField(label="Permitir Ejecucion?", required=False)
    canDownload = BooleanField(label="Permitir Descargar?", required=False)


namespace_field = CharField(label="Namespace:", max_length=50)
repository_field = CharField(label="Repository:", max_length=50)
file_path_field = CharField(label="Ruta de Archivo:", max_length=255)
language_field = ChoiceField(label="Lenguage de Programacion:", choices=constants.LANGUAGE_NAMES)


class NamespaceForm(Form):
    namespace = namespace_field


class RepositoryForm(Form):
    namespace = CharField(widget=HiddenInput)
    repository = repository_field


class FullRepositoryForm(Form):
    namespace = namespace_field
    repository = repository_field


class NewRepositoryFileForm(Form):
    namespace = CharField(widget=HiddenInput)
    repository = CharField(widget=HiddenInput)
    file_path = file_path_field
    language = language_field
