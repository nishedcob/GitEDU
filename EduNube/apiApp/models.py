from django.db import models

from authApp import constants

# Create your models here.


class RepoSpec(models.Model):
    parent_repo = models.CharField(max_length=constants.MAX_URL_LENGTH, blank=True, null=True, default=None)
    repo = models.CharField(max_length=constants.MAX_REPO_NAME_LENGTH, unique=True)
    secret_key = models.CharField(max_length=constants.SECRET_KEY_SIZE, unique=True)
    token = models.CharField(max_length=constants.REPOSPEC_TOKEN_SIZE, unique=True)
    token_algo = models.CharField(max_length=constants.MAX_ALGO_NAME_LENGTH, default=constants.DEFAULT_ALGO)

    def __str__(self):
        return "<RepoSpec: PR='%s' R='%s' SK='%s' TK='%s' TKA='%s'>" % (self.parent_repo, self.repo, self.secret_key,
                                                                        self.token, self.token_algo)


class JobSpec(models.Model):
    docker_image = models.CharField(max_length=constants.MAX_URL_LENGTH)
    git_repo = models.CharField(max_length=constants.MAX_URL_LENGTH)
    job_name = models.CharField(max_length=constants.MAX_NAME_LENGTH, unique=True)
    deterministic = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return "<JobSpec: DI='%s' GR='%s' JN='%s' DET='%s'>" % (self.docker_image, self.git_repo, self.job_name,
                                                                self.deterministic)


class JobNameCounter(models.Model):
    orig_job_name = models.CharField(max_length=constants.MAX_NAME_LENGTH, unique=True)
    job_count = models.IntegerField(default=0)

    def __str__(self):
        return "<JobNameCounter: OJN='%s' JC='%d'>" % (self.orig_job_name, self.job_count)
