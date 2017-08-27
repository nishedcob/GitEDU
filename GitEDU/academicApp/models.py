from django.db import models

from socialApp.models import Student, Teacher

# Create your models here.

class ClassSubject(models.Model):
    name = models.CharField(max_length=50, null=False)

class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    classSubject = models.ForeignKey(ClassSubject, null=True)

class Section(models.Model):
    name = models.CharField(max_length=50, null=False)

class Classroom(models.Model):
    course = models.ForeignKey(Course, null=False)
    section = models.ForeignKey(Section, null=False)

class ClassroomTeacher(models.Model):
    classroom = models.ForeignKey(Classroom, null=False)
    teacher = models.ForeignKey(Teacher, null=False)
    classroomGradeWeight = models.DecimalField(decimal_places=4, max_digits=5)
    relativeGradeWeight = models.DecimalField(decimal_places=3, max_digits=5, null=True)

class ClassroomStudent(models.Model):
    classroom = models.ForeignKey(Classroom, null=False)
    student = models.ForeignKey(Student, null=False)

class AcademicCategory(models.Model):
    name = models.CharField(max_length=50, null=False)
    categoryGradeWeight = models.DecimalField(decimal_places=4, max_digits=5)
    relativeGradeWeight = models.DecimalField(decimal_places=3, max_digits=5, null=True)
    classroomTeacher = models.ForeignKey(ClassroomTeacher, null=False)

class AcademicSubCategory(models.Model):
    name = models.CharField(max_length=50, null=False)
    subcategoryGradeWeight = models.DecimalField(decimal_places=4, max_digits=5)
    relativeGradeWeight = models.DecimalField(decimal_places=3, max_digits=5, null=True)
    academicCategory = models.ForeignKey(AcademicCategory, null=False)

class AcademicAssignment(models.Model):
    name = models.CharField(max_length=50, null=False)
    assignmentGradeWeight = models.DecimalField(decimal_places=4, max_digits=5)
    relativeGradeWeight = models.DecimalField(decimal_places=3, max_digits=5, null=True)
    academicSubCategory = models.ForeignKey(AcademicSubCategory, null=False)
