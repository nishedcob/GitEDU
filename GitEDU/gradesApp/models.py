from django.db import models

from academicApp.models import ClassroomStudent, AcademicCategory, AcademicSubCategory, AcademicAssignment
# Create your models here.

class StudentCategoryGrade(models.Model):
    classroomStudent = models.ForeignKey(ClassroomStudent, null=False)
    academicCategory = models.ForeignKey(AcademicCategory, null=False)
    grade = models.DecimalField(decimal_places=3, max_digits=6, null=True)

class StudentSubCategoryGrade(models.Model):
    classroomStudent = models.ForeignKey(ClassroomStudent, null=False)
    academicSubCategory = models.ForeignKey(AcademicSubCategory, null=False)
    grade = models.DecimalField(decimal_places=3, max_digits=6, null=True)

class StudentAssignmentGrade(models.Model):
    classroomStudent = models.ForeignKey(ClassroomStudent, null=False)
    academicAssignment = models.ForeignKey(AcademicAssignment, null=False)
    grade = models.DecimalField(decimal_places=3, max_digits=6, null=True)
