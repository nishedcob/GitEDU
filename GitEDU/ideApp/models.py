from django.db import models

from . import constants

from socialApp.models import Person, Group

# Create your models here.


class Repository(models.Model):
    namespace = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    owner = models.ForeignKey(Person, null=True, blank=True)
    owning_group = models.ForeignKey(Group, null=True, blank=True)


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


class BackendType(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "%s" % self.name


class BackendAuthType(models.Model):
    name = models.CharField(max_length=255, null=False)


class BackendAuthData(models.Model):
    auth_type = models.ForeignKey(BackendAuthType, null=False)


class BackendUserAuth(models.Model):
    auth_data = models.ForeignKey(BackendAuthData, null=False)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)


class BackendTokenAuth(models.Model):
    auth_data = models.ForeignKey(BackendAuthData, null=False)
    username = models.CharField(max_length=255, null=False)
    token = models.CharField(max_length=255, null=False)


class Backend(models.Model):
    type = models.ForeignKey(BackendType, null=False)
    alias = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "%s :: '%s'" % (self.type, self.alias)


class MongoBackend(models.Model):
    backend = models.ForeignKey(Backend, null=True)
    database = models.CharField(max_length=255, null=False)


class GitBackend(models.Model):
    backend = models.ForeignKey(Backend, null=False)
    url = models.CharField(max_length=255, null=False)
    authentication_type = models.ForeignKey(BackendAuthType, null=False)
    auth_data = models.ForeignKey(BackendAuthData, null=True)


class GitLabBackend(models.Model):
    backend = models.ForeignKey(Backend, null=False)
    url = models.CharField(max_length=255, null=False)
    authentication_type = models.ForeignKey(BackendAuthType, null=False)
    auth_data = models.ForeignKey(BackendAuthData, null=True)


class GitRepoGitLabAssociations(models.Model):
    gitlab = models.ForeignKey(GitLabBackend)
    gitrepo = models.ForeignKey(GitBackend)


class BackendNamespace(models.Model):
    backend = models.ForeignKey(Backend, null=False)
    namespace = models.CharField(max_length=255, null=False)

