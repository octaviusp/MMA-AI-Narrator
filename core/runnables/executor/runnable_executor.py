from config.config import KEYS, config_instance

from core.runnables.extra_runnables.google_custom_runnable import GoogleRunnable
from core.graph.state.state_definition import State
from core.graph.utils.message_converter import turn_to
from core.graph.utils.names import (
    narrator_text
)

from core.models.messages import (
    AIMessage,
    NarratorSpeechMessage,
    FightVisionMessage,
    SpeechRecognitionBytesMessage
)

from core.graph.state.state_definition import State
from exceptions.exceptions import NetworkCallException
from logger.logger import Logger

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)

from openai import AsyncOpenAI
from typing import Callable, Iterator

import httpx
import asyncio
import time

class RunnableExecutor:
    """
    Base class for executing all Runnables (Agents, Tools, etc...)
    """
    def __init__(self, runnable: Runnable, max_retries: int = 2):
        self.runnable = runnable
        self.name = runnable.name
        self.max_retries = max_retries

    async def __invoke(self, state: State, config: RunnableConfig):
        Logger.debug(f"{self.name} __INVOKE", __name__)
        result = await self.runnable.ainvoke(state, config=config)
        result = AIMessage(content=result.content, response_metadata=result.response_metadata)
        # Ensure tool call responses are handled correctly
        if not result.additional_kwargs.get('tool_calls', []) and (
            not result.content
            or isinstance(result.content, list)
            and not result.content[0].get("text")
        ):
            human_message_handle = HumanMessage(content="Please, respond with a real output.")
            messages += [human_message_handle]

        return result
    
    async def __call__(self, state: State, config: RunnableConfig, invoke_funk: Callable = None):
        Logger.debug(f"{self.name}: Running inference", __name__)
        result = None
        try:
            for i in range(self.max_retries):
                try:
                    result = (await self.__invoke(state, config)) if not invoke_funk else (await invoke_funk(state, config))
                    break
                except Exception as e:
                    Logger.error(f"__call__ Error during runnable invocation or message processing: {str(e)}", __name__)
                    continue  # Optionally, could handle differently or re-raise after logging
                finally:
                    if self.max_retries - 1 == i:
                        return {
                            "messages": AIMessage(content="I can't resolve the task. Retry.")
                        }

            if isinstance(result, BaseMessage):
                result = self.__get_message_type(
                    runnable=self.runnable,
                    from_=result
                )
            
            Logger.debug(f"{self.name}: Response done, updating state messages...", __name__)

            return {
                "messages": result
            }
        except Exception as e:
            Logger.error(f"Error in RunnableExecutor call method: {e}", __name__)
            return {"messages": [f"An error occurred: {str(e)}"]}  # Provide fallback state or raise

    def __get_message_type(self, runnable: Runnable, from_: BaseMessage):
        try:
            name = runnable.name
            
            if name == narrator_text:
                return turn_to(from_, NarratorSpeechMessage)
            
            return from_
        except Exception as e:
            Logger.error(f"Error converting message type in __get_message_type: {e}", __name__)
            return from_  # Return the original message as a fallback

class GoogleRunnableExecutor(RunnableExecutor):
    def __init__(self, runnable: GoogleRunnable, max_retries: int = 2):
        super().__init__(runnable=runnable, max_retries=max_retries)

    async def __invoke(self, state: State, config: RunnableConfig):
        Logger.debug(f"{self.name} __INVOKE", __name__)
        result = await self.runnable.ainvoke(state, config=config)
        result = AIMessage(content=result)
        return result

    async def __call__(self, state: State, config: RunnableConfig, invoke_funk: Callable = None):
        Logger.debug(f"{self.name}: Running inference", __name__)
        result = None
        try:
            for i in range(self.max_retries):
                try:
                    result = (await self.__invoke(state, config)) if not invoke_funk else (await invoke_funk(state, config))
                    break
                except Exception as e:
                    Logger.error(f"__call__ Error during runnable invocation or message processing: {str(e)}", __name__)
                    continue  # Optionally, could handle differently or re-raise after logging
                finally:
                    if self.max_retries - 1 == i:
                        return {
                            "messages": AIMessage(content="I can't resolve the task. Retry.")
                        }

            if isinstance(result, BaseMessage):
                result = self.__get_message_type(
                    runnable=self.runnable,
                    from_=result
                )
            
            Logger.debug(f"{self.name}: Response done, updating state messages...", __name__)

            return {
                "messages": result
            }
        except Exception as e:
            Logger.error(f"Error in RunnableExecutor call method: {e}", __name__)
            return {"messages": [f"An error occurred: {str(e)}"]}  # Provide fallback state or raise

    def __get_message_type(self, runnable: Runnable, from_: BaseMessage):
        try:
            name = runnable.name
            
            if name == narrator_text:
                return turn_to(from_, NarratorSpeechMessage)
            
            return from_
        except Exception as e:
            Logger.error(f"Error converting message type in __get_message_type: {e}", __name__)
            return from_  # Return the original message as a fallback
        
