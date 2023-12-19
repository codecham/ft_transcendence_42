from django.shortcuts import render
from authentification.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse

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
        #with open(image_path, 'rb') as f:
        #    return HttpResponse(f.read(), content_type='image/jpeg')
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@login_required
@csrf_exempt
def update_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']
    
        # Update the user's profile image
        request.user.profile_image = profile_image
        request.user.save()

        return JsonResponse({'message': 'Profile image updated successfully.'})    
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)