from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Works(models.Model):
    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/how-it-works')
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	
	class Meta:
		verbose_name_plural = 'categories' 
		
class Vehicles(models.Model):
	vehicle_model = models.CharField(max_length=100)
	rent_price = models.PositiveIntegerField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')

	def __str__(self):
		return self.vehicle_model


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)