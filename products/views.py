from django.shortcuts import render
from products.models import Product
# Create your views here.

def get_product(request,slug):
    
    obj = Product.objects.get(slug=slug)
    context = {'obj' : obj}
    if request.GET.get('size'):
        size = request.GET.get('size')
        
        price = obj.get_product_price_by_size(size)
        context['selected_size'] = size
        context['updated_price'] = price
        
        print(price)
    return render(request,'products/products.html',context= context)
    