from gpiozero import Button
from signal import pause
from pygame import mixer
import pyaudio
import wave
import datetime
import atexit
import configparser
from os.path import isfile, isdir
from os import makedirs

# Read config data from the config file
config = configparser.ConfigParser()
config.read("config.cfg")
greeting_path = config["Files"]["greeting_path"]
output_folder = config["Files"]["output_folder"]
handset_signal_pin = config["GPIO"]["handset_signal_pin"]

# Check if the output folder exists. Error if it exists and is a file, create it if it doesn't exist
if not isdir(output_folder):
    if isfile(output_folder):
        print("ERROR: Output folder is actually a file! Terminating...")
        quit()
    else:
        makedirs(output_folder)

# Configure settings for the recording device
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
p = pyaudio.PyAudio()

# Initialise the GPIO button
handset_switch = Button(handset_signal_pin, bounce_time=0.25)

# Initialise greeting playback
if not isfile(greeting_path):
    print(f"ERROR: No greeting file at {greeting_path}")
    quit()
mixer.init()
greeting = mixer.Sound(greeting_path)

def recordAudio():
    # Generate filename for current recording based on configured folder path and current time
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{output_folder}recording-{str(current_time)}.wav"
    
    # If the file exists, create a versioned copy.
    # This should almost never run if using timestamps, but on the rare chance that
    # the system clock resets after a power cycle it would be possible to overwrite
    # a previously written file, and this should prevent that
    file_version = 1
    while isfile(filename):
        filename = f"{output_folder}recording-{str(current_time)} ({file_version}).wav"
        file_version += 1

    # Play greeting audio and begin recording
    greeting.play()
    print("Recording...")

    stream = p.open(format = sample_format,
                    channels = channels,
                    rate = fs,
                    frames_per_buffer =  chunk,
                    input = True)
    
    # Keep recording while handset is lifted and store audio in temp buffer
    frames = []
    while handset_switch.is_pressed:
        data = stream.read(chunk)
        frames.append(data)

    # When handset replaced, write the final data frame and log that recording has ceased
    data = stream.read(chunk)
    frames.append(data)
    stream.stop_stream()
    stream.close()
    print("Recording ended... Writing to " + filename + "...")
    greeting.stop()

    # Write audio from buffer to output file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    print("Write complete")

# Set up event handler to run when the handset is lifted
handset_switch.when_pressed = recordAudio

# Gracefully clean up when exiting using CTRL+C
def exit_handler():
    p.terminate()
    mixer.quit()
    print("Guestbook terminated gracefully")

atexit.register(exit_handler)

print("Ready to record!")

pause()
