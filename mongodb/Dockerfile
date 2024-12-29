# Use the official MongoDB image
FROM mongo:7.0.16

# Create directories to store initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy initialization scripts to the container
COPY ./init-collections.sh /docker-entrypoint-initdb.d/

# Set permissions for the scripts
RUN chmod +x /docker-entrypoint-initdb.d/init-collections.sh