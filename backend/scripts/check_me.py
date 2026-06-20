import os
import requests

TOKEN = os.environ.get('TOKEN') or ''
URL = os.environ.get('URL') or 'http://127.0.0.1:8000/api/v1/auth/me'

if not TOKEN:
    print('No TOKEN provided. Set TOKEN env var.')
    raise SystemExit(1)

headers = {'Authorization': f'Bearer {TOKEN}'}

resp = requests.get(URL, headers=headers, timeout=10)
print('status_code=', resp.status_code)
print('headers=', resp.headers)
print('body=')
print(resp.text)
