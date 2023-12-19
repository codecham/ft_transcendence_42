from django.urls import path
from . import views

urlpatterns=[
    path("create_room/", views.create_room_view, name="create_room"),
	path("create_tournement/<int:nb_player>", views.create_tournement_view, name="create_tournement"),
]