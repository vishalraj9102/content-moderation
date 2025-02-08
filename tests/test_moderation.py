from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_moderation():
    response = client.post("/api/v1/moderate/text", json={"text": "Hello world"})
    assert response.status_code == 200
    assert response.json()["is_safe"] == True
