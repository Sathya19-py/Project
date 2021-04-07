from django.db import models
from Seller.models import Product, Seller_Registration


# Create your models here.

class Farmer_Registration(models.Model):
    First_Name = models.CharField(max_length=150)
    Last_Name = models.CharField(max_length=150)
    Mobile_Number = models.IntegerField()
    Email_Id = models.EmailField()
    Password = models.CharField(max_length=120)

class Cart(models.Model):
    Farmer = models.ForeignKey(Farmer_Registration,on_delete=models.CASCADE, null=True, blank=True)
    Seller = models.ForeignKey(Seller_Registration, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    Quantity = models.IntegerField()
    Sub_Total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Delivery_Address(models.Model):
    Farmer = models.ForeignKey(Farmer_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Locality_Area = models.CharField(max_length=150)
    Landmark = models.CharField(max_length=150)
    City = models.CharField(max_length=150)
    State = models.CharField(max_length=150)
    Pin_Code = models.IntegerField()

class Order(models.Model):
    Order_Id = models.CharField(max_length=50,default="ABC",unique=True)
    Farmer = models.ForeignKey(Farmer_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Seller = models.ForeignKey(Seller_Registration, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    Quantity = models.IntegerField()
    Sub_Total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    Payment_Mode = models.CharField(default=0, max_length=100)
    Order_Status = models.CharField(max_length=100)
    Order_Date = models.DateTimeField(auto_now=True, auto_now_add=False)
    Status_Date = models.DateTimeField(auto_now=True, auto_now_add=False)
    Address = models.ForeignKey(Delivery_Address,on_delete=models.CASCADE, null=True, blank=True)

class Contact(models.Model):
    First_Name = models.CharField(max_length=150)
    Last_Name = models.CharField(max_length=150)
    Mobile_Number = models.IntegerField()
    Email_Id = models.EmailField()
    Message = models.TextField(max_length=1000)
