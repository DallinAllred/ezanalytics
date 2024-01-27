-- init.sql

-- Create a table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL
);

-- Insert some sample data

INSERT INTO users (first_name, last_name, email)
VALUES ('john', 'doe', 'john@email.com');

INSERT INTO users (first_name, last_name, email)
VALUES ('jane', 'doe', 'jane@email.com');

INSERT INTO users (first_name, last_name, email)
VALUES ('jack', 'oneill', 'oneill@email.com');
