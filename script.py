import psycopg2
import time
from datetime import datetime
import random
from dotenv import load_dotenv
import os

load_dotenv()

dbConfig = {
    "dbname": os.getenv("dbName"),
    "user": os.getenv("dbUser"),
    "password": os.getenv("dbPassword"),
    "host": os.getenv("dbHost"),
    "port": os.getenv("dbPort"),
}

class WeatherSimulator:
    def __init__(self):
        self.currentTemp = random.uniform(0, 15)
        self.currentHumidity = random.randint(60, 80)
        self.currentPressure = random.uniform(740, 750)
        self.currentWind = random.uniform(1, 3)

    def updateWeather(self):
        tempChange = random.uniform(-0.2, 0.2)
        self.currentTemp = max(-30, min(40, self.currentTemp + tempChange))

        humidityChange = random.uniform(-0.5, 0.5)
        self.currentHumidity = max(
            40, min(100, self.currentHumidity + humidityChange)
        )
        if self.currentTemp > 15:
            self.currentHumidity = min(self.currentHumidity, 85)
        elif self.currentTemp < 0:
            self.currentHumidity = max(self.currentHumidity, 65)

        pressureChange = random.uniform(-0.05, 0.05)
        self.currentPressure += pressureChange
        self.currentPressure = max(720, min(780, self.currentPressure))

        windChange = random.uniform(-0.4, 0.4)
        self.currentWind = max(0, self.currentWind + windChange)

        return {
            "temperature": round(self.currentTemp, 2),
            "humidity": int(self.currentHumidity),
            "pressure": round(self.currentPressure, 2),
            "windSpeed": round(self.currentWind, 2),
        }


def insertWeatherDataToDb(data):
    try:
        conn = psycopg2.connect(**dbConfig)
        cur = conn.cursor()

        insertQuery = """
        INSERT INTO weather_station_data 
        (timestamp, temperature, humidity, pressure, wind_speed)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(
            insertQuery,
            (
                datetime.now(),
                data["temperature"],
                data["humidity"],
                data["pressure"],
                data["windSpeed"],
            ),
        )

        conn.commit()
        print(
            f"Запись добавлена: {datetime.now().strftime('%D %H:%M:%S')}, "
            f"T={data['temperature']}°C, H={data['humidity']}%, P={data['pressure']}мм, W={data['windSpeed']}м/с"
        )

    except psycopg2.Error as e:
        print(f"Ошибка при работе с БД: {e}")
    finally:
        cur.close()
        conn.close()


def main():
    simulator = WeatherSimulator()
    while True:
        weatherData = simulator.updateWeather()
        insertWeatherDataToDb(weatherData)
        time.sleep(1)


if __name__ == "__main__":
    main()