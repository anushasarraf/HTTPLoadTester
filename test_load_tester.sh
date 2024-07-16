#!/bin/bash

# Stop all running containers that use the load_tester image
echo "Stopping all running containers using the load_tester image..."
docker stop $(docker ps -q --filter ancestor=load_tester)

# Remove all stopped containers that use the load_tester image
echo "Removing all stopped containers using the load_tester image..."
docker rm $(docker ps -a -q --filter ancestor=load_tester)

# Basic run command
echo "Running basic load test..."
docker run load_tester http://example.com --max-qps 20 --duration 60 --workers 5 --method GET

# Increase Duration
echo "Running load test with increased duration..."
docker run load_tester http://example.com --max-qps 20 --duration 120 --workers 5 --method GET

# Increase Number of Workers
echo "Running load test with increased number of workers..."
docker run load_tester http://example.com --max-qps 20 --duration 60 --workers 10 --method GET

# Change HTTP Method to POST
echo "Running load test with POST method..."
docker run load_tester http://example.com --max-qps 20 --duration 60 --workers 5 --method POST

# Run with Environment Variable
echo "Running load test with environment variable..."
docker run -e API_KEY=your_api_key load_tester http://example.com --max-qps 20 --duration 60 --workers 5 --method GET

# Run in Detached Mode
echo "Running load test in detached mode..."
docker run -d load_tester http://example.com --max-qps 20 --duration 60 --workers 5 --method GET

# Assign a Specific Name to the Container
echo "Running load test with a specific container name..."
docker run --name my_load_tester load_tester http://example.com --max-qps 20 --duration 60 --workers 5 --method GET

# View Logs of Named Container
echo "Viewing logs of the named container..."
docker logs my_load_tester

# Access Shell Inside Named Container
echo "Accessing shell inside the named container..."
docker exec -it my_load_tester /bin/sh

# Stop Named Container
echo "Stopping the named container..."
docker stop my_load_tester

# Remove Named Container
echo "Removing the named container..."
docker rm my_load_tester

# Inspect the Last Created Container
echo "Inspecting the last created container..."
docker inspect $(docker ps -l -q)

# List All Containers
echo "Listing all containers..."
docker ps -a

# Force Remove Docker Image
echo "Force removing the Docker image..."
docker rmi -f load_tester
