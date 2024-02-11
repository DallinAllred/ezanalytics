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
-- DUMMY DATA
INSERT INTO users (first_name, middle_name, last_name, username, user_email, password) VALUES ('John', 'Adams', 'Doe', 'johndoe', 'john@email.com', 'password');
INSERT INTO users (first_name, last_name, username, user_email, password) VALUES ('Jane', 'Doe', 'jadoe', 'jane@email.com', 'password');
INSERT INTO users (first_name, last_name, username, user_email, password) VALUES ('Jack', 'Oneill', 'joneill', 'oneill@email.com', 'password');
-- END DUMMY DATA

CREATE TYPE source_type_enum AS ENUM('external', 'upload');

CREATE TABLE data_sources (
    source_id SERIAL PRIMARY KEY,
    source_type source_type_enum,
    source_label VARCHAR(100) NOT NULL,
    source_access_id VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE connections (
    connection_id SERIAL PRIMARY KEY,
    connection_access_id VARCHAR(100) REFERENCES data_sources(source_access_id) ON DELETE CASCADE,
    connection_host VARCHAR(100) NOT NULL,
    connection_port INT NOT NULL,
    connection_user VARCHAR(100) NOT NULL,
    connection_pw VARCHAR(100) NOT NULL
);

-- DUMMY DATA
INSERT INTO data_sources(source_type, source_label, source_access_id) VALUES ('upload', 'Mill Data', 'mill_data');
INSERT INTO data_sources(source_type, source_label, source_access_id) VALUES ('upload', 'Mill Data 2', 'mill_data2');
INSERT INTO data_sources(source_type, source_label, source_access_id) VALUES ('upload', 'Mill Data 3', 'mill_data3');
-- END DUMMY DATA

CREATE DATABASE upload_data;
\c upload_data
-- CREATE TABLE owners (
--     user_id,
--     data_table,
--     PRIMARY KEY (user_id, data_table)
-- )


-- DUMMY DATA
CREATE TABLE mill_data (
    item_id SERIAL PRIMARY KEY,
    mill_id VARCHAR(100),
    process_time INT,
    defects INT,
    part_id VARCHAR(100),
    total_parts INT
);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 103, 2, 'Axle', 1);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 88, 3, 'Axle', 1);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 91, 20, 'Axle', 2);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 103, 6, 'Tooling', 1);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 106, 6, 'Tooling', 2);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 106, 18, 'Axle', 2);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 110, 27, 'Tooling', 3);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 113, 32, 'Casing', 4);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 94, 15, 'Gear', 3);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 155, 3, 'Bracket', 1);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 160, 10, 'Axle', 2);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 116, 45, 'Axle', 5);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 97, 8, 'Axle', 4);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 100, 15, 'Bracket', 5);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 165, 27, 'Axle', 3);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 120, 54, 'Tooling', 6);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 170, 36, 'Casing', 4);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 123, 63, 'Tooling', 7);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 110, 15, 'Casing', 3);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 102, 60, 'Gear', 6);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 105, 28, 'Tooling', 7);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 175, 10, 'Casing', 5);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 180, 36, 'Gear', 6);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 185, 42, 'Axle', 7);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 113, 40, 'Gear', 4);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 116, 45, 'Casing', 5);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 120, 42, 'Casing', 6);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 190, 8, 'Tooling', 8);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 108, 72, 'Bracket', 8);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 195, 72, 'Tooling', 9);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 150, 40, 'Axle', 10);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 123, 56, 'Tooling', 7);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 126, 8, 'Casing', 8);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 126, 72, 'Axle', 8);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 130, 54, 'Bracket', 9);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 111, 27, 'Bracket', 9);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 130, 72, 'Casing', 9);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 100, 20, 'Axle', 10);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 100, 90, 'Gear', 10);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 103, 110, 'Axle', 11);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 103, 99, 'Casing', 11);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 106, 72, 'Tooling', 12);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 155, 33, 'Gear', 11);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 110, 91, 'Casing', 13);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 85, 70, 'Bracket', 10);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 88, 66, 'Casing', 11);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 91, 60, 'Casing', 12);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 113, 56, 'Bracket', 14);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 106, 12, 'Casing', 12);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 94, 39, 'Casing', 13);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 97, 14, 'Tooling', 14);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 110, 26, 'Gear', 13);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 160, 12, 'Tooling', 12);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 113, 56, 'Gear', 14);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 116, 30, 'Tooling', 15);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 116, 105, 'Bracket', 15);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 165, 91, 'Axle', 13);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 170, 28, 'Tooling', 14);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 100, 150, 'Gear', 15);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 175, 75, 'Tooling', 15);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 120, 80, 'Tooling', 16);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 123, 153, 'Axle', 17);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 180, 128, 'Gear', 16);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 185, 102, 'Bracket', 17);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 190, 144, 'Bracket', 18);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 120, 144, 'Bracket', 16);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 195, 114, 'Axle', 19);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 150, 120, 'Gear', 20);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 155, 168, 'Tooling', 21);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 123, 102, 'Gear', 17);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 102, 32, 'Axle', 16);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 126, 180, 'Axle', 18);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 126, 36, 'Gear', 18);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 130, 38, 'Bracket', 19);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 100, 80, 'Axle', 20);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 130, 57, 'Axle', 19);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 160, 220, 'Bracket', 22);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 165, 184, 'Tooling', 23);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 105, 85, 'Axle', 17);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 103, 147, 'Gear', 21);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 170, 192, 'Tooling', 24);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 100, 200, 'Bracket', 20);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 175, 175, 'Gear', 25);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 108, 126, 'Casing', 18);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 111, 190, 'Tooling', 19);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 106, 66, 'Casing', 22);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 110, 46, 'Tooling', 23);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 180, 156, 'Casing', 26);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 103, 63, 'Tooling', 21);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 85, 160, 'Axle', 20);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-90', 185, 54, 'Gear', 27);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 106, 220, 'Tooling', 22);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 113, 96, 'Gear', 24);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 110, 92, 'Bracket', 23);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 116, 200, 'Gear', 25);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 88, 147, 'Tooling', 21);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-120X', 113, 240, 'Tooling', 24);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 91, 66, 'Casing', 22);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-1200X', 94, 115, 'Gear', 23);
INSERT INTO mill_data (mill_id, process_time, defects, part_id, total_parts) VALUES ('M-100X', 120, 78, 'Gear', 26);
-- END DUMMY DATA