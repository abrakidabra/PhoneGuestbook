from gpiozero import Button
from signal import pause
from pygame import mixer
import pyaudio
import wave
import datetime
import atexit

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
p = pyaudio.PyAudio()

button = Button(5, bounce_time=0.25)

mixer.init()

greeting = mixer.Sound("greeting.wav")

def recordAudio():
    global message_count
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"recording-{str(current_time)}.wav"
    greeting.play()
    print("Recording...")

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
    print("Recording ended... Writing to " + filename + "...")
    greeting.stop()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    print("Write complete")

button.when_pressed = recordAudio

def exit_handler():
    p.terminate()
    mixer.quit()

atexit.register(exit_handler)

print("Ready to record!")

pause()
