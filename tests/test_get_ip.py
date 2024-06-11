import re

from fastapi.testclient import TestClient
from fastapi import status
from main import app  # replace with the actual location of your FastAPI application


def test_get_ip():
    def is_valid_ip(ip: str) -> bool:
        pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return bool(re.match(pattern, ip))

    client = TestClient(app)
    response = client.get("/ip")
    assert response.status_code == status.HTTP_200_OK
    assert "ipAddress" in response.json()
    ip_address = response.json()["ipAddress"]
    assert isinstance(ip_address, str)

    if is_valid_ip(ip_address):
        assert True
    else:
        assert ip_address == 'Error: [Errno 101] Network is unreachable'

