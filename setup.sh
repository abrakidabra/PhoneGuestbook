#!/usr/bin/env bash

cd "$(dirname "$0")"
sudo apt update
sudo apt full-upgrade -y

# Install python dev tools and pyaudio dependencies to allow building pip packages in the venv
sudo apt install git python3-dev portaudio19-dev -y

# Download guestbook code and change to the code directory
git clone https://github.com/abrakidabra/PhoneGuestbook.git ./PhoneGuestbook
cd PhoneGuestbook

# Create virtualenv and source it
python -m venv .venv
. .venv/bin/activate

# Install required pip packages into the venv
pip install gpiozero lgpio pyaudio

# Sleep for a second to improve reliability of script
sleep 1

# Patch lgpio to work on the Pi 5
sed -i 's/chip = 4/chip = 0/g' .venv/lib/python3.11/site-packages/gpiozero/pins/lgpio.py

echo "Setup completed! Please reboot, then run PhoneGuestbook/run.sh to start the program"
