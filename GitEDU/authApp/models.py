from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.


class EquivalentUser(models.Model):
    normal_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name="equivalent_normal_user",
                                    null=False)
    lti_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name="equivalent_lti_user",
                                 null=False)

    def __str__(self):
        return "EqU: %s = %s" % (self.normal_user.username, self.lti_user.username)


class AuthenticationType(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return "AuT: %s" % self.name


class UserAuthentication(models.Model):
    authentication_type = models.ForeignKey(AuthenticationType, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "UAuTy: %s - %s" % (self.user.username, self.authentication_type.name)
