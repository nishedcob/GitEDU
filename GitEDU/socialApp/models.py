from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    user = models.ForeignKey(User, null=False)


class Student(models.Model):
    person = models.ForeignKey(Person, null=False)


class Teacher(models.Model):
    person = models.ForeignKey(Person, null=False)


class Administrator(models.Model):
    person = models.ForeignKey(Person, null=False)


class Group(models.Model):
    name = models.CharField(max_length=50, null=False)


class GroupMembership(models.Model):
    person = models.ForeignKey(Person, null=False)
    group = models.ForeignKey(Group, null=False)
