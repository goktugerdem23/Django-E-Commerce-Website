from django.urls import path
from . import views
app_name = 'tbeapp'

urlpatterns = [
    path("",views.ProductsListView.as_view(),name='product-list'),
    path('signup/',views.SignupView.as_view(),name="signup"),
    path("add_product/",views.ProductCreateView.as_view(),name='add_product'),
    path("productcomment/<int:product_id>",views.add_comment,name="addcomment"),
    path("deletproduct/<int:product_id>",views.delete_product,name="deleteproduct"),
    path("sellersignup/",views.SellerSignupView.as_view(),name="sellersignup"),
    path("payment/",views.PaymentView.as_view(),name="payment"),
    path("deletecomment/<int:product_id>/<int:customer_id>/", views.delete_comment, name="deletecomment"),
    path("<pk>/updateproduct/",views.UpdateProduct.as_view(),name="updateproduct")


    
]
