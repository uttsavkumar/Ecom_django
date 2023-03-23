
from django.contrib import admin
from django.urls import path
from shop.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('category/<slug>/',catfilter,name='filter'),
    path('search/',search,name='search'),
    path('singlepage/<int:id>/',singlepage,name='singlepage'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('register/',register,name='register'),
    path('addtocart/<slug>/',addtocart,name='addtocart'),
    path('reduceitem/<slug>/',reduceqty,name='reducequantity'),
    path('removeproduct/<slug>/',removeproduct,name='removeproduct'),
    path('cart/',cart,name='cart'),
    path('coupon/',coupon,name='coupon'),
    path('removecoupon/',removecoupon,name='removecoupon'),
    path('checkout/',checkout,name='checkout'),
    path('addAddress/',addAddress,name='addAddress'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
