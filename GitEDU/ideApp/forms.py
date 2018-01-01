from django.forms import Form, IntegerField, CharField, ChoiceField, Textarea, BooleanField

from . import constants


class CodeForm(Form):
    file_name = CharField(label="Nombre de Archivo:")
    language = ChoiceField(label="Lenguage de Programacion:", choices=constants.LANGUAGE_NAMES)
    code = CharField(label="", widget= Textarea({'hidden': ''}))

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


class NamespaceForm(Form):
    namespace = CharField(label="Namespace:", max_length=50)
