from django.urls import path
from . import views

urlpatterns=[
    path("friends_view/", views.friends_view, name="friends_view"),
	path("add_friend_view/<str:friend_name>", views.add_friend_view, name="add_friend_view"),
	path("remove_friend_view/<str:friend_name>", views.remove_friend_view, name="remove_friend_view"),
	path("friends_list_view/", views.friends_list_view, name="friends_list_view"),
	path("non_friends_list_view/", views.non_friends_list_view, name="non_friends_list_view"),
]