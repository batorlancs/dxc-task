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
- Employs a local database for authorization information (tracks which user accesses which API, limits, etc.).

## Testing

The following tests are implemented to ensure functionality:

1. **Simple Test**: Verifies that the correct response is received from each API endpoint.
2. **API Key Test**: Checks if an invalid API key is correctly denied access to the API.
3. **Limit Test**: Ensures that the server responds with an error when usage limits are exceeded.

## Getting Started

### Prerequisites

- Python 3.x
- Redis

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/batorlancs/dxc-task.git
    cd dxc-task
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate
    # On Windows CMD use `venv\Scripts\activate.bat`
    # On Windows PWSH use `venv\Scripts\Activate.ps1`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Ensure Redis is installed and running. Refer to [Redis installation documentation](https://redis.io/docs/getting-started/installation/) for more details.

### Running the Server

Start the server using:

```sh
python server.py
```

### Running Tests

Run the tests with:

```sh
pytest
```

## References

- [Socketify.py - Bringing Http/Https and WebSockets High Performance servers for PyPy3 and Python3](https://docs.socketify.dev/)
- [Redis Installation Documentation](https://redis.io/docs/getting-started/installation/)
