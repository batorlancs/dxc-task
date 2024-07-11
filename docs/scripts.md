# Scripts

## Run redis locally (docker)

Compose docker

```sh
docker-compose up -d
```

Shut down docker

```sh
docker-compose down
```

## Run the server

### Powershell

```sh
venv/Scripts/Activate.ps1
python app.py
```

### Command Prompt

```sh
venv\Scripts\activate.bat
python app.py
```

## Run tests

```sh
pytest
```