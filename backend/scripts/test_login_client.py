import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:
    r = client.post('/api/v1/auth/login', json={'username':'admin','password':'admin123'})
    print('status', r.status_code)
    print(r.text)
