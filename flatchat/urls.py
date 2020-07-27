"""flatchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from firstapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('contact/',views.contact,name="contact"),
    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name="signup"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('contact/',views.contact,name="contact"),
    path('property_detail/',views.property_detail,name="property_detail"),
    path('property/',views.properties,name="property"),
    path('check_user',views.check_user,name="check_user"),
    path('user_login/',views.user_login,name="user_login"),
    path('customer_dashboard/',views.customer_dashboard,name="customer_dashboard"),
    path('seller_dashboard/',views.seller_dashboard,name="seller_dashboard"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('category_type/',views.category_type,name="category_type"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('add_property/',views.add_property_view,name="add_property_view"),
    path('my_property/',views.my_property,name="my_property"),
    path('single_property/',views.single_property,name="single_property"),
    path('update_property/',views.update_property,name="update_property"),
    path('delete_property',views.delete_property,name="delete_property"),
    path('all_property/',views.all_property,name="all_property"),
    path('sendemail/',views.sendemail,name="sendemail"),
    path('forgotpass/',views.forgotpass,name="forgotpass"),
    path('resetpass',views.resetpass,name="resetpass"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('books/',views.books,name='books'),
    path('payment-done/<int:pid>', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
