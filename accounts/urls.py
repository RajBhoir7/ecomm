
#  Accounts app Urls
from accounts import views
from django.contrib import admin
from django.urls import path
from products import views as productViews



urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('activate/<email_token>',views.activate_email,name="activate_email"),
    path('add-to-cart/<uid>',productViews.add_to_cart,name='add_to_cart'),
    path('carts/',views.Cart_view,name='carts'),
    path('delete-cart/<cart_item_uid>/',views.remove_cart,name='remove_cart'),
    path('remove-coupon/<cart_id>/',views.remove_coupon,name='remove_coupon'),
    path('success/',views.success,name='success')
]
