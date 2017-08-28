from django.db import models

from . import constants

from socialApp.models import Person, Group

# Create your models here.


class Repository(models.Model):
    namespace = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    owner = models.ForeignKey(Person, null=False)
    owning_group = models.ForeignKey(Group, null=True)


class File(models.Model):
    path = models.CharField(max_length=255, null=False)
    repository = models.ForeignKey(Repository, null=False)
    language = models.CharField(max_length=50, choices=constants.LANGUAGE_NAMES)


class RepositoryPersonMembership(models.Model):
    person = models.ForeignKey(Person, null=False)
    repository = models.ForeignKey(Repository, null=False)


class RepositoryGroupMembership(models.Model):
    group = models.ForeignKey(Group, null=False)
    repository = models.ForeignKey(Repository, null=False)
