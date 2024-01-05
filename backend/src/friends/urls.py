from django.urls import path
from . import views

urlpatterns=[
    path("friends_view/", views.friends_view, name="friends_view"),
]