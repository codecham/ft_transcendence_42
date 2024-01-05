import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from authentification.models import UserProfile


@login_required
@csrf_exempt
def friends_view(request):
    if request.method == 'GET':

        print("In in backend")
        # get all users saved in database
        all_users = UserProfile.objects.all()
        friends_data = []
        current_user = request.user
        for user in all_users:
            if user != current_user:
                print("user id %s and the online status is :%s", user.username, user.online_status)
                friend_info = {
                    'username': user.username,
                    'online_status': user.online_status,
                }
                friends_data.append(friend_info)
        return JsonResponse({'friends': friends_data})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)