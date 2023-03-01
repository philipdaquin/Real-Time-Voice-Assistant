# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=bad-identation
# pylint: disable=invalid-name
# pylint: disable=broad-exception-caught




import pyaudio
import asyncio
import base64
import json
import openai
import os
import websockets
from chat_helper import send_message


# Setup Microphone recording
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

APIKEY = os.getenv("ASSEMBLYAI_API_KEY")

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
        session_begins = await _ws.recv()

        print(session_begins)
        print("Sending messages ")

        async def send():
            while True:
                try:
                    raw_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    voice_data = base64.b16encode(raw_data).decode("utf-8")
                    json_object = json.dumps({"audio_data": str(voice_data)})
                    await _ws.send(json_object)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error: " + str(e)
                await asyncio.sleep(0.01)


        async def receive():
            while True:
                try:
                    result = await _ws.recv()
                    results = json.loads(result)
                    prompt = results["text"]

                    if prompt and results["message_type"] == "FinalTranscript":
                        resp = send_message(prompt)
                        # print("Me:", prompt)
                        print("Bot:", resp)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error: " + str(e)
                await asyncio.sleep(0.01)
                
        sendResult, receiveResult = await asyncio.gather(send(), receive())
asyncio.run(send_recv())