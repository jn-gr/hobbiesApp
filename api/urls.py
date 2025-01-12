from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_spa),
    # auth
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # csrf
    path('set-csrf-token/', views.set_csrf_token, name='set_csrf_token'),
    path('user/', views.user, name='user'), # temp

    # Profile
    path("profile/", views.profile_api, name="profile_api"),
    path("profile/update/", views.update_profile_api, name="profile_api"),
    
    # idek bro
    path("hobbies/", views.hobbies_api, name="hobbies"),
    path("hobbies/add/", views.add_hobby, name="add_hobby"),

    # friends
    path('friends/', views.list_friends, name='list_friends'),
    path('friend_requests/sent/', views.list_sent_requests, name='list_sent_requests'),
    path('friend_requests/received/', views.list_received_requests, name='list_received_requests'),
    path('friend_requests/send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend_requests/reject/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
