# Use the official PostgreSQL image
FROM postgres:latest

# Set environment variables
# ENV POSTGRES_DB=ezanalytics \
#     POSTGRES_USER=ezanalytics \
#     POSTGRES_PASSWORD=mypassword

# Copy the SQL script to initialize the database
COPY init.sql /docker-entrypoint-initdb.d/