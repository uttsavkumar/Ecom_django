from django.shortcuts import render,redirect ,get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate,login as loginFunction,logout as logoutFunction
from django.urls import reverse
# Create your views here.

def getCategory():
    cat = Category.objects.all()
    return cat

def home(r):
   
    cat = getCategory()
    prd = Product.objects.all()[:10]
    data = {'cat':cat,'prd':prd}
    return render(r,'ecommerce/home.html',data)

def catfilter(r,slug):
    cat = getCategory()
    prd = Product.objects.filter(category__slug = slug)
    category = Category.objects.get(slug = slug)
    data = {'cat':cat,'prd':prd,'catdata':category}

    return render(r,'ecommerce/home.html',data)


def search(r):
    search = r.POST.get('search')
    cat = getCategory()
    prd = Product.objects.filter(Q(slug__contains=search)|Q(name__contains=search)|Q(category__title__contains=search))
    data = {'cat':cat,'prd':prd}

    return render(r,'ecommerce/home.html',data)

def singlepage(r,id):
    cat = getCategory()
    prd = Product.objects.get(pk=id)
    data = {'cat':cat,'prd':prd}

    return render(r,'ecommerce/singlepage.html',data)


def login(r):
    cat = getCategory()
    form = AuthenticationForm(data=r.POST or None)
    data = {'cat':cat,'form':form}
    if r.method == 'POST':
        username =  r.POST.get('username')
        password =  r.POST.get('password')
        print(form)

        if form.is_valid():
            print(form)
            user = authenticate(username=username,password=password)
            if user is not None:
                print('user')

                loginFunction(r,user=user)
                return redirect(to='home')
            
    return render(r,'ecommerce/login.html',data)

def register(r):
    cat = getCategory()
    form = RegisterForm(r.POST or None)
    data = {'cat':cat,'form':form}

    if r.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(login)
        
    return render(r,'ecommerce/register.html',data)


def logout(r):
    logoutFunction(r)
    return redirect(home)

def addtocart(r,slug):
    prd = get_object_or_404(Product,slug = slug)
    
    order_item,created = OrderItem.objects.get_or_create(user=r.user,ordered=False,item=prd)
    order = Order.objects.filter(user = r.user,ordered = False)

    if order.exists():
        first_order = order[0]
        if first_order.items.filter(item__slug = slug).exists():
            order_item.qty += 1
            order_item.save()
            return redirect(cart)
        else:
            first_order.items.add(order_item)
    else:
        ord = Order.objects.create(user=r.user)
        ord.items.add(order_item)

        
    return redirect(home)

def reduceqty(r,slug):
    prd = get_object_or_404(Product,slug = slug)

    order_item = OrderItem.objects.get(user = r.user,ordered=False,item=prd)

    if order_item.qty != 1:
        order_item.qty -= 1
        order_item.save()
        return redirect(cart)
    else:
        order_item.delete()
        return redirect(cart)
def removeproduct(r,slug):
    prd = get_object_or_404(Product,slug = slug)
    order_item = OrderItem.objects.get(user = r.user,ordered=False,item=prd)

    if order_item:
        order_item.delete()
        return redirect(cart)

def cart(r):
    cat = getCategory()
    order = OrderItem.objects.filter(user=r.user,ordered = False)
    orde = Order.objects.get(user = r.user,ordered = False)
    data = {'order':order,'mainorder':orde,'cat':cat}
    return render(r,'ecommerce/cart.html',data)

from django.contrib import messages


def coupon(r):
    if r.method == 'POST':
        data = r.POST.get('coupon')
        try:
            cou = Coupon.objects.get(coupon = data)
            order = Order.objects.get(user = r.user,ordered = False)
            if cou:
                order.coupon = cou
                order.save()
                messages.success(r, 'Coupon applied!.')
                return redirect(cart)
            
        except:
            messages.success(r, 'Not a valid coupon!.')
            return redirect(cart)
        

def removecoupon(r):
    order = Order.objects.get(user = r.user,ordered = False)
    if order.coupon:
        order.coupon = None
        order.save()
        return redirect(cart)

def addAddress(r):
    if r.method == 'POST':
        add = Address()
        add.user = r.user
        add.state = r.POST.get('state')   
        add.city = r.POST.get('city')   
        add.pincode = r.POST.get('pincode')   
        add.last_name = r.POST.get('last_name')   
        add.first_name = r.POST.get('first_name')   
        add.contact = r.POST.get('contact')   
        add.type = r.POST.get('type')   
        add.address = r.POST.get('address')   
        if r.POST.get('address_optional') :
            add.address_optional = r.POST.get('address_optional')  

        add.save()
        return redirect(checkout)
         

def checkout(r):
    add = Address.objects.filter(user=r.user)
    order = Order.objects.get(user=r.user,ordered=False)
    data= {'address':add,'order':order}

    if r.method == 'POST':
        add = Address.objects.get(pk=r.POST.get('saved_address'))
        order = Order.objects.get(user=r.user,ordered = False)
        order.address = add
        order.save()
        return redirect(checkout)
        
    return render(r,'ecommerce/checkout.html',data)