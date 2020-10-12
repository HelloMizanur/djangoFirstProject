from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *
from .forms import OrderForm
from .filters import OrderFilter


# Create your views here.

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


def products(request):
    context={}
    return render(request,'accounts/products.html', context)


def customers(request, pk_customer):
    customer = Customer.objects.get(id=pk_customer)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context={'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request,'accounts/customers.html', context)


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


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request, 'accounts/delete.html', context)