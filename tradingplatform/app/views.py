import requests
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

API_KEY = 'GRP09XINF1N1T'
SALT = "8b4f6b2cc1868d75ef79e5cfb8779c11b6a374bf0fce05b485581bf4e1e25b96c8c2855015de8449"
BASE_URL = 'https://echios.tech'
SYMBOLS = ['ibm', 'msft', 'tsla', 'race']

def get_stock_price(symbol, api_key):
    endpoint = f'/price/{symbol}?apikey={api_key}'
    url = BASE_URL + endpoint
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@api_view(['GET'])
def stock_price(request, symbol):
    if symbol not in SYMBOLS:
        return JsonResponse({"error": "Symbol not supported"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = get_stock_price(symbol, API_KEY)
    if data:
        return JsonResponse(data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Failed to fetch data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        password = make_password(data['password'], salt=SALT)
        if User.objects.filter(email=email):
            return JsonResponse({"error": "Email already registered!"}, status=status.HTTP_400_BAD_REQUEST)
        if len(username)>30:
            return JsonResponse({"error": "Username must be under 30 charcters!!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User(user_name = username, email = email, password = password)
            user.save()
            return JsonResponse({"message": "Successfully Registered!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt  
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = make_password(data['password'], salt=SALT)
        user = User.objects.get(email=email)
        if user is None or user.password != password:
            return JsonResponse({'message': 'Invalid credentials', 'success': False})  
        else:
            refresh = RefreshToken.for_user(user)
            user_data = {
                'email': email,
            }
            return JsonResponse(
                {"message": "You are now logged in!",
                'success': True,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user_data
                 },
                status=status.HTTP_200_OK,
            )
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def getUserProfile(request):
    if request.method == 'GET':  
        data = json.loads(request.body)
        email = data['email']
        user = User.objects.get(email=email) 
        if user is None:
            return JsonResponse({'message': 'Invalid credentials', 'success': False})  
        else:
            user_data = {
                            'username':user.user_name,
                            'email':email
                        }
            return JsonResponse(
                {"message": "Here is the user profile",
                'success': True,
                'user': user_data
                 },
                status=status.HTTP_200_OK,
            )
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt  
def deleteAccount(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        user = User.objects.get(email=email)
        if user is None:
            return JsonResponse({'message': 'Invalid credentials', 'success': False})  
        else:
            user.delete()
            return JsonResponse(
                {"message": "Your account is deleted",
                'success': True
                 },
                status=status.HTTP_200_OK,
            )
    return JsonResponse({'message': 'Invalid request'}, status=400)