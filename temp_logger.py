#!/usr/bin/env python3
import time
import smbus2
import bme280
from datetime import datetime
import csv
import os

address = 0x76
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Data file
DATA_FILE = "temperature_data.csv"

def initialize_csv():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'temperature', 'humidity', 'pressure'])

def log_temperature():
    """Read sensor and log data"""
    data = bme280.sample(bus, address, calibration_params)
    
    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    temp = round(data.temperature * 9/5 + 32, 2)
    humidity = round(data.humidity, 2)
    pressure = round(data.pressure, 2)
    
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, temp, humidity, pressure])
    
    print(f"{timestamp} - Temp: {temp}°F, "
          f"Humidity: {humidity}%, Pressure: {pressure}hPa")

def main():
    initialize_csv()
    print("Temperature monitoring started. Logging every hour...")
    
    while True:
        try:
            log_temperature()
            time.sleep(3600)  # Wait 1 hour (3600 seconds)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait 1 minute

if __name__ == "__main__":
    main()