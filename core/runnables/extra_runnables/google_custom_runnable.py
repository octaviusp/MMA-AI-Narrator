from core.graph.state.state_definition import State

from langchain_core.runnables import Runnable, RunnableConfig

from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from vertexai.generative_models import GenerativeModel, Part, GenerationResponse, GenerationConfig

import vertexai
import base64

class GoogleRunnable(Runnable):
    """
        Google Custom Runnable - Inference endpoint for gemini.
    """
    def __init__(self, name: str, prompt: str, project_id: str, location: str, model: str = "gemini-1.5-flash-001"):
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        # Define the model
        
        generation_config = GenerationConfig(
            temperature=1,
            top_p=0.2,
            top_k=1,
            candidate_count=1,
            max_output_tokens=15,
            stop_sequences=["STOP"]
        )

        safety_settings={
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = GenerativeModel(model_name=model, generation_config=generation_config, safety_settings=safety_settings)
        self.name = name
        self.prompt = prompt

    def invoke(self,state: State, config: RunnableConfig) -> str:
        # Base64 encoded image string (replace this with your base64 string)
        base64_image = state.get("frames_b64")

        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_image[0])

        response_generator: GenerationResponse = self.model._generate_content(
            [
                Part.from_data(image_data, "image/jpeg"),
                self.prompt
            ], 
            
        )
        
        return response_generator.candidates[0].content.text

    async def ainvoke(self,state: State, config: RunnableConfig) -> str:
        # Base64 encoded image string (replace this with your base64 string)
        base64_image = state.get("frames_b64")

        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_image[0])

        response_generator: GenerationResponse = await self.model._generate_content_async(
            [
                Part.from_data(image_data, "image/jpeg"),
                self.prompt
            ], 
            
        )
        
        return response_generator.candidates[0].content.text
