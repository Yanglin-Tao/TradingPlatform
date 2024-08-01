import requests
import json
import pytz
import schedule
import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Order, Price
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from asgiref.sync import sync_to_async

API_KEY = 'GRP09XINF1N1T'
SALT = "8b4f6b2cc1868d75ef79e5cfb8779c11b6a374bf0fce05b485581bf4e1e25b96c8c2855015de8449"
BASE_URL = 'https://echios.tech'
SYMBOLS = ['ibm', 'msft', 'tsla', 'race']
TIMEZONE = pytz.timezone('America/New_York')

def get_stock_price_and_timestamp(symbol, api_key=API_KEY):
    endpoint = f'/price/{symbol}?apikey={api_key}'
    url = BASE_URL + endpoint
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@api_view(['GET'])
def stock_price(symbol):
    if symbol not in SYMBOLS:
        return JsonResponse({"message": "Symbol not supported"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = get_stock_price_and_timestamp(symbol)
    if data:
        return JsonResponse(data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "Failed to fetch data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        password = make_password(data['password'], salt=SALT)
        if User.objects.filter(email=email):
            return JsonResponse({"message": "Email already registered!"}, status=status.HTTP_400_BAD_REQUEST)
        if len(username) > 30:
            return JsonResponse({"message": "Username must be under 30 charcters!!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User(user_name=username, email=email, password=password)
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
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'message': 'Invalid credentials', 'success': False})  
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
def get_user_profile(request):
    if request.method == 'POST':  
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
def delete_account(request):
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

@csrf_exempt  
def buy(request): 
    """
    Input request is the request after user clicking on "buy" button for a certain type of stock
    The request should contain the following fields:
        - email: the email of the user
        - stock_symbol: the stock symbol (order of operation) to buy
        - quantity: the quantity of stock to buy
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        quantity = data['quantity']
        stock_symbol = data['stock_symbol']

        user = User.objects.get(email=email)
        if user is None:
            return JsonResponse({'message': 'Invalid credentials', 'success': False})  
        else:
            stock_data = get_stock_price_and_timestamp(stock_symbol, API_KEY)
            if stock_data:
                try:
                    time = datetime.fromtimestamp(stock_data['time'], TIMEZONE)
                    # create and save the stock price
                    price = Price(price=stock_data['price'], symbol=stock_data['symbol'], time=time)
                    price.save()
                    # create and save the order
                    assert(stock_data['symbol'].upper() == stock_symbol.upper())
                    order = Order(user=user, price=price, order_type='Limit', order_operation='buy', quantity=quantity, order_time=time, stop_price=0, limit_price=0)
                    order.save()
                    return JsonResponse({"message": "Buying Successfully!"}, status=status.HTTP_200_OK)
                except Exception as e:
                    return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
            else:
                return JsonResponse({'message': 'Failed to fetch stock data', 'success': False})
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt  
def sell(request): 
    """
    Input request is the request after user clicking on "sell" button for a certain type of stock
    The request should contain the following fields:
        - email: the email of the user
        - stock_symbol: the stock symbol (order of operation) to sell
        - quantity: the quantity of stock to sell
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        quantity = data['quantity']
        stock_symbol = data['stock_symbol']

        user = User.objects.get(email=email)
        if user is None:
            return JsonResponse({'message': 'Invalid credentials', 'success': False})  
        else:
            stock_data = get_stock_price_and_timestamp(stock_symbol, API_KEY)
            if stock_data:
                try:
                    time = datetime.fromtimestamp(stock_data['time'], TIMEZONE)
                    # create and save the stock price
                    price = Price(price=stock_data['price'], symbol=stock_data['symbol'], time=time)
                    price.save()
                    # create and save the order
                    assert(stock_data['symbol'].upper() == stock_symbol.upper())
                    order = Order(user=user, price=price, order_type='Limit', order_operation='sell', quantity=quantity, order_time=time, stop_price=0, limit_price=0)
                    order.save()
                    return JsonResponse({"message": "Selling Successfully!"}, status=status.HTTP_200_OK)
                except Exception as e:
                    return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
            else:
                return JsonResponse({'message': 'Failed to fetch stock data', 'success': False})
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt  
def get_order_history(request): 
    """
    Input request is the request after navigating to history page for a certain user
    The request should contain the following fields:
        - email: the email of the user
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        orders = Order.objects.filter(user_id=email)
        if orders is None:
            return JsonResponse({'message': 'No Available Orders', 'success': False})  
        else:
            order_data = []
            for order in orders:
                order_data.append({
                    'symbol': order.price.symbol,
                    'order_operation': order.order_operation,
                    'order_type': order.order_type,
                    'stock_price': order.price.price,
                    'quantity': order.quantity,
                    'time': order.price.time.astimezone(TIMEZONE),
                    'total_price': order.price.price * order.quantity
                })
            return JsonResponse(
                {"message": "Here is the order history for user",
                'success': True,
                'orders': order_data
                 },
                status=status.HTTP_200_OK,
            )
        
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt  
def get_price_history(request): 
    """
    Input request is the request after navigating to price history page 
    The request should contain the following fields:
        - email: the email of the user
    """
    if request.method == 'POST':
        price_data = []
        for stock_symbol in SYMBOLS:
            prices = Price.objects.filter(symbol=stock_symbol.upper()).order_by('-time')[:10]
            if prices is not None:
                price_data_stock = {'labels':[], 'datasets':{}}
                for price in prices[::-1]:
                    price_data_stock['labels'].append(price.time.astimezone(TIMEZONE))
                    price_data_stock['datasets']['label'] = price.symbol
                    price_data_stock['datasets']['data'] = price_data_stock['datasets'].get('data', [])+[price.price]
                    price_data_stock['datasets']['highest_price'] = max(price_data_stock['datasets']['data'])
                    price_data_stock['datasets']['lowest_price'] = min(price_data_stock['datasets']['data'])
            price_data.append(price_data_stock)
        return JsonResponse(
            {"message": "Here is the price history for all stocks",
            'success': True,
            'prices': price_data
            },
            status=status.HTTP_200_OK,
        )
        
    return JsonResponse({'message': 'Invalid request'}, status=400)

def get_stock_price(symbol, api_key=API_KEY): 
    endpoint = f'/price/{symbol}?apikey={api_key}'
    url = BASE_URL + endpoint
    response = requests.get(url)
    if response.status_code == 200:
        stock_data = response.json()
        price = Price(price=stock_data['price'], symbol=stock_data['symbol'], time=datetime.fromtimestamp(stock_data['time'], TIMEZONE))
        price.save()
    else: 
        pass
        # print("Failed to fetch stock data for {}".format(symbol))

# while 1: 
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         future_to_stock = {executor.submit(get_stock_price(symbol), symbol): symbol for symbol in SYMBOLS}
#         for future in future_to_stock:
#             symbol = future_to_stock[future]
#             try:
#                 future.result()
#             except Exception as exc:
#                 pass
#                 # print(f'{symbol} generated an exception: {exc}')
#         print("-"*20)
#         time.sleep(10)