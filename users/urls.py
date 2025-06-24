from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('lottery/', views.lottery_view, name='lottery'),
    path('exchange_tip/', views.exchange_tip_view, name='exchange_tip'),
    path('points/', views.points_view, name='points'),
]
