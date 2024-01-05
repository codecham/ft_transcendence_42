import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from authentification.models import UserProfile
from .models import Friend


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
    




#Add a friend
@login_required
@csrf_exempt
def add_friend_view(request, friend_name):
    if request.method == 'GET':

        #Take UserProfile object of the user and the friend in the request
        current_user = request.user
        friend = get_object_or_404(UserProfile, username=friend_name)

        #Return an errror if no one with the friend name is found in DB
        if not friend:
            return JsonResponse({'error': 'Username friend not found.'}, status=404)

        #Return an error if the relation already exist
        if Friend.objects.filter(user=current_user, friend=friend).exists():
            return JsonResponse({'error': 'You are already friends with this user.'}, status=400)

        #Create a new line in DataBase with the current_user and the new_friend
        new_friendship = Friend(user=current_user, friend=friend)
        new_friendship.save()
        return JsonResponse({'success': 'Friend added successfully.'}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)





#Remove a friend
@login_required
@csrf_exempt
def remove_friend_view(request, friend_name):
    if request.method == 'GET':
        current_user = request.user
        friend = get_object_or_404(UserProfile, username=friend_name)

        if not friend:
            return JsonResponse({'error': 'Username friend not found.'}, status=404)

        friendship = Friend.objects.filter(user=current_user, friend=friend).first()

        if not friendship:
            return JsonResponse({'error': 'You are not friends with this user.'}, status=400)

        friendship.delete()

        return JsonResponse({'success': 'Friend removed successfully.'}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)



@login_required
@csrf_exempt
def friends_list_view(request):
    if request.method == 'GET':
        print("In in backend")
        
        current_user = request.user
        friends_data = []

        friends = Friend.objects.filter(user=current_user)

        for friendship in friends:
            friend = friendship.friend
            print("Friend id %s and the online status is :%s", friend.username, friend.online_status)
            friend_info = {
                'username': friend.username,
                'online_status': friend.online_status,
            }
            friends_data.append(friend_info)

        return JsonResponse({'friends': friends_data})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    

@login_required
@csrf_exempt
def non_friends_list_view(request):
    if request.method == 'GET':
        print("In in backend")

        all_users = UserProfile.objects.all()
        non_friends_data = []
        current_user = request.user

        friends = Friend.objects.filter(user=current_user)

        friend_ids = [friend.friend.id for friend in friends]

        for user in all_users:
            if user != current_user and user.id not in friend_ids:
                print("User id %s and the online status is :%s", user.username, user.online_status)
                non_friend_info = {
                    'username': user.username,
                }
                non_friends_data.append(non_friend_info)

        return JsonResponse({'user': non_friends_data})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)