from django.shortcuts import render
from products.models import Product,SizeVariant
from accounts.models import Cart,CartItems
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def get_product(request,slug):

    obj = Product.objects.get(slug=slug)
    context = {'obj' : obj}
    if request.GET.get('size'):
        size = request.GET.get('size')
        price = obj.get_product_price_by_size(size)
        context['selected_size'] = size
        context['updated_price'] = price
        
    return render(request,'products/products.html',context= context)
    

@login_required(login_url='http://127.0.0.1:8000/accounts/login/')
def add_to_cart(request,uid):
    varient = request.GET.get('varient')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user,is_paid = False)
    cart_item = CartItems.objects.create(cart=cart,product=product)
    
    if varient:
        varient = request.GET.get('varient')
        size_varient = SizeVariant.objects.get(size_name=varient)
        cart_item.size_variant = size_varient
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #  <---- Same Page Redirect
        