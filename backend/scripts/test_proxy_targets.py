import requests
urls = [
    'http://127.0.0.1:8000/api/v1/auth/login',
    'http://localhost:8000/api/v1/auth/login',
    'http://localhost:5173/api/v1/auth/login',
]
for url in urls:
    try:
        r = requests.post(url, json={'username':'admin','password':'1234'}, timeout=5)
        print(url, r.status_code, r.text)
    except Exception as e:
        print(url, 'ERROR', e)
