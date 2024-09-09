from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Profile




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
            login(request,user1)
            return redirect('/register')
        else:
            messages.warning(request, "Invalid Credintials")
            return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/login.html')





    