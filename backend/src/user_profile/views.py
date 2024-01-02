import json
from django.shortcuts import render
from authentification.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


def user_profile(request):
    users = UserProfile.objects.all()
    return render(request, 'user_list.html', {'users': users})


# Create your views here.
@login_required
def get_profile_view(request):
    if request.method == 'GET':
        user = request.user
        user_info = {
            'username': user.username
        }
        return (JsonResponse(user_info))
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@login_required
def get_profile_image(request):
    if request.method == 'GET':
        user = request.user
        image_path = user.profile_image.path

        with default_storage.open(image_path, 'rb') as f:
            image_data = f.read()
            return HttpResponse(image_data, content_type="image/jpeg")
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@login_required
@csrf_exempt
def update_profile(request):
    update_username = 0
    update_password = 0
    update_image = 0

    if request.method != 'POST':
        return (JsonResponse({"error": "Unauthorized method"}, status=405))
    try:
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        new_profile_image = request.FILES.get('fileInput')

        if new_username:
            try:
                UserProfile.objects.get(username=new_username)
                return (JsonResponse({"error": "Username already exist"}, status=400))
        
            except ObjectDoesNotExist:
                update_username = 1

        if new_password:
            hashed_password = make_password(new_password)
            update_password = 1
        
        if new_profile_image:
            update_image = 1
        
        if update_username:
            request.user.username = new_username
        if update_password:
            request.user.password = hashed_password
        if update_image:
            request.user.profile_image = new_profile_image
        request.user.save()
        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        
    except json.JSONDecodeError:
        return (JsonResponse({"error": "Invalid JSON data"}, status=400))

