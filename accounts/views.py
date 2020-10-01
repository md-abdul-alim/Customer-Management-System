from django.shortcuts import render, redirect
from django.forms import inlineformset_factory  # multiple order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
# Create your views here.


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
            # if user.email == "abdul_alim@zohomail.com":
            #     #print(user.username)
            #     login(request,user)
            #     return redirect('index')
            # else:
            #     login(request,user)
            #     return redirect('register')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'accounts/login.html')
    
    return render(request, 'accounts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def index(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=7)  # multiple order
    customer = Customer.objects.get(id=pk)
    # multiple order #queryset use kora hoise jeno previous order gula show na kore
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer}) #single order er jonno
    context = {
        'formset': formset
    }
    if request.method == 'POST':
        # print("print:",request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {
        'order': order
    }
    return render(request, 'accounts/delete_order.html', context)
