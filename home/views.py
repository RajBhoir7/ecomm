from django.shortcuts import render
from products.models import Product


def index(request):
    return render(request,'home/index.html',{'products':Product.objects.all()})