class OpenAISpeechRecognitionModel(RunnableExecutor):
    def __init__(self, name: str,
                client: AsyncOpenAI,
                voice: str = "echo",
                model: str = "tts-1",
                speed: float = 1.0,
                max_retries: int = 2):
        self.name = name
        self.client = client
        self.voice = voice
        self.model = model
        self.speed = speed
        self.max_retries = max_retries

    async def create_speech(self, narration: str) -> Iterator[bytes]:
        try:
            client_response = await self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                speed=self.speed,
                input=narration
            )
            return client_response.iter_bytes()
        except Exception as e:
            return None

    async def __invoke(self, state: State, config: RunnableConfig):
        Logger.debug(f"{self.name} __INVOKE", __name__)

        # Obtener el último mensaje del estado
        narration = state["messages"][-1].content

        if not narration:
            raise ValueError("Narration from state messages must not be empty.")

        # Realizar la inferencia de TTS
        speech_response = await self.create_speech(narration)
        return SpeechRecognitionBytesMessage(content="TTS Done", additional_kwargs={"iterator_bytes": speech_response})   

    async def __call__(self, state: State, config: RunnableConfig, invoke_funk: Callable = None):
        Logger.debug(f"{self.name}: Running inference", __name__)
        result = None
        try:
            for i in range(self.max_retries):
                try:
                    result = (await self.__invoke(state, config)) if not invoke_funk else (await invoke_funk(state, config))
                    break
                except Exception as e:
                    Logger.error(f"__call__ Error during runnable invocation or message processing: {e}", __name__)
                    continue  # Optionally, could handle differently or re-raise after logging
                finally:
                    if self.max_retries - 1 == i:
                        return {
                            "messages": AIMessage(content="I can't resolve the task. Retry.")
                        }
            
            Logger.debug(f"{self.name}: Response done, updating state messages...", __name__)

            return {
                "messages": result
            }
        except Exception as e:
            Logger.error(f"Error in OpenAISpeechRecognitionModel call method: {e}", __name__)
            return {"messages": [f"An error occurred extracting information from fight video. I don't have any fight situations."]}  # Provide fallback state or raise

