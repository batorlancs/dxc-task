# Pipenv Scripts

You can find the scripts in the `Pipfile` under the `scripts` section.
To run a script, use the following command:

```bash
pipenv run <script_name>
```

## Running Server

```sh
pipenv run app # start the server
pipenv run app --empty # empty the redis database and start the server
pipenv run app --test # empty and create tokens for testing (admin5, admin10, admin100, admin1000)
```

## Redis/Docker Scripts

> **Note**: Docker Engine needs to be running to use these scripts.

```bash
pipenv run redis-up # Start Redis container
pipenv run redis-down # Stop Redis container
pipenv run redis-restart # Restart Redis container
pipenv run redis-info # Check wether Redis container is running
pipenv run redis-logs # Show Redis container logs
```

## Testing

```sh
pipenv run test # Run all tests
pipenv run test -k <keyword> # Run tests with a specific keyword
```

## Formatting

```sh
pipenv run format # Format the code with autopep8
pipenv run format-diff # Show the diff of the code formatting (Does not change the code)
```

## CLI

This script is used to interact with the database from the command line.

```sh
pipenv run cli create <token> # Create a new token with all permissions, 100 access limit
pipenv run cli delete <token> # Delete a token
pipenv run cli use <token> # Use a token (increment access_count)
```
