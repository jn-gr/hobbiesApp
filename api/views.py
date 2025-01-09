from typing import Any, Dict
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout
from .models import CustomUser, Hobby
import json
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from datetime import date
from django.shortcuts import get_object_or_404
from .models import FriendRequest
from typing import List, TypedDict

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

class Hobby(TypedDict):
    id: int
    name: str

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            name: str = data.get('name')
            email: str = data.get('email')
            password: str = data.get('password')
            hobbies: List[Hobby] = [hobby.get('name') for hobby in data.get('hobbies', [])]
            
            if not all([name, email, password]):
                return JsonResponse({
                    'success': False, 
                    "message": "Name, email, and password are required."
                }, status=400)
            
            if not hobbies:
                return JsonResponse({
                    'success': False, 
                    "message": "Please enter at least one hobby."
                }, status=400)
            
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False, 
                    "message": "Email already in use."
                }, status=400)
            
            # Create user
            user = CustomUser.objects.create_user(
                email=email,
                name=name,
                password=password
            )
            
            # Add hobbies
            for hobby_name in hobbies:
                hobby_name = hobby_name.strip()
                if hobby_name:
                    hobby, _ = Hobby.objects.get_or_create(name=hobby_name)
                    user.hobbies.add(hobby)
            
            login(request, user)
            return JsonResponse({
                'success': True, 
                "message": "Successful Sign Up"
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                "message": "Invalid JSON data."
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                "message": str(e)
            }, status=400)
            
    return JsonResponse({
        'success': False, 
        "message": "Invalid Request Method."
    }, status=405)


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
            return JsonResponse({"success": False, "message": "Cannot Authenticate User"}, status=403)
        except Exception as e:
            print("Exception during login:", str(e)) 
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid Request."}, status=405)


@csrf_exempt
@login_required
def similar_users(request):
    current_user = request.user
    user_hobbies = set(current_user.hobbies.values_list('id', flat=True))

    # Calculate similarity scores
    users = CustomUser.objects.exclude(id=current_user.id).annotate(
        common_hobbies=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies))
    ).order_by('-common_hobbies')

    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'common_hobbies': user.hobbies,
            'age': user.date_of_birth,
        }
        for user in page_obj
    ]

    return JsonResponse({'users': users_data, 'has_next': page_obj.has_next()}, safe=False)


@csrf_exempt
@login_required
def similar_users(request):
    current_user = request.user
    user_hobbies = set(current_user.hobbies.values_list('id', flat=True))

    # Calculate similarity scores based on hobbies
    users = CustomUser.objects.exclude(id=current_user.id).annotate(
        common_hobbies=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies))
    ).order_by('-common_hobbies')

    # Age filtering
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    today = date.today()

    # Add age calculation as an annotation
    users = users.annotate(
        age=(today.year - F('date_of_birth__year') - ((today.month, today.day) < (F('date_of_birth__month'), F('date_of_birth__day'))))
    )

    if age_min:
        users = users.filter(age__gte=int(age_min))
    if age_max:
        users = users.filter(age__lte=int(age_max))

    # Pagination
    page = int(request.GET.get('page', 1))
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    users_paginated = users[start:end]
    has_next = users.count() > end

    # Prepare data
    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'common_hobbies': user.common_hobbies,
            'age': user.age,
        }
        for user in users_paginated
    ]

    return JsonResponse({'users': users_data, 'has_next': has_next}, safe=False)


@csrf_exempt
@login_required
def list_friends(request):
    user = request.user
    friends = user.friends.all()
    friends_data = [{'id': friend.id, 'name': friend.name, 'email': friend.email} for friend in friends]
    return JsonResponse({'friends': friends_data}, safe=False)


@csrf_exempt
@login_required
def list_sent_requests(request):
    user = request.user
    sent_requests = user.get_sent_requests()
    sent_requests_data = [
        {'id': fr.id, 'to_user': fr.to_user.name, 'status': fr.status, 'created_at': fr.created_at}
        for fr in sent_requests
    ]
    return JsonResponse({'sent_requests': sent_requests_data}, safe=False)


@csrf_exempt
@login_required
def list_received_requests(request):
    user = request.user
    received_requests = user.get_received_requests()
    received_requests_data = [
        {'id': fr.id, 'from_user': fr.from_user.name, 'status': fr.status, 'created_at': fr.created_at}
        for fr in received_requests
    ]
    return JsonResponse({'received_requests': received_requests_data}, safe=False)


@csrf_exempt
@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists():
        return JsonResponse({'error': 'Friend request already sent!'}, status=400)
    if request.user.is_friend(to_user):
        return JsonResponse({'error': 'You are already friends!'}, status=400)
    
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return JsonResponse({'message': 'Friend request sent successfully!'})


@csrf_exempt
@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, status='pending')
    friend_request.accept()
    return JsonResponse({'message': 'Friend request accepted!'})


@csrf_exempt
@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, status='pending')
    friend_request.reject()
    return JsonResponse({'message': 'Friend request rejected!'})


@csrf_exempt
def user_logout(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        logout(request)
        return JsonResponse({
            "success": True,
            "message": "Logged out successfully"
        })
    return JsonResponse({
        "success": False,
        "message": "Invalid request method"
    }, status=405)