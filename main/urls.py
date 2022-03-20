from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login' ),
    path('logout/', views.logoutPage, name='logout' ),
    path('register/', views.registerPage, name='register' ),
    path('', views.home, name='home' ),
    path('home/<str:pk>/', views.message, name='message' ),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('updateProfile', views.updateProfile, name='updateProfile'),
    path('add_friends', views.add_friends, name='add_friends'),
    path('update_message/<str:f_pk>/<str:m_pk>', views.update_message, name='update_message'),
    path('deleteFriend/<str:pk>/', views.deleteFriend, name='deleteFriend'),
    path('getMessages/<str:pk>/', views.getMessages, name='getMessages'),


]
