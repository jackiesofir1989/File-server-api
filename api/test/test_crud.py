# -*- coding: utf-8 -*-
from starlette import status
from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_response():
    response = client.get('/api/v1/')
    assert response.status_code, status.HTTP_200_OK
    assert response.json(), {"message": "Hello World"}
