from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.EquivalentUser)
admin.site.register(models.AuthenticationType)
admin.site.register(models.UserAuthentication)
