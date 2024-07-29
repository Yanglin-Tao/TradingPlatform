# TradingPlatform
A Django-based Python backend for the online trading platform.

## Development setup
### Install development dependences
```
pipenv install
```
### Run development server
```
python manage.py runserver
```
### Example API
In tradingplatform/app/views.py, an API is defined for getting the stock price (stock_price):

http://127.0.0.1:8000/app/price/ibm/

### Connecting to database
1. Download Postgresql and pgAdmin4.

2. Create a new database named 'tradingdata' and make sure that it's connected.

3. In the top menu, open Tools > Query Tool, then change the password to 'mypassword' using the following query:
```
ALTER USER postgres WITH PASSWORD 'mypassword';
```
Make sure the database user is 'postgres' (default user) as well.

4. Make migrations to the database using the following command:
```
python manage.py migrate
```

5. Right click on database and select Refresh, under Schemas > Tables, the tables should be ready.

## References
[Trading Platform Project Delierables](https://docs.google.com/document/d/1nSemyHsZdxt_cOOt12eZMfBD5qV_iyabLDchFLDIPrU/edit)


[Trading Platform Project Charts](https://app.diagrams.net/#G10uPsdOcl96lwgtEo8y07Zrb-_jO5mh0a#%7B%22pageId%22%3A%22v89XgWUNqkIryxFXCNnX%22%7D)