"""milliodollar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('addimage',views.addImageView,name="addimage"),
    path('addAddress',views.addAddressView,name="addaddress"),
    path('userForm',views.userFormView,name="userForm"),
    path('requests',views.requestView,name='requests'),
    path('faq',views.faqView,name='faq'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)