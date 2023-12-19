import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# decorator
@csrf_exempt
def register_view(request):
	if request.method != "POST":
		return (JsonResponse({"error":"Unauthorized method"}, status=405))

	try:
		data=json.loads(request.body.decode('utf-8')) # data will contain the parsed request
		username=data.get('username')
		password=data.get('password')
	except json.JSONDecodeError:
		return (JsonResponse({"error":"Invalid Json format"}, status=400))
		
	if not username or not password:
		return (JsonResponse({"error":"Username or Password Invaled"}, status=400))

	try:
		UserProfile.objects.get(username=username)
		return (JsonResponse({"error":"Username already exist"}, status=400))
	except ObjectDoesNotExist:
		pass

	# Hash the password before storing it
	hashed_password = make_password(password)
	UserProfile.objects.create(username=username, password=hashed_password)
	return (JsonResponse({"success":"Registration success"}))


@csrf_exempt
def	login_view(request):
	if request.method != "POST":
		return (JsonResponse({"error":"Unauthorized method"}, status=405))
	
	try:
		data=json.loads(request.body.decode('utf-8'))
		username=data.get('username')
		password=data.get('password')
	except json.JSONDecodeError:
		return (JsonResponse({"error":"Invalid Json format"}, status=400))

	if not username or not password:
		return (JsonResponse({"error":"Username or Password Invalid"}, status=400))
	
	user = authenticate(request, username=username, password=password)

	if user is not None:
		login(request, user)

		return (JsonResponse({"success": "Login successful"}))
	else:
		return (JsonResponse({"error": "Invalid credentials"}, status=401))

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': 'User logged out successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
	

def user_is_log(request):
	user = request.user
	if user.is_authenticated:
		return (JsonResponse({"sucess": 'User is log', "username" : user.username}))
	return (JsonResponse({"error": 'User is not log'}, status=401))


@csrf_exempt
@login_required
def user_info_view(request):
	if request.method == 'GET':
		user = request.user

		if user.is_authenticated:
			user_info = {
				'id': user.id,
				'username': user.username
			} 
			return (JsonResponse(user_info))
		print("User is not auth...")
		return JsonResponse({'error': 'User not authenticated'}, status=401)
	else:
		return JsonResponse({'error': 'Method not allowed.'}, status=405)
