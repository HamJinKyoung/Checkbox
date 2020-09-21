from django.db import models

# Create your models here.
class Option(models.Model):
    def __str__(self):
        return self.option_name

    option_name = models.CharField(max_length=200)
    option_price = models.IntegerField()

class Basket(models.Model):
    ototal_price = models.IntegerField()
    option_list = models.CharField(max_length=200)