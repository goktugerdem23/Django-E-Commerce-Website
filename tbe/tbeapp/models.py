from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    user_comment= models.CharField(max_length=120)

    def __str__(self):
        return f"Customer name: {self.user}, Customer comment: {self.user_comment}"



class Seller(models.Model):
    seller_name = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Seller name: {self.seller_name.username}"






class Product(models.Model):
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    customer_comment = models.ManyToManyField(Customer,blank=True)
    product_image = models.ImageField(upload_to='product_image',blank=True,null=True)
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE,null=True) 
    

    def __str__(self):
        return self.name