from django.shortcuts import render
from products.models import Product
# Create your views here.

def get_product(request,slug):
    obj = Product.objects.get(slug=slug) 
    return render(request,'products/products.html',context={'obj':obj})