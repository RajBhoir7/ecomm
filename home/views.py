from django.shortcuts import render
from products.models import Product
from django.core.paginator import Paginator

def index(request):
    Product_obj = Product.objects.all()
    paginator = Paginator(Product_obj, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    Product_name = request.GET.get('Search_product')
    if Product_name != '' and Product_name is not None:
        page_obj= Product.objects.filter(product_name__icontains=Product_name)
        
    return render(request,'home/index.html',{'products':page_obj})