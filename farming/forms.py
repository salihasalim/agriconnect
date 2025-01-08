from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,UserProfile,Product,Review,Order

class RegisterForm(UserCreationForm):

    class Meta:

        model=CustomUser

        fields=["username","email","password1","password2","role"]

        widgets={
            'role':forms.Select(attrs={
                'style':'width:100%; padding:10px;'
            })
        }
       
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # for role,field in self.fields.items():
        #     if isinstance(field.widget,forms.Select):
        #         field.widget.attrs['class']='form-control'

        # self.fields['role'].widget.attrs["class"]="form-select"
        self.fields['username'].help_text=""
        self.fields['password1'].help_text=""
        self.fields['password2'].help_text=""


class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()


class ProfileForm(forms.ModelForm):
    class Meta:

        model=UserProfile

        fields=["name","address","phone","email"]

        widgets={
            "name":forms.TextInput(attrs={'class':'form-control'}),
             
            "address":forms.TextInput(attrs={'class':'form-control'}),

            "phone":forms.NumberInput(attrs={'class':'form-control'}),

            "email":forms.EmailInput(attrs={'class':'form-control'})
        }




class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name","quantity","unit","price","product_category","tags","image"]
        labels={
            "category_object":"Category"
        }
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "quantity":forms.NumberInput(attrs={'class':'form-control'}),
            "image":forms.FileInput(attrs={'class':'form-control'}),
            "price":forms.NumberInput(attrs={'class':'form-control'}),
            "category_object":forms.Select(attrs={'class':'form-control form-select'})

        }

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name","quantity","unit","price","product_category","tags","image"]
        labels={
            "category_object":"Category"
        }
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "quantity":forms.NumberInput(attrs={'class':'form-control'}),
            "image":forms.FileInput(attrs={'class':'form-control'}),
            "price":forms.NumberInput(attrs={'class':'form-control'}),
            "category_object":forms.Select(attrs={'class':'form-control form-select'})

        } 


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=["product_object","rating","review_comment"]
        
        
        widgets = {
            'rating': forms.Select(attrs={'class':'form-control form-select'}),  
            'review_comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }


class PasswordResetForm(forms.Form):

    username=forms.CharField()

    email=forms.CharField()

    password1=forms.CharField()

    password2=forms.CharField()



class OrderForm(forms.ModelForm):

    class Meta:

        model=Order

        fields=['payment_type','delivery_address',]

        widgets={
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter delivery address'})
        }