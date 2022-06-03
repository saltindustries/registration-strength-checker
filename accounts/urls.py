from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginAccountPage, name="login"),
    path('register/', views.registerAccountPage, name="register"),
    path('logout', views.logoutUser, name="logout"),
]