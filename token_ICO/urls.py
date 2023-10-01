"""
URL configuration for token_ICO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from icoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_token_balance/', views.get_token_balance, name='get_token_balance'),
    path('projects/', views.project_list, name='project_list'),
    path('invest/', views.get_token_balance, name='invest'),
    path('fetch_project/', views.fetch_project_from_contract, name='fetch_project'),


]
