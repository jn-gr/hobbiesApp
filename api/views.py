from typing import Any, Dict
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser, Hobby
import json

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
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Invalid request method."}, status=405)

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
            return JsonResponse({"success": False, "errors": {"oldPassword": ["Incorrect password"]}}, status=400)
        if data["newPassword"] != data["confirmPassword"]:
            return JsonResponse({"success": False, "errors": {"confirmPassword": ["Passwords do not match"]}}, status=400)
        user.set_password(data["newPassword"])
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({"success": True, "message": "Password updated successfully."})
    except Exception as e:
        return JsonResponse({"success": False, "errors": str(e)}, status=400)

# Fetch all hobbies
@login_required
def hobbies_api(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        hobbies = Hobby.objects.all().values("id", "name")
        return JsonResponse(list(hobbies), safe=False)
    return JsonResponse({"error": "Invalid request method."}, status=405)
