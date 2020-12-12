
from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', views.welcome),
    path('admin/login', views.login),
    path('admin/logout', views.logout),
    path('', views.index, name='index'),
    url(r'^admin/updateRequest/$', views.updateRequest, name='updateRequest'),  
]