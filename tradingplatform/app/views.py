import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

