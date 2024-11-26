#Products Urls


from django.urls import path
from products import views


urlpatterns = [
    path('get_product/<slug>',views.get_product,name='get_product'),
    
]
