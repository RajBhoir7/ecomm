from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Profile,CartItems,Cart
from products.models import ProductImage,Product,Coupon
import razorpay


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = email)
        if user.exists():
            messages.warning(request, "Username already exits")
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email)
        
        user_obj.set_password(password)
        user_obj.save()
        messages.warning(request, "Mail sent to your Email")
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/register.html')



def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username = email)
        
        if not user.exists():
            messages.warning(request, "Account Not Found")
            return HttpResponseRedirect(request.path_info)
        
        user1 = authenticate(username=email,password=password)
        if user1:
            
            #account Verification Status Check
            if Profile.objects.filter(user__username=email)[0].is_email_verified != True:
                messages.warning(request, "Your account needs Verification")
                return HttpResponseRedirect(request.path_info)
                
            login(request,user1)
            return redirect('login')
        
        else:
            messages.warning(request, "Incorrect Password")
            return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/login.html')




def activate_email(request,email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('login')
    except Exception as e:
        return HttpResponse(request,'Invalid Email Verification')

def remove_cart(request,cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



from django.conf import settings
def Cart_view(request):   

    
    cart_obj = Cart.objects.get(is_paid=False,user=request.user)
    if request.method == 'POST':
        coupon = request.POST.get('coupon_code')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)

        if not coupon_obj.exists():
            messages.warning(request, "Invalid Coupon")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, "Coupon alredy exits")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_cart_total() < coupon_obj[0].min_amount:
            messages.warning(request, f"Amount should be greater than {coupon_obj[0].min_amount}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, f"Coupon is Expired")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, "Coupon applied")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        


    client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment = client.order.create({'amount':cart_obj.get_cart_total()*100,'currency':'INR','payment_capture':1})
    print('**************************')
    print(payment)
    print('**************************')
    cart_obj.razor_pay_order_id = payment['id']
    cart_obj.save()
    context = {'cart_items':CartItems.objects.filter(cart=Cart.objects.get(is_paid=False,user=request.user)),
               'cart':Cart.objects.get(is_paid=False,user=request.user),'payment':payment}
    return render(request,'accounts/carts.html',context)


def remove_coupon(request,cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request,'Coupon Removed!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
    #order_id = request.GET.get('order_id')
    cart = Cart.objects.get(user=request.user)
    cart.is_paid = True
    cart.delete()
    return HttpResponse('Paymetn success')