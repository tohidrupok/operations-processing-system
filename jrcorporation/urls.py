"""
URL configuration for jrcorporation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views. i would like go that . that why i can not go to the return  
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home, importnt but it's make sence some enargy, we wnna go back from here. 
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home') , like then zero, from today tho another day. 
Including another URLconf
    1. Import the include() function: from django.urls import include, path by path. 
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT) 