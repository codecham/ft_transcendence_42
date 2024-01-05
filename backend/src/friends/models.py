from django.db import models
from authentification.models import UserProfile

# This friend request model will store friend requests info (who send request to whom)
# - from_user: it will have a foreignkey relation with a user(first user) who is sending this request.
# - to_user: it will have a foreignkey relation with another user(second user) to whom the first user is sending the request. 


class Friend_Request(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='to_user', on_delete=models.CASCADE)

class Friend(models.Model):
    user = models.ForeignKey(UserProfile, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(UserProfile, related_name='friend', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} <-> {self.friend.username}"