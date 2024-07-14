from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_page,name='register'),
    path('profile/<str:id>/',views.user_profile,name='profile'),
    path('', views.home,name='home'),
    
    path('room/<str:id>/', views.room,name='room'),
    path('create_room/', views.create_room,name='room_create'),
    path('update_room/<str:id>',views.update_room,name='room_update'),
    path('delete_room/<str:id>',views.delete_room,name='room_delete'),
    path('delete_message/<str:id>/', views.delete_message,name='message_delete'),
    
    path('update_user',views.update_user,name='user_update'),
    
    path('topics/',views.topics_page,name='topics'),
    path('activity/',views.activity_page,name='activity'),
    
]