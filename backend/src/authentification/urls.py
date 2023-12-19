from django.urls import path
from . import views

urlpatterns=[
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
	path("user_info/", views.user_info_view, name="userinfo"),
	path("logout/", views.logout_view, name="logout"),
	path("user_is_log/", views.user_is_log, name="userIsLog"),
]