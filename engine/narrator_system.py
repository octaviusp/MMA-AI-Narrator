from core.graph.compiled import graph_compiled
from langchain_core.messages import HumanMessage, BaseMessage

from typing import Iterator

import sounddevice as sd
import numpy as np
import io
import soundfile as sf

class NarratorSystem:

    def __init__(self, testing_only_vision: bool):
        self.only_vision = testing_only_vision

    async def generate(self, frames_b64: list[str]) -> BaseMessage:
        input_dict = {
            "messages": HumanMessage(role="user", content="Extract the techniques, the movements and what is happening in this fight:"),
            "history": [],
            "frames_b64": frames_b64
        }

        results = await graph_compiled.ainvoke(
            config={
                "configurable": {
                    "input": "Extract info from image.",
                    "session_id": ""
                }
            },
            input=input_dict
        )

        return results["messages"][-1]

    async def generate_with_audio(self, frames_b64: list[str]) -> Iterator[bytes]:
        response = await self.generate(frames_b64)
        print("- TEXT ANSWER: ", response.content)
        return response.additional_kwargs["iterator_bytes"]
    
    def generate_voice(self, voice_bytes: Iterator[bytes]):
        # Read the audio bytes from the response
        audio_bytes = b''.join(voice_bytes)
        
        # Use an in-memory buffer to convert bytes to an audio stream
        buffer = io.BytesIO(audio_bytes)
        data, samplerate = sf.read(buffer)
        
        # Ensure the audio data is in the correct format for playback
        audio_stream = np.array(data, dtype=np.float32)
        
        return audio_stream, samplerate
    
    def play_audio_stream(self, audio_stream, samplerate):
        sd.play(audio_stream, samplerate=samplerate)
        sd.wait()
    
    async def execute(self, frames_b64: list[str]):
        if self.only_vision:
            response = await self.generate(frames_b64)
            print(response.content)
        else:
            response_bytes = await self.generate_with_audio(frames_b64)
            audio_stream, samplerate = self.generate_voice(response_bytes)
            self.play_audio_stream(audio_stream, samplerate)