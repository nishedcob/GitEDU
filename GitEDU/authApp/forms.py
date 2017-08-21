from django.contrib.auth.models import User
from django.db.models import TextField
from django.forms import ModelForm, PasswordInput

class RegistrationForm(ModelForm):
    confirm_password = TextField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': PasswordInput(),
            'confirm_password': PasswordInput(),
        }
