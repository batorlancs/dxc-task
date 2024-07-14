import sys
import random
import grequests


BASE_URL = "http://localhost:3000"
ALL_URLS = [f"{BASE_URL}/api1", f"{BASE_URL}/api2", f"{BASE_URL}/api3"]


def get_var_from_args() -> tuple[int, str]:
    args = sys.argv[1:]
    if len(args) != 2:
        print("Args usage: ... <API_CALLS: int> <TOKEN: str>")
        sys.exit(1)
    try:
        api_calls = int(args[0])
        token = args[1]
    except ValueError:
        print("API_CALLS must be an integer")
        sys.exit(1)

    return api_calls, token


def on_exception(request, exception):
    print(f"\033[91mRequest failed for URL {request.url}\033[0m")
    print(exception)
    sys.exit(1)


def run_server_async():
    api_calls, token = get_var_from_args()
    print(f"Running {api_calls} API calls with token {token}...\n")
    urls = random.choices(ALL_URLS, k=api_calls)
    reqs = [grequests.get(url, headers={"token": token}) for url in urls]
    responses = grequests.map(reqs, exception_handler=on_exception)
    for resp in responses:
        if resp is not None:
            print(f"Status code: {resp.status_code}, response: {resp.text}")
        else:
            print("\033[91mNo Response\033[0m")
    print("\033[92mFinished\033[0m")


if __name__ == "__main__":
    run_server_async()
