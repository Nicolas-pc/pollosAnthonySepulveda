
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', views.welcome),
    path('admin/login', views.login),
    path('admin/logout', views.logout),
    path('', views.index, name='index'),
]