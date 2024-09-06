
from django.contrib import admin
from django.urls import path, include


from . import views
from auth import views as auth_views
from subscriptions import views as sub_views
from checkouts import views as checkout_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('protected/', views.pw_protected_view, name='protedted'),
    path('protected/user_only/', views.user_only_view, name='user_only'),
    path('protected/staff_only/', views.staff_only_view, name='staff_only'),

    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),

    path('pricing/', sub_views.subscription_price_view, name='pricing'),
    path('pricing/<str:interval>/', sub_views.subscription_price_view, name='pricing_interval'),
    path('profiles/', include('profiles.urls')),

    path('checkouts/sub_price/<str:price_id>/', checkout_views.product_price_redirect_view, name='sub_price_checkout'),
    path('checkouts/start/', checkout_views.checkout_redirect_view, name='checkout_start'),
    path('checkouts/finalize/', checkout_views.checkout_finalize_view, name='checkout_finalize'),
]
