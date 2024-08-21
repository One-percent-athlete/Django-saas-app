
from django.contrib import admin
from django.urls import path
from . import views
from auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    path('login/', auth_views.login_view, name='login_view'),
]
