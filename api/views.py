from typing import Any, Dict
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash, login, authenticate
from .models import CustomUser, Hobby
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

# Render the main SPA
def main_spa(request: HttpRequest) -> JsonResponse:
    return render(request, 'api/spa/index.html', {})

# Fetch the current user's profile data
@login_required
def profile_api(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        user: CustomUser = request.user
        data: Dict[str, Any] = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
            "hobbies": list(user.hobbies.values('id', 'name')),
        }
        return JsonResponse({"success": True, "data": data})
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

# Update the user's profile
@login_required
@require_POST
@csrf_exempt
def update_profile_api(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        user: CustomUser = request.user
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        user.date_of_birth = data.get("date_of_birth", user.date_of_birth)

        # Update hobbies
        hobbies_ids = data.get("hobbies", [])
        hobbies = Hobby.objects.filter(id__in=hobbies_ids)
        user.hobbies.set(hobbies)

        user.save()
        updated_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
            "hobbies": list(user.hobbies.values('id', 'name')),
        }
        return JsonResponse({"success": True, "message": "Profile updated successfully.", "data": updated_data})
    except Exception as e:
        return JsonResponse({"success": False, "errors": str(e)}, status=400)

# Update the user's password
@login_required
@require_POST
@csrf_exempt
def update_password_api(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        user: CustomUser = request.user
        if not user.check_password(data["oldPassword"]):
            return JsonResponse({'success': False, "errors": {"oldPassword": ["Incorrect password"]}}, status=400)
        if data["newPassword"] != data["confirmPassword"]:
            return JsonResponse({'success': False, "errors": {"confirmPassword": ["Passwords do not match"]}}, status=400)
        user.set_password(data["newPassword"])
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({'success': True, "message": "Password updated successfully."})
    except Exception as e:
        return JsonResponse({'success': False, "errors": str(e)}, status=400)

# Fetch all hobbies
@csrf_exempt
def hobbies_api(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        hobbies = Hobby.objects.all().values("id", "name")
        return JsonResponse(list(hobbies), safe=False)
    elif request.method == "POST":
        try:
            data=json.loads(request.body)
            hobby_name = data.get("name", "").strip()
            if not hobby_name:
                return JsonResponse({"error": "Hobby name required"}, status=400)
            
            hobby, created = Hobby.objects.get_or_create(name=hobby_name)
            return JsonResponse({"id": hobby.id, "name": hobby.name, "created": created})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
@login_required
def add_hobby(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            hobby_name = data.get("name", "").strip()

            if not hobby_name:
                return JsonResponse({"success": False, "message": "Hobby name is required."}, status=400)

            hobby, created = Hobby.objects.get_or_create(name=hobby_name)
            print(f"Hobby {'created' if created else 'exists'}: {hobby.name}")
            return JsonResponse({"id": hobby.id, "name": hobby.name}, status=201 if created else 200)
        except Exception as e:
            print(f"Error in add_hobby: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid Request."}, status=405)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"Signup Data Received: {data}")
            
             
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            hobbies = data.get('hobbies', [])
            
            print(f"Signup Attempt - Name: {name}, Email: {email}, Password: {password}, Hobbies: {hobbies}")
            
            
            if not hobbies:
                return JsonResponse({'success': False, "message": "Please enter at least one hobby."}, status = 400 )
            
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'success': False, "message": "Email already in use."}, status=400)
            

            user = CustomUser.objects.create_user(email=email, name=name, password=password)
            user.save()
            
            for hobby_name in hobbies:
                hobby_name = hobby_name.strip()  # Clean up whitespace
                if hobby_name:  # Ignore empty strings
                    hobby, created = Hobby.objects.get_or_create(name=hobby_name)
                    user.hobbies.add(hobby)
                    print(f"Hobby Added: {hobby}")
            
            
            
            
            print(f"User Created: {user}")
            
            login(request, user)
            return JsonResponse({'success': True, "message": "Successful Sign Up"})
        except Exception as e:
            print("Exception during signup:", str(e))
            return JsonResponse({'success': False, "message": str(e)}, status=400)
    return JsonResponse({'success': False, "message": "Invalid Request."}, status=405)



@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            print("Request body:", request.body)
            
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            print(f"Login Attempt - Email: {email}, Password: {password}")

            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                print(f"Login Successful for: {user}")
                return JsonResponse({"success": True, "message": "Successful Login."})
            print("Authentication Failed")
            return JsonResponse({"success": False, "message": "Cannot Authenticate User"}, status=400)
        except Exception as e:
            print("Exception during login:", str(e)) 
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid Request."}, status=405)


        
            
        
            
