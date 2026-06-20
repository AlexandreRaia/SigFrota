import requests

r = requests.post('http://127.0.0.1:8000/api/v1/auth/login', json={'username':'admin','password':'admin123'})
print('status:', r.status_code)
print(r.text)
