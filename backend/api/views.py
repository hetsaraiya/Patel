import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Split full name into first and last name
        first_name, last_name = full_name.split(maxsplit=1) if ' ' in full_name else (full_name, '')
        username = str(phone_number)
        # Create user and store phone number
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.phone_number = phone_number
        user.save()

        response_data = {
            'message': 'User created successfully',
            'phone_number': user.phone_number,
            'user_id': user.id  # Include user ID if needed
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def createUserProfile(request):
    if request.method == 'POST':
        # Retrieve data from the request body
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        current_address = request.POST.get('current_address')
        native_address = request.POST.get('native_address')
        mobile_number = request.POST.get('mobile_number')
        marital_status = request.POST.get('marital_status')
        profile_picture = request.FILES.get('profile_picture')

        # Create a new UserProfile object with the retrieved data
        new_profile = UserProfile.objects.create(
            full_name=full_name,
            age=age,
            gender=gender,
            current_address=current_address,
            native_address=native_address,
            mobile_number=mobile_number,
            marital_status=marital_status,
            profile_picture=profile_picture
        )

        # Return a success message as JSON response
        return JsonResponse({'message': 'User profile created successfully'}, status=201)
    else:
        # If request method is not POST, return method not allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def createFamilyDetails(request):
    if request.method == 'POST':
        # Retrieve data from the request body
        user = request.POST.get('user')
        # users = User.objects.get(first_name=user)
        print(user)
        # user_id = users.pk
        related_to = UserProfile.objects.get(full_name=user)
        relation = request.POST.get('relation')
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        marital_status = models.CharField(default="", max_length=20)
        current_address = request.POST.get('current_address')
        age = request.POST.get('age')
        photo = request.FILES.get('photo')

        # Create a new FamilyDetails object with the retrieved data
        new_family_detail = FamilyDetails.objects.create(
            related_to=related_to,
            relation=relation,
            full_name=full_name,
            mobile_number=mobile_number,
            current_address=current_address,
            age=age,
            photo=photo,
            marital_status=marital_status
        )

        # Return a success message as JSON response
        return JsonResponse({'message': 'Family details created successfully'}, status=201)
    else:
        # If request method is not POST, return method not allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def createPost(request):
    if request.method == 'POST':
        # Retrieve data from the request body
        user_id = request.POST.get('full_name')  # Assuming the frontend sends the user ID associated with the post
        user = UserProfile.objects.get(full_name=user_id)
        type_of_post = request.POST.get('type_of_post')
        message = request.POST.get('message')
        image = request.FILES.get('image')

        # Create a new Post object with the retrieved data
        new_post = Post.objects.create(
            user=user,
            type_of_post=type_of_post,
            message=message,
            image=image
        )

        # Return a success message as JSON response
        return JsonResponse({'message': 'Post created successfully'}, status=201)
    else:
        # If request method is not POST, return method not allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def addComment(request):
    if request.method == 'POST':
        # Get data from request body
        post_id = request.POST.get('post_id')
        user_name = request.POST.get('full_name')
        content = request.POST.get('content')
        
        try:
            # Retrieve the post and user objects
            post = Post.objects.get(id=post_id)
            user = UserProfile.objects.get(full_name=user_name)
            print(post.message)
        except (Post.DoesNotExist, UserProfile.DoesNotExist) as e:
            # If post or user does not exist, return error response
            return JsonResponse({'error': str(e)}, status=404)
        
        # Create the comment
        comment = Comment.objects.create(
            post=post,
            user=user,
            content=content,
            created_at=datetime.now()
        )
        
        # Return success response
        return JsonResponse({'message': 'Comment added successfully'}, status=201)
    else:
        # If request method is not POST, return method not allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def likePost(request):
    if request.method == 'POST':
        # Get data from request body
        post_id = request.POST.get('post_id')
        user_name = request.POST.get('full_name')
        
        try:
            # Retrieve the post and user objects
            post = Post.objects.get(pk=post_id)
            user = UserProfile.objects.get(full_name=user_name)
        except (Post.DoesNotExist, UserProfile.DoesNotExist) as e:
            # If post or user does not exist, return error response
            return JsonResponse({'error': str(e)}, status=404)
        
        # Check if the user has already liked the post
        if Like.objects.filter(post=post, user=user).exists():
            Like.objects.filter(post=post, user=user).delete()
            return JsonResponse({'message': 'Post like removed successfully'}, status=200)
        
        # Create the like
        like = Like.objects.create(
            post=post,
            user=user,
            created_at=datetime.now()
        )
        
        # Return success response
        return JsonResponse({'message': 'Post liked successfully'}, status=201)
    else:
        # If request method is not POST, return method not allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def makeMatrimonialProfile(request):
    if request.method == 'POST':
        # Retrieve data from the request
        full_name = request.POST.get('full_name')
        birth_date = request.POST.get('birth_date')
        age = request.POST.get('age')
        current_address = request.POST.get('current_address')
        native_address = request.POST.get('native_address')
        mobile_number = request.POST.get('mobile_number')
        marital_status = request.POST.get('marital_status')
        profile_picture = request.FILES.get('profile_picture')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        education = request.POST.get('education')
        occupation = request.POST.get('occupation')
        occupation_detail = request.POST.get('occupation_detail')
        hobby = request.POST.getlist('hobby')
        user = UserProfile.objects.get(full_name=full_name)

        # Create MatrimonialProfile object
        matrimonial_profile = MatrimonialProfile.objects.create(
            user=user,
            full_name=full_name,
            birth_date=birth_date,
            age=age,
            current_address=current_address,
            native_address=native_address,
            mobile_number=mobile_number,
            marital_status=marital_status,
            profile_picture=profile_picture,
            height=height,
            weight=weight,
            education=education,
            occupation=occupation,
            occupation_detail=occupation_detail,
            hobby=hobby
        )

        # Return success response
        return JsonResponse({'message': 'Matrimonial profile created successfully'}, status=201)
    else:
        # Return error response for invalid request method
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getCount(request):
    if request.method == "GET":
        # Get the post ID from the request parameters
        post_id = request.GET.get("post")
        post = Post.objects.get(pk=post_id)
        # Get the count of comments for the post
        comments_count = Comment.objects.filter(post=post.pk).count()
        # Get the count of likes for the post
        likes_count = Like.objects.filter(post=post.pk).count()
        # Prepare the response data
        response_data = {
            "comments": comments_count,
            "likes": likes_count,
        }
        # Return the response with the counts
        return JsonResponse({"counts": response_data}, status=200)
    else:
        # If the request method is not GET, return method not allowed error
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        pho = str(phone_number)
        # Authenticate user
        user = authenticate(request, username=pho, password=password)

        if user is not None:
            # User authenticated, log them in
            login(request, user)
            response_data = {
                'message': 'Login successful',
            }
            return JsonResponse(response_data, status=200)
        else:
            # Authentication failed
            return JsonResponse({'error': 'Invalid phone number or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
def signIn(request):
    if request.method == "POST":
        username = request.POST.get("phone_number")
        password = request.POST.get("password")
        pho = str(username)
        user = authenticate(username=pho, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({"msg": " Logged In"}),content_type="application/json",)
        else:
            # messages.error(request, "Bad Credentials!!")
            return HttpResponse(json.dumps({"msg": " None"}),content_type="application/json",)
    
    return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)
