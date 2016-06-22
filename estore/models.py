from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)

class Item(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=100)
	category = models.ForeignKey(Category)
	price = models.IntegerField()
	amount = models.IntegerField()

class Cart(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    items = models.ManyToManyField(Item)