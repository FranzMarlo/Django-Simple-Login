from django.urls import path
from . import views, api_views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/', api_views.LoginAPIView.as_view(), name='api-login'),
]
