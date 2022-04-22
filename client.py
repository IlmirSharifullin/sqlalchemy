from requests import get, put

print(get('http://localhost:5000/api/users/1').json())

