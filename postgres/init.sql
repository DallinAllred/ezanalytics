-- init.sql

CREATE DATABASE ezanalytics;
\c ezanalytics

-- Create a table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    active BOOLEAN DEFAULT true,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(20) NOT NULL UNIQUE,
    user_email VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    admin BOOLEAN DEFAULT false,
    viewer BOOLEAN DEFAULT false,
    chart_builder BOOLEAN DEFAULT false,
    dash_builder BOOLEAN DEFAULT false,
    connections BOOLEAN DEFAULT false
);

-- Insert some sample data

INSERT INTO users (first_name, middle_name, last_name, username, user_email, password) VALUES ('John', 'Adams', 'Doe', 'johndoe', 'john@email.com', 'password');
INSERT INTO users (first_name, last_name, username, user_email, password) VALUES ('Jane', 'Doe', 'jadoe', 'jane@email.com', 'password');
INSERT INTO users (first_name, last_name, username, user_email, password) VALUES ('Jack', 'Oneill', 'joneill', 'oneill@email.com', 'password');

-- CREATE DATABASE user_data;
-- \c user_data

-- CREATE TABLE owners (
--     user_id,
--     data_table,
--     PRIMARY KEY (user_id, data_table)
-- )
