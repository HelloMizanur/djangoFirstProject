from django.urls import path, include
from accounts import views


app_name='accounts'


urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk_customer>/', views.customers, name='customers'),
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),



]