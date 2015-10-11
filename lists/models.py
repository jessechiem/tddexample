from django.db import models

# Create your models here.
class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    # to save the relationship to the object itself,
    # we tell Django about the relationship between
    # the two classes using a ForeignKey
    list = models.ForeignKey(List, default=None)
