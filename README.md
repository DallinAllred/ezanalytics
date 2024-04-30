# Setup
## Download and Install Docker
EZAnalytics is designed to be quickly started as a set of Docker containers. To utilize the application, Docker must first be installed on the host system.

For Windows, MacOS, and Linux Desktops, the download can be found at:

    https://www.docker.com/products/docker-desktop/

## Start Containers

### Development Mode
To start the application, run one of the following commands:
```sh
# On the first run this builds the containers and starts them.
# If the containers already exist then they restart in their same state.
docker compose -f docker-compose-dev.yml up 

# Rebuild the containers
docker compose -f docker-compose-dev.yml build

# Rebuild and start the containers
docker compose -f docker-compose-dev.yml up --build

# Run destached (frees up the terminal)
docker compose -f docker-compose-dev.yml up -d

```

### Production Mode
```sh
docker compose up --build -d
```


## Stop the Containers
```sh
# Stop running containers
docker compose -f docker-compose-dev.yml stop

# Stop and delete all Docker containers
docker compose -f docker-compose-dev.yml down

# Stop and delete both containers and volumes
docker compose -f docker-compose-dev.yml down -v
```

## Miscellaneous Docker Info
```sh
# Remove all containers
docker rm -f $(docker ps -a -q)  

# Remove all volumes
docker volume rm $(docker volume ls -q)  
```