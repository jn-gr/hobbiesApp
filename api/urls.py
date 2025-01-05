from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from .views import signup, user_login, profile_api, hobbies_api, add_hobby, main_spa, list_friends, list_received_requests, list_sent_requests, send_friend_request, accept_friend_request, reject_friend_request

urlpatterns = [
    path('', main_spa),
    path("api/signup/", signup, name="signup"),
    path("api/login/", user_login, name="login"),
    path("api/profile/", profile_api, name="profile_api"),
    path("api/hobbies/", hobbies_api, name="hobbies"),
    path("api/hobbies/add/", add_hobby, name="add_hobby"),
    path('api/friends/', list_friends, name='list_friends'),
    path('api/friend_requests/sent/', list_sent_requests, name='list_sent_requests'),
    path('api/friend_requests/received/', list_received_requests, name='list_received_requests'),
    path('api/friend_requests/send/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('api/friend_requests/accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('api/friend_requests/reject/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
]
