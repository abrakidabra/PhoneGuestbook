from gpiozero import Button
from signal import pause
import pyaudio
import wave

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
p = pyaudio.PyAudio()

button = Button(5, bounce_time=0.5)

greeting_path = "greeting.wav"

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
    greeting.stop()

    with wave.open(greeting_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    print("Write complete")
    p.terminate()
    quit()

button.when_pressed = recordAudio

print("Ready to record greeting! Pickup handset and record greeting")

pause()
