from django import forms
from django.forms import ModelForm
from tbeapp.models import Product,Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Seller

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","description","product_image"]




class SellerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
    
    def save(self,commit = True):
        user = super().save(commit=False)
        if commit:
            user.save()

            seller = Seller.objects.create(seller_name = user)
            seller.save()
        return user
    

class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
    

    def save(self, commit = True):
        user = super().save(commit=False)
        if commit:
            user.save()
            customer = Customer.objects.create(user = user)
            customer.save()
        return user
        