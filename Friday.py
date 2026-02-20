from fastrtc import ReplyOnPause,Stream,get_tts_model,get_stt_model
from gradio_client import Client
import requests

stt_model=get_stt_model()
tts_model=get_tts_model()

OLLAMA_URL="http://localhost:11434/api/generate"

def echo(audio):
    user_text=stt_model.stt(audio)
    print("User:",user_text)

    response=requests.post(
        OLLAMA_URL,
        json={
            "model":"gemma3:1b",
            "prompt":user_text,
            "stream":False,
            "prompt":"Your name is Friday."
        }
    )
    reply=response.json()["response"]
    print("AI:",reply)

    for chunk in tts_model.stream_tts_sync(reply):
        yield chunk

stream=Stream(ReplyOnPause(echo),modality="audio",mode="send-receive")
stream.ui.launch()