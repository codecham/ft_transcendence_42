# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_profile/', views.get_profile_view, name='get_profile'),
    path('get_profile_image/', views.get_profile_image, name='get_profile_image'),
    path('update_profile/', views.update_profile, name='update_profile'),
	path('get_other_user_profile/<str:username>', views.get_other_user_profile, name='get_other_user_profile'),
	path('get_other_profile_image/<str:username>', views.get_other_profile_image, name='get_other_profile_image'),
]