def is_endpoint_in_scope(endpoint: str, scope: str) -> bool:
    """
    Check if an endpoint is in the scope of a token.
    - "*" access to all endpoints and home
    - "" access to just home (or "/")
    - "api/" access to all endpoints in the api but not api itself
    - "api*" access to all endpoints in the api including api itself
    - "api" access to the specific endpoint

    Args:
        token (str): The token to check.
        endpoint (str): The endpoint to check.

    Returns:
        bool: True if the endpoint is in the scope of the token, False otherwise.
    """
    endpoint = endpoint[1:]  # remove the leading slash

    if scope == "*":
        return True
    if scope == "" or scope == "/":
        return endpoint == ""

    if scope.endswith("*"):
        return endpoint.startswith(scope[:-1])

    if scope.endswith("/"):
        return endpoint.startswith(scope)

    return endpoint == scope


def is_endpoint_in_any_scope(endpoint: str, scopes: list[str]) -> bool:
    """
    Check if an endpoint is in the scope of any token.

    Args:
        endpoint (str): The endpoint to check.
        scopes (list): The list of scopes to check.

    Returns:
        bool: True if the endpoint is in the scope of any token, False otherwise.
    """
    for scope in scopes:
        if is_endpoint_in_scope(endpoint, scope):
            return True

    return False
