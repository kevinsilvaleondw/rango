"""tango_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf.urls import url, include
from django.urls import path
from rango import views
from django.conf import settings
from django.views.static import serve
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from django.contrib import admin # UNCOMMENT THIS LINE
admin.autodiscover() # UNCOMMENT THIS LINE, TOO!
urlpatterns = [
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG: 
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),

    ]

   