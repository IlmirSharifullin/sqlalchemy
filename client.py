from requests import get

print(get('http://localhost:5000/api/jobs').json())
# Выводит все работы

print(get('http://localhost:5000/api/jobs/2').json())
# Выводит работу с id = 2

print(get('http://localhost:5000/api/jobs/15').json())
# {'response': 404, 'text': 'NOT FOUND'}

print(get('http://localhost:5000/api/jobs/qwe').json())
# {'response': 404, 'text': 'Wrong type of id, int expected'}
