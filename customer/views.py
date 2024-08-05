import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import *

# Create your views here.
# 
#@login_required(login_url = "/login/")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username!!!')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.error(request, 'Invalid password!!!')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')
    return render(request, 'customer/login.html')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, 'User already exists!!')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        
        messages.info(request, 'Account created successfully')
        return redirect('/login/')
    return render(request, 'customer/register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class Home(View,User):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/home.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        #get items from every category
        appetizers = MenuItems.objects.filter(category__name__icontains='Appetizer')
        entres = MenuItems.objects.filter(category__name__icontains='Entre')
        desserts = MenuItems.objects.filter(category__name__icontains='Dessert')
        drinks = MenuItems.objects.filter(category__name__icontains='Drink')
        
        #pass into context
        context = {
            'appetizers' : appetizers,
            'entres' : entres,
            'desserts' : desserts,
            'drinks' : drinks,
        }
        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        street = request.POST.get('street')
        zip_code = request.POST.get('zip_code')
        
        order_items = {
            'items' : []
        }
        items = request.POST.getlist('items[]')
        
        for item in items:
            menu_item = MenuItems.objects.get(pk__contains=int(item))
            item_data = {
                'id' : menu_item.pk,
                'name' : menu_item.name,
                'price' : menu_item.price
            }
            
            order_items['items'].append(item_data)
            
            price = 0
            item_ids = []
            
        #for adding up all the prices of items
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            
        #order items to be appended
        order = OrderModel.objects.create(price=price, name=name, email=email, street=street, city=city, state=state, zip_code=zip_code)
        order.items.add(*item_ids)
        
        #after everythin is done send mail
        body = ('Thank you for your order,Hope you enjoy your food visit again\n'
                f'Your total:{price}')
        send_mail(
            'Thank you for the order',
            body,
            'example@gmail.com',
            [email],
            fail_silently=False
        )
            
        context = {
            'items' : order_items['items'],
            'price' : price
        }
        
        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwars):
        order = OrderModel.objects.get(pk=pk)
        
        context = {
            'pk' : order.pk,
            'price' : order.price,
            'items' : order.items   
        }
        return render(request, 'customer/order_confirmation.html', context) 
    
    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)
        
        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.isPaid = True
            order.save()
            
        return redirect('payment-confirmation')
        
class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')