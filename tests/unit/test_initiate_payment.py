from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_pay_productinfo():

    response = client.post("https://lankly-multipointed-kirstie.ngrok-free.dev/api/payy")

    # API should respond
    assert response.status_code == 200

    html = response.text

    # Check productinfo in HTML
    assert 'name="productinfo" value="Test Product"' in html
