from django.urls import path
from . import views

urlpatterns=[
    path("create_room/", views.create_room_view, name="create_room"),
	path("create_tournement/<int:nb_player>", views.create_tournement_view, name="create_tournement"),
	path("create_local/", views.create_local_game_view, name="create_local")
]