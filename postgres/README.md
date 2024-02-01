# PSQL
Connect to the Docker container via Docker Desktop or the terminal

### Terminal
```sh
docker exec -it postgres_eza_container bash
```

## Start the CLI
```sh
psql -U postgres

# List Databases
\l

# Select the desired database
\c ezanalytics

# List tables
\dt

# Execute query
SELECT * FROM users;
```