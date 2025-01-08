from django.db import models

from django.conf import settings

from django.contrib.auth.models import AbstractUser,User

from django.db.models.signals import post_save

from django.utils.timezone import now


class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    

class CustomUser(AbstractUser):

    role_choices=(
        ('farmer','farmer'),
        ('Buyer','Buyer')
    )


    role=models.CharField(max_length=20,choices=role_choices)
    

    def __str__(self):
        return self.username


class UserProfile(BaseModel):

    name=models.CharField(max_length=200,null=True)

    address=models.TextField()

    phone=models.CharField(max_length=200,null=True)

    email=models.EmailField()

    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="profile",null=False)
   

    def __str__(self) -> str:
        return f"{self.owner.username}-{self.owner.role}"


class Category(BaseModel):

    product_category=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.product_category


class Tag(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):

        return self.name



class Product(BaseModel):

    name=models.CharField(max_length=20)

    quantity=models.PositiveIntegerField()

    price=models.PositiveIntegerField()

    unit_choice=(
        ("k.g","k.g"),
        ("Gram","Gram"),
        ("box","box"),
        ("packet","packet")

    )

    unit=models.CharField(max_length=20,choices=unit_choice,default="k.g")

    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    product_category=models.ForeignKey(Category,on_delete=models.CASCADE)

    tags=models.ManyToManyField(Tag)

    image=models.ImageField(upload_to="product_images",null=True,blank=True)

    def __str__(self):

        return self.name




class Basket(BaseModel):

    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="cart")


class BasketItem(BaseModel):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(default=1)

    is_order_placed=models.BooleanField(default=False)

    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cart_item")


class Order(BaseModel):

    basket_item_objects=models.ManyToManyField(BasketItem)

    is_paid=models.BooleanField(default=False)

    order_id=models.CharField(max_length=200,null=True)

    buyer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_choices=(
        ("credit/debit Card","credit/debit Card"),
        ("UPI","UPI"),
        ("Cash on Delivery","Cash on Delivery")
    )

    payment_type=models.CharField(max_length=200,choices=payment_choices)

    delivery_address=models.TextField()

    estimated_delivery_date=models.DateTimeField(null=True)

    order_status=(
            ("pending","pending"),
            ("paid","paid"),
            ("cancelled","cancelled"),
            ("shipped","shipped")

        )
    
    status=models.CharField(max_length=200,choices=order_status,default="pending")

    

class  Review(BaseModel):

    buyer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    rating_choice=(
        ("1 star","1 star"),
        ("2 star","2 star"),
        ("3 star","3 star"),
        ("4 star","4 star"),
        ("5 star","5 star")
    )


    rating=models.CharField(max_length=20,choices=rating_choice,default="1 star")

    review_comment=models.TextField()



def create_user_profile(sender,instance,created,**kwargs):

    if created:

        UserProfile.objects.create(owner=instance)

post_save.connect(create_user_profile,sender=settings.AUTH_USER_MODEL)

def create_basket(sender,instance,created,**kwargs):

    if created:

        Basket.objects.create(owner=instance)


post_save.connect(create_basket,CustomUser)






