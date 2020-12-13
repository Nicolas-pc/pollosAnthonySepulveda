
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', views.welcome),
    path('admin/login', views.login),
    path('admin/logout', views.logout),
    path('', views.index, name='index'),
    
    url(r'^admin/updateRequest/$', views.updateRequest, name='updateRequest'),
    url(r'^admin/changeState/$', views.changeState, name='changeState'), 
    
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
