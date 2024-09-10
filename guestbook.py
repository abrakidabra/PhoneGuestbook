from gpiozero import Button
from signal import pause
import pyaudio
import wave
import datetime

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100

p = pyaudio.PyAudio()

button = Button(5)

def recordAudio():
    global message_count
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"recording-{str(current_time)}.wav"
    print ("recording...")

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
    print("... Ending Recording")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

button.when_pressed = recordAudio

pause()
