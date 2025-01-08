from django.shortcuts import render,redirect,get_object_or_404

from django.urls import reverse_lazy

from farming.forms import RegisterForm,SignInForm,ProductForm,ReviewForm,PasswordResetForm,ProductUpdateForm,OrderForm,ProfileForm

from django.views.generic import View,FormView

from django.contrib.auth import authenticate,login,logout

from farming.models import UserProfile,Category,Product,Order,BasketItem

from django.contrib import messages

from django.db.models import Sum

from django.contrib.auth.decorators import login_required
import razorpay

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_exempt

from django.db.models.signals import post_save

from django.dispatch import receiver


from farming.decorators import signin_required


decs=[signin_required,never_cache]

from decouple import config

from twilio.rest import Client

def send_text_message():

    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+12199734046',
    to='+919633864123',
    body='You have csuccessfully registered in agriconnect'
    )


    print(message.sid)
    

def send_email():
    
    send_mail(
    "agriconnect Registration",
    "you are successfully registered in agriconnect,keep purchase",
    config('DEFAULT_FROM_EMAIL'),
    ["salihasalim3110@gmail.com"],
   
    fail_silently=False,
)






class HomePageView(View):

    template_name='home.html'

    def get(self,request,*args,**kwargs):

     return render(request,self.template_name)


