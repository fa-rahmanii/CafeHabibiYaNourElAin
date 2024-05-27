from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class User(models.Model):
  username = models.CharField(max_length=255, unique=True)
  full_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  phone_number = models.IntegerField()

class Admin(models.Model):
  username = models.CharField(max_length=255, unique=True)
  email = models.CharField(max_length=255, unique=True)
  password = models.CharField(max_length=255)

class Product(models.Model):
  name = models.CharField(max_length=255)

class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  purchase_amount = models.IntegerField()

# Since the table schema doesn't specify data types, assuming binary(10) as boolean field  
class Storage(models.Model):
  type = models.BooleanField()
  name = models.CharField(max_length=255)
  amount = models.IntegerField()




class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField()

class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    storage = models.IntegerField()
    type = models.BinaryField(max_length=1)
    price = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_amount = models.IntegerField()

class AdditionalProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
