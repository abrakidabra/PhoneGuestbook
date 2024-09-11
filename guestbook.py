from gpiozero import Button
from signal import pause
from pygame import mixer
import pyaudio
import wave
import datetime
import atexit
import configparser

# Read config data from the config file
config = configparser.ConfigParser()
config.read("config.cfg")
greeting_path = config["Files"]["greeting_path"]
output_folder = config["Files"]["output_folder"]
handset_signal_pin = config["GPIO"]["handset_signal_pin"]

# Configure settings for the recording device
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
p = pyaudio.PyAudio()

# Initialise the GPIO button
handset_switch = Button(handset_signal_pin, bounce_time=0.25)

# Initialise greeting playback
mixer.init()
greeting = mixer.Sound(greeting_path)

def recordAudio():
    # Generate filename for current recording based on configured folder path and current time
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{output_folder}recording-{str(current_time)}.wav"
    
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

# Set up event handler for the
handset_switch.when_pressed = recordAudio

def exit_handler():
    p.terminate()
    mixer.quit()
    print("Guestbook terminated gracefully")

atexit.register(exit_handler)

print("Ready to record!")

pause()
