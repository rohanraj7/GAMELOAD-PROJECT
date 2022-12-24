from django.db import models



# Create your models here.




class Stock(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.CharField(max_length=10)
    stock = models.IntegerField()
    description = models.CharField(max_length=600)
    image1 = models.ImageField(upload_to='pics/')
    image2 = models.ImageField(upload_to='pics/')
    image3 = models.ImageField(upload_to='pics/')
    image4 = models.ImageField(upload_to='pics/')
    category = models.ForeignKey("gameadmin.Categories",on_delete= models.CASCADE)
    proOffer  = models.IntegerField(default=5)
    

class Banner(models.Model):
    heading = models.CharField(max_length=50)
    image   = models.ImageField(upload_to='pics/')
    description = models.CharField(max_length=500)    
    