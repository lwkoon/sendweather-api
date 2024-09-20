# sendweather-aprsfi-api.py
Get data from MET https://www.met.gov.my/en/ (Malaysian Meteorological Department) and Sending APRS WX api crawler Spider

Get data and post to your own callsign-WX 
you must be a licensed amateur operator to use this

# Prerequisite
Go to https://getwebdriver.com/chromedriver#stable
wget https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.58/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
cp chromedriver /usr/bin/

# installing google chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install ./google-chrome-stable_current_amd64.deb

# pip install
# You need to have python3 installed , i am using Debian 12 with Python 3.11.2 installed
pip install webdriver-manager
pip install selenium

# APT install
apt install xvfb
Xvfb :99 -ac &
export DISPLAY=:99

# edit /etc/rc.local
put this into the startup script
Xvfb :99 -ac &
export DISPLAY=:99

# git clone and compile aprs-weather-submit from (please follow the README.md)
https://github.com/rhymeswithmogul/aprs-weather-submit

# how to enable rc.local for debian/ubuntu system :- https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd

#install VENV environment
virtualenv virtualenv=/usr/bin/python3 /home/user/.venv
source /home/user/.venv/bin/activate

# To run
source /home/user/.venv/bin/activate; /home/user/.venv/bin/python3 /usr/bin/sendweather-aprsfi-api.py

# Crontab
*/5 * * * * source /home/user/.venv/bin/activate; /home/user/.venv/bin/python3 /usr/bin/sendweather-aprsfi-api.py; deactivate
