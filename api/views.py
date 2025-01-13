from typing import Any, Dict
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash, login, logout, authenticate
from .models import CustomUser, Hobby
import json
from django.db.models import Count, Q
from datetime import date, timedelta, datetime
from django.shortcuts import get_object_or_404
from .models import FriendRequest
from typing import List, TypedDict
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

@ensure_csrf_cookie
def set_csrf_token(request):
    response = JsonResponse({"details": "CSRF cookie set"})
    response['X-CSRFToken'] = get_token(request)  # Explicitly set the token
    return response

# Render the main SPA
def main_spa(request: HttpRequest) -> JsonResponse:
    return render(request, 'api/spa/index.html', {})

# Fetch the current user's profile data
@login_required
@csrf_exempt
def profile_api(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        user: CustomUser = request.user
        data: Dict[str, Any] = {
            "name": user.name,
            "email": user.email,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
            "hobbies": list(user.hobbies.values('id', 'name')),
        }
        return JsonResponse({"success": True, "data": data})
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

# Update the current user's profile data
@login_required
@require_POST
@csrf_exempt
def update_profile_api(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        user: CustomUser = request.user
        updated_fields = []

        if 'name' in data and data['name'] != user.name:
            user.name = data['name']
            updated_fields.append('name')
            
        if 'email' in data and data['email'] != user.email:
            if CustomUser.objects.filter(email=data['email']).exclude(id=user.id).exists():
                return JsonResponse({
                    "success": False, 
                    "message": "Email already in use."
                }, status=400)
            user.email = data['email']
            updated_fields.append('email')
            
        if 'date_of_birth' in data and data['date_of_birth'] != user.date_of_birth:
            try:
                if data['date_of_birth']:
                    parsed_date = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                else:
                    parsed_date = None
                user.date_of_birth = parsed_date
                updated_fields.append('date_of_birth')
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid date format. Please use YYYY-MM-DD'
                }, status=400)

        if 'hobbies' in data:
            new_hobby_ids = set(hobby['id'] for hobby in data['hobbies'])
            current_hobby_ids = set(user.hobbies.values_list('id', flat=True))
            
            if new_hobby_ids != current_hobby_ids:
                hobbies = Hobby.objects.filter(id__in=new_hobby_ids)
                user.hobbies.set(hobbies)
                updated_fields.append('hobbies')

        if updated_fields:
            user.save()
            
            updated_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
                "hobbies": list(user.hobbies.values('id', 'name')),
            }
            return JsonResponse({
                "success": True, 
                "message": f"Updated: {', '.join(updated_fields)}",
                "data": updated_data
            })
        else:
            return JsonResponse({
                "success": True, 
                "message": "No changes detected",
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
                    "hobbies": list(user.hobbies.values('id', 'name')),
                }
            })
            
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "errors": str(e)
        }, status=400)


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

class HobbyDict(TypedDict):
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
            date_of_birth: str = data.get('date_of_birth')
            hobbies: List[HobbyDict] = data.get('hobbies', [])
            hobby_names: List[str] = [hobby.get('name') for hobby in hobbies]
            
            if not all([name, email, password]):
                return JsonResponse({
                    'success': False, 
                    "message": "Name, email, and password are required."
                }, status=400)
            
            if not hobby_names:
                return JsonResponse({
                    'success': False, 
                    "message": "Please enter at least one hobby."
                }, status=400)
            
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False, 
                    "message": "Email already in use."
                }, status=400)
            
            parsed_date = None
            if date_of_birth:
                try:
                    parsed_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid date format. Please use YYYY-MM-DD'
                    }, status=400)
            
            user = CustomUser.objects.create_user(
                email=email,
                name=name,
                password=password,
                date_of_birth=parsed_date
            )

            for hobby_name in hobby_names:
                hobby_name = hobby_name.strip()
                if hobby_name:
                    hobby, _ = Hobby.objects.get_or_create(name=hobby_name)
                    user.hobbies.add(hobby)
            
            login(request, user)

            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
                "hobbies": list(user.hobbies.values('id', 'name')),
            }
            return JsonResponse({
                'success': True, 
                "message": "Successful Sign Up",
                "user": user_data
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
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            if email is None or password is None:
                return JsonResponse({'detail': 'Please provide email and password.'}, status=400)

            print(f"Attempting to authenticate user: {email}")

            user = authenticate(request, username=email, password=password)
            if user is None:
                return JsonResponse({'detail': 'Invalid credentials.'}, status=400)
            print(f"Authenticated User: {user}")

            if user:
                if not user.is_active:
                    return JsonResponse({"success": False, "message": "User account is inactive."}, status=403)

                login(request, user)
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
                    "hobbies": list(user.hobbies.values('id', 'name')),
                }
                return JsonResponse({"success": True, "message": "Successful Login.", "user": user_data})
            
            return JsonResponse({"success": False, "message": "Cannot Authenticate User"}, status=403)
        except Exception as e:
            print(f"Error in login: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid Request."}, status=405)



@csrf_exempt
@login_required
def similar_users(request):
    current_user = request.user
    user_hobbies = set(current_user.hobbies.values_list('id', flat=True))

    users = CustomUser.objects.exclude(id=current_user.id).annotate(
        common_hobbies=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies))
    ).order_by('-common_hobbies')

    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    today = date.today()

    if age_min:
        users = users.filter(date_of_birth__lte=today - timedelta(days=int(age_min)*365))
    if age_max:
        users = users.filter(date_of_birth__gte=today - timedelta(days=int(age_max)*365))

    total_count = users.count()

    page = int(request.GET.get('page', 1))
    per_page = 9
    start = (page - 1) * per_page
    end = start + per_page
    users_paginated = users[start:end]

    friend_ids = set(current_user.friends.values_list('id', flat=True))
    sent_request_ids = set(current_user.sent_requests.filter(
        status='pending'
    ).values_list('to_user_id', flat=True))

    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'common_hobbies': user.common_hobbies,
            'age': (today - user.date_of_birth).days // 365 if user.date_of_birth else None,
            'isFriend': user.id in friend_ids,
            'requestSent': user.id in sent_request_ids,
        }
        for user in users_paginated
    ]

    return JsonResponse({
        'users': users_data,
        'total_count': total_count,
        'page': page,
        'per_page': per_page
    }, safe=False)


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
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)
        
        logout(request)
        return JsonResponse({
            "success": True,
            "message": "Logged out successfully"
        })
    return JsonResponse({
        "success": False,
        "message": "Invalid request method"
    }, status=405)

@require_http_methods(['GET'])
def user(request):
    print(request.user)
    if request.user.is_authenticated:
        return JsonResponse(
            {'email': request.user.email}
        )
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )