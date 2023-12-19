# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_profile/', views.get_profile_view, name='get_profile'),
    path('get_profile_image/', views.get_profile_image, name='get_profile_image'),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),

]