from gpiozero import Button
from signal import pause
import pyaudio
import wave
import datetime
import configparser
from os.path import isfile, isdir
from shutil import copy2

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
p = pyaudio.PyAudio()

config = configparser.ConfigParser()
config.read("config.cfg")

greeting_path = config["Files"]["greeting_path"]
handset_signal_pin = config["GPIO"]["handset_signal_pin"]

button = Button(handset_signal_pin, bounce_time=0.25)

if isfile(greeting_path):
    if isdir(greeting_path):
        print("Greeting file is actually a directory! Cannot overwrite")
    else:
        print("Greeting file exists. Backing up to" + f'{greeting_path}.bak_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}')
        copy2(greeting_path, f'{greeting_path}.bak_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}')


def recordAudio():
    print("Recording greeting.wav...")

    stream = p.open(format = sample_format,
                    channels = channels,
                    rate = fs,
                    frames_per_buffer =  chunk,
                    input = True)

    frames = []
    while button.is_pressed:
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    print("Recording ended... Writing to " + greeting_path + "...")

    with wave.open(greeting_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    print("Write complete")
    p.terminate()
    exit()

print("Ready to record greeting! Pickup handset and record greeting")

button.wait_for_press()

recordAudio()
