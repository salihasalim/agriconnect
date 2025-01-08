"""
URL configuration for agriconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from farming import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='signup'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    path('farmerdashboard/',views.FarmerDashboardView.as_view(),name='farmerdashboard'),
    path('buyerdashboard/',views.BuyerDashboardView.as_view(),name='buyerdashboard'),
    path('product/add/',views.ProductView.as_view(),name='productadd'),
    path('home/',views.HomePageView.as_view(),name='home'),
    path('signout/',views.SignOutView.as_view(),name='signout'),
    path("productlist/",views.ProductListView.as_view(),name='productlist'),
    path("buyerproductlist/",views.BuyerProductList.as_view(),name="buyerproductlist"),
    path("product/<int:pk>/change",views.ProductUpdateView.as_view(),name="productupdate"),
    path("product/<int:pk>/detail",views.ProductDetailView.as_view),
    path('product/<int:pk>/delete',views.ProductDeleteView.as_view,name='remove'),
    path("passwordreset/",views.PasswordResetView.as_view(),name='reset'),
    path("product/<int:pk>/addwishlist",views.AddToWishlistItemView.as_view(),name='addwishlist'),
    path('about/',views.AboutView.as_view(),name='about'),
    path("mywishlist/",views.MyWishListItemsView.as_view(),name="mywishlist"),
    path("wishlist/remove/<int:pk>/",views.WishListItemDeleteView.as_view(),name="wishlist-remove"),
    path("order/",views.OrderSummaryView.as_view(),name='order'),
    path("checkout/",views.CheckOutView.as_view(),name='checkout'),
    path('add-profile/', views.add_profile, name='add_profile'),
    path('view-profile/', views.view_profile, name='view_profile'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)















    
