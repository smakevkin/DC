CREATE TABLE IF NOT EXISTS weather_station_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature REAL NOT NULL,
    humidity INTEGER NOT NULL,
    pressure REAL NOT NULL,
    wind_speed REAL NOT NULL
);