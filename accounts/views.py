from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group


from .forms import OrderForm, CustomerForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from accounts.models import *


# Create your views here.
@unauthenticated_user
def rigistrationPage(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customers')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account has Created For ' + username)
            return redirect('/login/')
    context = {'form':form}
    return render(request,'accounts/registration.html', context)
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username Or Password Is Incorrect')
    context = {}
    return render(request,'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
@admin_only
def index(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers =  customers.count()

    total_orders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    context={'customers':customers, 'orders':orders, 'total_orders':total_orders,
    'pending':pending, 'delivered':delivered}
    return render(request,'accounts/dashboard.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product = Product.objects.all()
    context={'product':product}
    return render(request,'accounts/products.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context={'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request,'accounts/customers.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)

    form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render (request, 'accounts/user_page.html', context)

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request, 'accounts/Customer_form.html', context)

