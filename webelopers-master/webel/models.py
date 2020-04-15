from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Contact(models.Model):
    title = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Course(models.Model):
    department = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    group_number = models.IntegerField()
    course_number = models.IntegerField()

    teacher = models.CharField(max_length=50)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    exam_date = models.CharField(max_length=20)
    first_day = models.IntegerField()
    second_day = models.IntegerField()

    def __str__(self):
        return self.name


class UserAvatar(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.CharField(max_length=500)
