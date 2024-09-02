from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout')
]
