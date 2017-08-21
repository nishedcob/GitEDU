from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.


class EquivalentUser(models.Model):
    normal_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name="equivalent_normal_user")
    lti_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name="equivalent_lti_user")
