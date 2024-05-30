# Setup
## Table of Contents
1. [Docker](#docker)
2. [Basic Usage](#basic-usage)

## Docker
### Download and Install Docker
EZAnalytics is designed to be quickly started via Docker Compose. To utilize the application, Docker must first be installed on the host system.

For Windows, MacOS, and Linux Desktops, the download can be found at:

    https://www.docker.com/products/docker-desktop/

### Start Containers

#### Development Mode
To start the application, run one of the following commands:
```sh
# On the first run this builds the containers and starts them.
# If the containers already exist then they restart in their same state.
docker compose -f docker-compose-dev.yml up 

# Rebuild the containers
docker compose -f docker-compose-dev.yml build

# Rebuild and start the containers
docker compose -f docker-compose-dev.yml up --build

# Run detached (frees up the terminal)
docker compose -f docker-compose-dev.yml up -d

```

#### Production Mode
```sh
docker compose up --build -d
```


### Stop the Containers
```sh
# Stop running containers
docker compose -f docker-compose-dev.yml stop

# Stop and delete all Docker containers
docker compose -f docker-compose-dev.yml down

# Stop and delete both containers and volumes
docker compose -f docker-compose-dev.yml down -v
```

### Miscellaneous Docker Info
```sh
# Remove all containers
docker rm -f $(docker ps -a -q)  

# Remove all volumes
docker volume rm $(docker volume ls -q)  
```

## Basic Usage
### Login
By default, a single user is created:
- Username: **admin**
- Password: **password**

Additional users can be created via the User Admin page. Passwords can be changed via an administrator from that page, and users can update their own passwords from the User Settings window.

## Pages

### Home
The home page lists all charts and dashboards created by the logged in user.

---
### Chart Viewer
Existing charts can be selected from the dropdown at top center for viewing.

Access Permission: *Viewer*

---
### Chart Builder
To create a chart:
1. Select a Data Source from the top left (next to 'Upload CSV button').
2. Change the chart type if desired.
3. Select the appropriate columns from the data set for the X and Y axes.
4. The 'Group By' dropdown at the top right can be used for grouping data (i.e. by part type, etc.)

Access Permission: *Chart Builder*

---
### Dashboards

Existing dashboards can be selected from the dropdown at top center for viewing.

Access Permission: *Viewer*

---
### Dash Builder
To create a dashboard:
1. Select **+Add Chart** button.
2. From the dropdown, select a chart to display.
3. Add additional charts/rows as desired.

*Note: The dashboard layout is restricted to 3 columns.*

Access Permission: *Dash Builder*

---
### Data Sources
The Data Sources page lists all uploaded data on the left side and all external database connections on the right.

Delimited data (e.g. .csv or .tsv files) can be uploaded via the **+Upload Data** button (also available on the Chart Builder page).

Connections to external databases (outside EZAnalytics) can be created via the **+New DB Connection** button. The connection will also store the query to be executed.

<span style="color: orange">**Warning:** The user supplied for the database connection should not have permission to modify any aspects of the database. Only rudimentary checks are in place to prevent data manipulation.</span>

Access Permissions: *Data Connections*

### User Admin
The User Admin page enables adding, removing, and managing users and their permissions.

Access Permissions: *Administrator*