class NvidiaVisionModel(RunnableExecutor):
    """
    Base class for executing vision models via API.
    """
    def __init__(self,name:str,
                vision_prompt: str,
                api_key: str = "",
                streaming: bool = False,
                max_retries: int = 2,
                max_tokens: int = 1024,
                temperature: int = 1,
                top_p: int = 0.2,
                seed: int = 0,
                invoke_url: str = "https://ai.api.nvidia.com/v1/vlm/",
                model: str = "nvidia/neva-22b"):
        
        self.name = name
        self.api_key = config_instance.get_env(KEYS.NVIDIA_API_KEY) if not api_key else api_key
        self.vision_prompt = vision_prompt
        self.max_retries = max_retries
        self.stream = streaming
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.seed = seed
        self.model = model
        self.invoke_url = invoke_url + model

    async def __invoke(self, state: State, config: RunnableConfig):
        Logger.debug(f"{self.name} __INVOKE", __name__)
        
        start_time = time.time()

        frames_b64 = state.get("frames_b64")
        # assert len(frames_b64) == 5, "Expected exactly 5 frames in the list."

        invoke_url = self.invoke_url
        stream = self.stream
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream" if stream else "application/json"
        }

        async def fetch_response(image_b64):
            async with httpx.AsyncClient() as client:
                assert len(image_b64) < 180_000, "To upload larger images, use the assets API (see docs)"

                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": self.vision_prompt + f'''<img src="data:image/png;base64,{image_b64}" />'''
                        }
                    ],
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    #"seed": self.seed,
                    "stream": stream
                }
                try:
                    response = await client.post(invoke_url, headers=headers, json=payload)
                except Exception as e:
                    raise NetworkCallException(message="Network error")
                if stream:
                    async for line in response.aiter_lines():
                        if line:
                            return f"situation: {line.strip()}"
                else:
                    response_json = response.json()
                    return f"THIS HAPPENS NOW: {response_json['choices'][0]['message']['content'].strip()}"

        try:
            tasks = [fetch_response(image_b64) for image_b64 in frames_b64]
            responses = await asyncio.gather(*tasks)

            elapsed_time = time.time() - start_time
            Logger.debug(f"{self.name} inference time elapsed: {elapsed_time:.2f} seconds", __name__)

            return FightVisionMessage(content="\n".join(responses))
        except Exception as e:
            Logger.error(str(e), __name__)
            return FightVisionMessage(content="Sorry, vision model can't capture fight moments.")

    async def __call__(self, state: State, config: RunnableConfig, invoke_funk: Callable = None):
        Logger.debug(f"{self.name}: Running inference", __name__)
        result = None
        try:
            for i in range(self.max_retries):
                try:
                    result = (await self.__invoke(state, config)) if not invoke_funk else (await invoke_funk(state, config))
                    break
                except Exception as e:
                    Logger.error(f"__call__ Error during runnable invocation or message processing: {e}", __name__)
                    continue  # Optionally, could handle differently or re-raise after logging
                finally:
                    if self.max_retries - 1 == i:
                        return {
                            "messages": AIMessage(content="I can't resolve the task. Retry.")
                        }
            
            Logger.debug(f"{self.name}: Response done, updating state messages...", __name__)

            return {
                "messages": result
            }
        except Exception as e:
            Logger.error(f"Error in NvidiaVisionModel call method: {e}", __name__)
            return {"messages": [f"An error occurred extracting information from fight video. I don't have any fight situations."]}  # Provide fallback state or raise
        
class OpenAIVisionModel(RunnableExecutor):
    """
    Base class for executing vision models via OpenAI API.
    """
    def __init__(self, name: str,
                 client: AsyncOpenAI,
                 vision_prompt: str,
                 streaming: bool = False,
                 max_retries: int = 2,
                 max_tokens: int = 1024,
                 temperature: int = 1,
                 top_p: int = 0.2,
                 seed: int = 0,
                 invoke_url: str = "https://api.openai.com/v1/",
                 model: str = "gpt-4o"):
        
        self.name = name
        self.client = client
        self.api_key = config_instance.get_env(KEYS.OPENAI_API_KEY)
        self.vision_prompt = vision_prompt
        self.max_retries = max_retries
        self.streaming = streaming
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.seed = seed
        self.model = model
        self.invoke_url = invoke_url + "chat/completions"

    async def __invoke(self, state: State, config: RunnableConfig):
        Logger.debug(f"{self.name} __INVOKE", __name__)
        
        start_time = time.time()

        frames_b64 = state.get("frames_b64")

        response = await self.get_description(frames_b64)

        return FightVisionMessage(content=response)

    async def get_description(self, frames_b64: list[str]):
        try:
            response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "user",
                "content": [
                        self.vision_prompt,
                        *map(lambda x: {"image": x, "resize": 512}, frames_b64),
                    ],
                }
            ],
            max_tokens=100,
            temperature=self.temperature,
            seed=self.seed,
            stream=self.streaming
            )
            return response.choices[0].message.content
        except Exception as e:
            return "Sorry, vision model can't capture fight moments."

    async def __call__(self, state: State, config: RunnableConfig, invoke_funk: Callable = None):
        Logger.debug(f"{self.name}: Running inference", __name__)
        result = None
        try:
            for i in range(self.max_retries):
                try:
                    result = (await self.__invoke(state, config)) if not invoke_funk else (await invoke_funk(state, config))
                    break
                except Exception as e:
                    Logger.error(f"__call__ Error during runnable invocation or message processing: {e}", __name__)
                    continue  # Optionally, could handle differently or re-raise after logging
                finally:
                    if self.max_retries - 1 == i:
                        return {
                            "messages": AIMessage(content="I can't resolve the task. Retry.")
                        }
            
            Logger.debug(f"{self.name}: Response done, updating state messages...", __name__)

            return {
                "messages": result
            }
        except Exception as e:
            Logger.error(f"Error in OpenAIVisionModel call method: {e}", __name__)
            return {"messages": [f"An error occurred extracting information from fight video. I don't have any fight situations."]}  # Provide fallback state or raise