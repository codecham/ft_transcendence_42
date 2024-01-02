from django.contrib.auth.models import AbstractUser
from django.db import models

def default_profile_image_path():
    return 'profile_test.jpg'

class UserProfile(AbstractUser):
    id = models.AutoField(primary_key = True)  #unique ID
    online_status = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default=default_profile_image_path)


    def __str__(self):
        return (self.username)
	
    pass