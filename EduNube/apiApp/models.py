from django.db import models

from authApp import constants

# Create your models here.


class RepoSpec(models.Model):
    parent_repo = models.CharField(max_length=constants.MAX_URL_LENGTH, blank=True, null=True, default=None)
    repo = models.CharField(max_length=constants.MAX_REPO_NAME_LENGTH, unique=True)
    secret_key = models.CharField(max_length=constants.SECRET_KEY_SIZE, unique=True)
    token = models.CharField(max_length=constants.REPOSPEC_TOKEN_SIZE, unique=True)
    token_algo = models.CharField(max_length=constants.MAX_ALGO_NAME_LENGTH, default=constants.DEFAULT_ALGO)


class JobSpec(models.Model):
    docker_image = models.CharField(max_length=constants.MAX_URL_LENGTH)
    git_repo = models.CharField(max_length=constants.MAX_URL_LENGTH)
    job_name = models.CharField(max_length=constants.MAX_NAME_LENGTH, unique=True)
    deterministic = models.NullBooleanField(blank=True, null=True)


class JobNameCounter(models.Model):
    orig_job_name = models.CharField(max_length=constants.MAX_NAME_LENGTH, unique=True)
    job_count = models.IntegerField(default=0)
