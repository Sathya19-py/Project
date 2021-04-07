from django.db import models


# Create your models here.

class Seller_Registration(models.Model):
    id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=150)
    Last_Name = models.CharField(max_length=150)
    Mobile_Number = models.IntegerField()
    Email_Id = models.EmailField()
    Shop_Name = models.CharField(max_length=150)
    Password = models.CharField(max_length=120)

    def __str__(self):
        return self.Email_Id


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    Seller = models.ManyToManyField(Seller_Registration, null=True, blank=True)
    Product_Name = models.CharField(max_length=20)
    Product_Price = models.IntegerField()
    Product_Quantity = models.IntegerField()
    Product_Weight = models.IntegerField()
    Product_Weight1 = models.CharField(max_length=10,default=0)
    Product_Description = models.CharField(max_length=500)
    Product_Image = models.ImageField(upload_to='Products')
    Product_Status = models.CharField(max_length=20,default='Active')

    def __str__(self):
        return self.Product_Name