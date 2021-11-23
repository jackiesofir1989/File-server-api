# -*- coding: utf-8 -*-
from starlette import status
from starlette.testclient import TestClient
from main import app

client = TestClient(app, base_url='http://127.0.0.1:8000')


def test_get_file():
    response = client.get('/files/file.txt')
    assert response.status_code == 200


def test_get_file_list():
    response = client.get('/folder//')
    print(response.text)
    print(response.request)
    assert response.status_code == 200

