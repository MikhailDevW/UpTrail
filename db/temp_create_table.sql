CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS track (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT(10000),
    datetime_start TIMESTAMPTZ,
    author VARCHAR(255) NOT NULL,
    latitude_start FLOAT NOT NULL CHECK (latitude_start >= 0 AND latitude_start <= 90),
    longitude_start FLOAT NOT NULL CHECK (longitude_start >= 0 AND longitude_start <= 180),
    actual_route_length VARCHAR(255),
    gps_file JSONB NOT NULL
);
