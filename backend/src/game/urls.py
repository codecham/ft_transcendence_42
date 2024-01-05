from django.urls import path
from . import views

urlpatterns=[
    path("create_room/", views.create_room_view, name="create_room"),
	path("create_tournement/<int:nb_player>", views.create_tournement_view, name="create_tournement"),
	path("create_local/", views.create_local_game_view, name="create_local"),
	path("get_match_history/", views.get_match_history, name="get_match_history"),
	path("get_other_game_history/<int:user_id>", views.get_other_game_history, name="get_other_game_history"),
]