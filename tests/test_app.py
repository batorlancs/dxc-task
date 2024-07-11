import pytest
import requests

def test_app():
    response = requests.get("http://localhost:3000")
    assert response.text == "Hello World!"
    