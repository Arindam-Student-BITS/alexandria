# Disclaimer
**This is a directory to keep the microservices**

# Run/Set-up
```console
docker build -t local/alexandria:1.0.002 . --no-cache
```

# Goal/Objective

We would be spinning up the Books Service and its related dependencies here:

```console
docker-compose up
```

1. You may check the API documentation by hitting http://localhost:9000/docs from your browser
1. It will start two containers 1. Books micro service 2. MongoDB
1. It takes the port number 9000 configured in the Dockerfile.