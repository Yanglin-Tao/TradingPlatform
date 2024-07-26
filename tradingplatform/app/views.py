import requests
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import messages

API_KEY = 'GRP09XINF1N1T'
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
        return Response({"error": "Symbol not supported"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = get_stock_price(symbol, API_KEY)
    if data:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to fetch data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def signup(request):
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    if User.objects.filter(email=email):
        messages.error(request, "Email already registered!")
    if len(username)>30:
        messages.error(request, "Username must be under 30 charcters!!")
    if password1 != password2 :
        messages.error(request, "Passwords didn't matched!!")
    user = User(user_name = username, email = email, password = password1)
    user.save()
    
    
# def signin(request):
