-- init.sql

CREATE DATABASE ezanalytics;
\c ezanalytics

-- Create a table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(20) NOT NULL,
    user_email VARCHAR(50) NOT NULL
);

-- Insert some sample data

INSERT INTO users (first_name, middle_name, last_name, username, user_email) VALUES ('John', 'Adams', 'Doe', 'johndoe', 'john@email.com');
INSERT INTO users (first_name, last_name, username, user_email) VALUES ('Jane', 'Doe', 'jadoe', 'jane@email.com');
INSERT INTO users (first_name, last_name, username, user_email) VALUES ('Jack', 'Oneill', 'joneill', 'oneill@email.com');

-- CREATE DATABASE user_data;
-- \c user_data

-- CREATE TABLE owners (
--     user_id,
--     data_table,
--     PRIMARY KEY (user_id, data_table)
-- )
