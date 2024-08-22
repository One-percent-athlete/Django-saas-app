
from django.contrib import admin
from django.urls import path, include


from . import views
from auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('protected/', views.pw_protected_view, name='protedted'),
    path('protected/user_only/', views.user_only_view, name='user_only'),

    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
]
