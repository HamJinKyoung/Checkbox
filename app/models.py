from django.db import models

class Checkbox(models.Model):
    coursename = models.CharField(max_length=100)