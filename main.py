
import websockets
import pyaudio
import asyncio
import base64
import json 
import dotenv

# Setup Microphone recording
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

APIKEY = dotenv.load_dotenv("OPENAI_API_KEY")


# Audio Instance 
py = pyaudio.PyAudio()

# Stream 
stream = py.open(
    format=FORMAT,
    channels=CHANNELS,
    frames_per_buffer=FRAMES_PER_BUFFER,
    rate=RATE,
    input=True,
)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=" + str(RATE)
print(URL)
async def send_recv():
    async with websockets.connect(URL, ping_interval=5, ping_timeout=20, extra_headers={"Authorization": APIKEY}) as _ws:
        await asyncio.sleep(0.1)