#!/home/user/.venv/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess
import requests
import datetime
import re

# URL to crawl for APRS data (REST API)
aprs_url = "https://api.aprs.fi/api/get?name=CALLSIGN-SUFFIX&what=wx&apikey=APIKEY&format=json"

# Path to your ChromeDriver
chromedriver_path = '/usr/bin/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = '/usr/bin/google-chrome'  # Path to google-chrome binary
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
chrome_options.add_argument('--disable-gpu')  # Disable GPU, for headless Chrome
chrome_options.add_argument('--remote-debugging-port=9222')  # Avoid DevToolsActivePort issue

# Get today's date
today_date = datetime.datetime.today().strftime('%Y-%m-%d')

# Set up ChromeDriver service
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the APRS URL in ChromeDriver to capture the response
driver.get(aprs_url)

# Extract the rendered HTML content (APRS weather data in this case)
html_content = driver.page_source

# Save the HTML to a file for debugging (optional)
output_file = 'rendered_page.html'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"Rendered HTML saved to {output_file}")

# Close the ChromeDriver session
driver.quit()

# Fetch APRS weather data using requests (REST API call)
try:
    aprs_response = requests.get(aprs_url)
    aprs_data = aprs_response.json()

    # Extract data from the APRS API response
    if aprs_data['result'] == 'ok':
        aprs_entry = aprs_data['entries'][0]  # Getting the first (and possibly only) entry
        aprs_temperature = float(aprs_entry['temp'])
        aprs_humidity = int(aprs_entry['humidity'])
        aprs_pressure = float(aprs_entry['pressure'])

        print(f"APRS Weather Data:")
        print(f"Temperature: {aprs_temperature:.2f}°C")
        print(f"Humidity: {aprs_humidity}%")
        print(f"Barometric Pressure: {aprs_pressure:.1f} millibars (hPa)")
    else:
        print("Error fetching APRS weather data.")

except Exception as e:
    print(f"An unexpected error occurred while fetching APRS data: {e}")

# Define the weather API URL with today's date (MetMalaysia API)
met_url = f"https://api.met.gov.my/v2.1/data?datasetid=FORECAST&datacategoryid=GENERAL&locationid=LOCATION:300&start_date={today_date}&end_date={today_date}"

# API headers for MetMalaysia API
headers = {
    "Authorization": "METToken YOURTOKENKEYFROMMET"
}

# Fetch weather condition from the MetMalaysia API
try:
    weather_response = requests.get(met_url, headers=headers)
    weather_data = weather_response.json()

    # Extract the weather condition (MetMalaysia data)
    weather_condition = None
    for result in weather_data['results']:
        if result['datatype'] == 'FSIGW':
            weather_condition = result['value']
            break

    if weather_condition:
        print(f"MetMalaysia Weather Condition: {weather_condition}")
    else:
        print("Weather condition not found in the MetMalaysia API response.")
except Exception as e:
    print(f"An unexpected error occurred while fetching MetMalaysia weather data: {e}")

# Combine data from APRS and MetMalaysia and construct bash command
try:
    # Construct the bash command using both APRS and MetMalaysia data
    bash_command = f"""
    /root/aprs-weather-submit/aprs-weather-submit --callsign 9W4GWK-13 --latitude 3.001320 --longitude 101.567828 --altitude 100 --server aprs.my --port 14580 --username USERCALLSIGN --password YOURPASSWORD -M "Sky conditions: {weather_condition} CALLSIGN-API WX" -T "{aprs_temperature:.2f}" -h "{aprs_humidity}" -b "{aprs_pressure:.1f                                                                                }" > /dev/null 2>&1
    """
    print("Bash command to execute:")
    print(bash_command)

    # Execute the bash command
    subprocess.run(bash_command, shell=True)
except Exception as e:
    print(f"An error occurred while constructing or executing the bash command: {e}")
