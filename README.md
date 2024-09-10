# Phone Guestbook
This script turns a Raspberry Pi 5 into a digital audio guestbook, intended to be connected to a converted classic phone

## How to install
Write a fresh Raspberry Pi OS 64it Lite image to an SD card and run it on your Pi

Run `curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/abrakidabra/PhoneGuestbook/main/setup.sh | bash` on the pi

This will install updates, required dependencies, python packages, and patch gpiozero to work on the Pi 5

Once it is complete reboot the pi and run the `run.sh` script
