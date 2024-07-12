import pytest
import requests

url = "http://localhost:3000"


class TestSimpleApi:
    def test_api1_response(self):
        assert requests.get(url + "/api1").text == "API1"