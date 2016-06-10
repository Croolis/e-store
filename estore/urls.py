from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add-to-cart/$', views.add, name='add'),
    url(r'^remove-from-cart/$', views.remove, name='remove'),

    url(r'^accounts/logout/$', views.account_logout, name='logout'),
	url(r'^accounts/login/$', views.index, name='login'),
	url(r'^accounts/profile/$', views.account_profile, name='profile'),


    url(r'^payment/cart/$', views.paypal_pay, name='pay_cart'),
	url(r'^payment/success/$', views.paypal_success, name='success'),
]