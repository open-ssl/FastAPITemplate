# FastAPITemplate
Simple web application template with FastAPI

### Start with Docker

```
docker build -t fastapi_app -f deployment/non-compose.Dockerfile .
docker run -d -p 7311:8000 fastapi_app 
```

### Start with Compose

```
docker compose -f docker-compose.yaml up -d    
```
