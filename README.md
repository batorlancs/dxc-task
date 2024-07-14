# dxc-task

High-Level API Backend Server with Socketify

## Overview

This project involves creating a Python-based high-level API backend server using Socketify. The server provides low-level APIs to users, monitors usage (considering API keys), and denies service when limits are reached. Users authenticate themselves with pre-generated authorization strings, allowing access to specific APIs with predefined quotas.

## APIs

The project includes the following simulated API endpoints that return strings:

- **GET** /api1
- **GET** /api2
- **GET** /api3

## Server

The server is built with the following considerations:

- Utilizes the Socketify Python server with an object-oriented approach.
- Employs a local database (redis) for authorization information (tracks which user accesses which API, limits, etc.).

## Testing

The following tests are implemented to ensure functionality:

1. **Simple Test**: Verifies that the correct response is received from each API endpoint.
2. **API Key Test**: Checks if an invalid API key or an API key with no access to an API is denied access.
3. **Limit Test**: Ensures that the server responds with an error when usage limits are exceeded.

## Getting Started

### Prerequisites

- Docker Engine - [Installation](https://docs.docker.com/engine/install/)
- Pipenv - [Installation](https://pipenv.pypa.io/en/latest/installation.html)

### Running the Server

1. **Clone the repository**

2. **Install the dependencies**

    ```sh
    pipenv install
    ```

3. **Start Docker engine**

4. **Start Redis server**

    ```sh
    pipenv run redis-up
    ```

5. **Start the server** (optionally with the `--empty` or `--test` flag)

    ```sh
    pipenv run app
    pipenv run app --empty # empty the redis database and start the server
    pipenv run app --test # empty and create tokens for testing (admin5, admin10, admin100, admin1000)
    ```

### Running Tests

Run the tests with:

> **Note**: For the tests to run, the server **must** be running. (except for some tests)

```sh
pypenv run test
```

Run the tests that have a specific keyword in their name:

```sh
pipenv run test -k <keyword>
```

## References

- [Socketify.py - Bringing Http/Https and WebSockets High Performance servers for PyPy3 and Python3](https://docs.socketify.dev/)
- [Redis Installation Documentation](https://redis.io/docs/getting-started/installation/)
