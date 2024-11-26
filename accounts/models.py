from django.db import models
from base.models import BaseModel
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
from django.dispatch import receiver
from base.emails import send_account_activation_email
from products.models import Product,SizeVariant
from products.models import ProductImage,Product

class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=120,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def __str__(self) -> str:
        return self.user.username
    
    def get_cart_count(self,request):
        
        return CartItems.objects.filter(carts__is_paid=False,cart__user = self.user).count()
        

class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price =[]

        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.size_variant.price:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)

        return sum(price)
    


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.product.product_name
    
    def get_product_price(self):
        price = [self.product.price]

        if self.size_variant:
            size_varient_price = self.size_variant.price
            price.append(size_varient_price)  
        return sum(price)
    
   


@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance,email_token=email_token)
            email = instance.email
            send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)