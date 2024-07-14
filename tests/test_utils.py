import pytest
from utils import is_endpoint_in_scope


class TestUtils:
    @pytest.mark.parametrize("endpoint, scope, expected", [
        # "*" access to all endpoints
        ("/", "*", True),
        ("/api", "*", True),
        ("/api/resource", "*", True),
        ("/api/resource/detail", "*", True),
        
        # "" access to just home
        ("/", "", True),
        ("/api", "", False),
        ("/api/resource", "", False),
        
        # "api/" access to all endpoints in the api but not api itself (or "/api/")
        ("/api", "api/", False),       
        ("/api/resource", "api/", True),
        ("/before/api/resource", "api/", False),
        
        # "api*" access to all endpoints in the api including api itself (or "/api*")
        ("/api", "api*", True),
        ("/api/resource", "api*", True),
        ("/before/api/resource", "api*", False),
        
        # "api" access to the specific endpoint (or "/api")
        ("/api", "api", True),
        ("/api/resource", "api", False),
        ("/anotherapi", "api", False),
        ("/anotherapi/resource", "api", False),
        
        # Home access
        ("/", "api*", False),
        ("/", "api/", False),
        ("/", "api", False),
        ("/", "api/resource", False)
    ])
    def test_is_endpoint_in_scope(self, endpoint, scope, expected):
        assert is_endpoint_in_scope(endpoint, scope) == expected