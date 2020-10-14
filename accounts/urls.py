from django.urls import path, include
from accounts import views


app_name='accounts'


urlpatterns = [
    path('', views.index, name='index'),

    path('registration/', views.rigistrationPage, name='rigistrationPage'),
    path('login/', views.loginPage, name='loginPage'),

    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customers, name='customers'),
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('create_customer/', views.createCustomer, name='createCustomer'),


]