class SignUpView(View):

    template_name='register.html'

    form_class=RegisterForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{'form':form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            send_email()
            
            send_text_message()

            return redirect ("signin")
        return render(request,self.template_name,{'form':form_instance})
            

class SignInView(FormView):

    template_name='signin.html'

    form_class=SignInForm

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get('username')

            pwd=form_instance.cleaned_data.get('password')

            # authenticate
            user_obj=authenticate(username=uname,password=pwd)

            

            if user_obj:

                login(request,user_obj)

                # redirect based on user_role
                if user_obj.role=='farmer':

                    return redirect('farmerdashboard')

                if user_obj.role=='Buyer':
                    return redirect('buyerdashboard')
                

        return render(request,self.template_name,{'form':form_instance})


@login_required
def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            print(request.user)
            if request.user.is_authenticated:
                profile.user = request.user
                
                profile.save()
                return redirect('view_profile')
    else:
        form = ProfileForm()
    return render(request, 'add_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = get_object_or_404(UserProfile, owner=request.user)

    return render(request,'view_profile.html',{'profile':profile})


class FarmerDashboardView(View):
    template_name='farmer_dashboard.html'
    def get(self,request,*args,**kwargs):
        qs=Product.objects.filter(owner=request.user)
        return render(request,self.template_name,{"crops":qs})


    

class BuyerDashboardView(View):
    template_name='buyer_dashboard.html'
    def get(self,request,*args,**kwargs):
         categories=Category.objects.all()
         selected_category=request.GET.get('category')
         if selected_category:
             products=Product.objects.filter(category_object=selected_category)
         else:
             products=Product.objects.all()
         return render(request,self.template_name,{})


class ProductView(View):
    template_name='product.html'
    form_class=ProductForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        
        return render(request,self.template_name,{'form':form_instance})
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST,files=request.FILES)
        if form_instance.is_valid():
            print(request.POST)
            # add owner to form
            form_instance.instance.owner=request.user
            
            if request.user.role=="farmer":
                form_instance.save()
                return redirect('farmerdashboard')
        return render(request,self.template_name,{'form':form_instance})


class ProductListView(View):
    template_name="productlist.html"

    def get(self,request,*args,**kwargs):

               
        qs=Product.objects.filter(owner=request.user)

        
        return render(request,self.template_name,{'product':qs})


class BuyerProductList(View):

    template_name="buyerproductlist.html"

    def get(self,request,*args,**kwargs):


        qs=Product.objects.all()

        return render(request,self.template_name,{'product':qs})







class ProductUpdateView(View):

    template_name="productupdate.html"

    form_class=ProductUpdateForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        form_instance=self.form_class(instance=product_obj)

        return render(request,self.template_name,{'form':form_instance}) 

 
    def post(self,request,*args,**kwargs):

        id =kwargs.get('pk')

        product_obj=Product.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=product_obj,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect('productlist')
            
        return render(request,self.template_name,{'form':form_instance}) 



class ProductDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Product.objects.get(id=id).delete()

        return redirect('productlist')


class ProductDetailView(View):

    template_name='productdetail.html'
    
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Product.objects.get(id=id)
        
        return render(request,self.template_name,{"product":qs})





class ReviewCreateView(View):

    template_name='review.html'

    form_class=ReviewForm

    def get(self,request,*args,**kwargs):
        
        form=self.form_class()

        return render(request,self.template_name,{'form':form})

    def post(self,request,*args,**kwargs):

        form=self.form_class(request.POST)

        if form.is_valid():

            form.instance.owner=request.user

            form.save()
            return redirect('buyer_dashboard')

        else:
            
             return render(request,self.template_name,{'form':form})



@method_decorator(decs,name="dispatch")
class AddToWishlistItemView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_object=get_object_or_404(Product,id=id)

        try:

            request.user.cart.cart_item.create(product_object=product_object)

            messages.success(request,"item has been added to wishlist")
            
            print("item added")

        
        except Exception as e:

            messages.error(request,"failed to add item ")


        return redirect("buyerproductlist")

@method_decorator(decs,name="dispatch")
class MyWishListItemsView(View):

    template_name="mywishlist.html"

    def get(self,request,*args,**kwargs):

       
        qs=request.user.cart.cart_item.filter(is_order_placed=False)

        total=qs.values("product_object").aggregate(total=Sum("product_object__price")).get("total")

        print("totalll",total)           


        return render(request,self.template_name,{"product":qs,"total":total})

@method_decorator(decs,name="dispatch")
class WishListItemDeleteView(View):

        def get(self,request,*args,**kwargs):

            id=kwargs.get("pk")

            request.user.cart.cart_item.get(id=id).delete()

            return redirect("mywishlist")


class OrderSummaryView(View):

    template_name="order_summary.html"

    form_class=OrderForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        qs=request.user.cart.cart_item.filter(is_order_placed=False)

        total=qs.values("product_object").aggregate(total=Sum("product_object__price")).get("total")

        return render(request,self.template_name,{"data":qs,"form":form_instance,"total":total})

    def post(self,request,args,*kwargs):

        form_instance=self.form_class(request.POST)    

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()






class PasswordResetView(View):

    template_name="passwordreset.html"

    form_class=PasswordResetForm


    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            email=form_instance.cleaned_data.get("email")

            password1=form_instance.cleaned_data.get("password1")

            password2=form_instance.cleaned_data.get("password2")

            

            try:
                assert password1==password2, "password mismatch"

                user_object=User.objects.get(username=username,email=email)

                user_object.set_password(password2)

                user_object.save()

                return redirect("signin")

            except Exception as e:

                messages.error(request,f"(e)")

                return render(request,self.template_name,{"form":form_instance})


        return render(request,self.template_name,{"form":form_instance})


class AboutView(View):

    def get(self,request,*args,**kwargs):

    

     return render(request,'about.html')



class CheckOutView(View):

    template_name="checkout.html"

    def get(self,request,*args,**kwargs):

        KEY_ID="rzp_test_1bsos7mtrvFh3G"

        KEY_SECRET="e0caKFDxuZNumeK6G2Ir4G1z"


        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        amount=request.user.cart.cart_item.filter(is_order_placed=False).values("product_object").aggregate(total=Sum("product_object__price")).get("total")

        data={"amount":amount*100,"currency":"INR","receipt":"order_rcptid_11"}

        payment=client.order.create(data=data)

        print("payment")

        order_id=payment.get("id")

        order_object=Order.objects.create(order_id=order_id,buyer=request.user)

        wishlist_items=request.user.cart.cart_item.filter(is_order_placed=False)

        for wi in wishlist_items:

            order_object.basket_item_objects.add(wi)

            wi.is_order_placed=True

            wi.save()

        return render(request,self.template_name,{"key_id":KEY_ID,"amount": amount,"order_id":order_id})

@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)
        KEY_ID=config('KEY_ID')

        KEY_SECRET=config('KEY_SECRET')

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        try:
            client.utility.verify_payment_signature(request.POST)
            print("success")
            
            order_id=request.POST.get("razorpay_order_id")

            Order.objects.filter(order_id=order_id).update(is_paid=True)
            
           
        except:
            print("failed")

        
        return redirect("orders")


@method_decorator(decs,name="dispatch")
class MyOrdersView(View):

    template_name="myorders.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)

        return render(request,self.template_name,{"data":qs})





class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('signin')


