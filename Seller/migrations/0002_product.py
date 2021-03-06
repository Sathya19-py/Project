# Generated by Django 2.2.18 on 2021-04-06 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Product_Name', models.CharField(max_length=20)),
                ('Product_Price', models.IntegerField()),
                ('Product_Quantity', models.IntegerField()),
                ('Product_Weight', models.IntegerField()),
                ('Product_Weight1', models.CharField(default=0, max_length=10)),
                ('Product_Description', models.CharField(max_length=500)),
                ('Product_Image', models.ImageField(upload_to='Products')),
                ('Product_Status', models.CharField(default='Active', max_length=20)),
                ('Seller', models.ManyToManyField(blank=True, null=True, to='Seller.Seller_Registration')),
            ],
        ),
    ]
