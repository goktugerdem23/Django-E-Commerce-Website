from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse,HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from . import models
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import CreateView,ListView
from .models import Product,Customer,Seller
from tbeapp.forms import ProductForm
from django.utils import timezone
from  .forms import SellerCreationForm,CustomerCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin



class ProductsListView(ListView):
    model = Product
    template_name = "tbeapp/product_list.html"
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context



class ProductCreateView(CreateView,LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = "tbeapp/add_product.html"
    success_url = reverse_lazy("tbeapp:product-list")
    def form_valid(self, form):
        seller = get_object_or_404(Seller,seller_name=self.request.user)
        form.instance.owner = seller
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs) :
        if not Seller.objects.filter(seller_name = request.user).exists():
            return HttpResponseForbidden("You cannot add a product without a seller account.")
        return super().dispatch(request, *args, **kwargs)
 


 
class PaymentView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"tbeapp/payment.html")


def add_comment(request,product_id):
    try:
     product = models.Product.objects.get(id=product_id)
    except models.Product.DoesNotExist:
        return redirect("tbeapp:product-list")
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        customer = models.Customer.objects.create(user = request.user, user_comment = comment_text)
        product.customer_comment.add(customer)
        return redirect("tbeapp:product-list")
    return render(request,"tbeapp/add_comment.html",{"product":product})

    

def delete_product(request,product_id):
    product = get_object_or_404(models.Product,id=product_id)
       
    if request.user == product.owner.seller_name:
        product.delete()
    else:
        return redirect("tbeapp:product-list")
    return redirect("tbeapp:product-list")





    


from django.shortcuts import get_object_or_404, redirect
from . import models


@login_required
def delete_comment(request, product_id, customer_id):
    
    product = get_object_or_404(models.Product, id=product_id)
    
  
    customer_comment = get_object_or_404(models.Customer, id=customer_id)

    if customer_comment in product.customer_comment.all():
        product.customer_comment.remove(customer_comment)

    return redirect("tbeapp:product-list")


class UpdateProduct(UpdateView,LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = "tbeapp/update_product.html"
    success_url = "/"
    def dispatch(self, request, *args, **kwargs) :
        if not Seller.objects.filter(seller_name = request.user).exists():
            return HttpResponseForbidden("You don't have persmission for this action")
        return super().dispatch(request, *args, **kwargs)
    


    
class SignupView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class SellerSignupView(CreateView):
    form_class = SellerCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/seller_signup.html"