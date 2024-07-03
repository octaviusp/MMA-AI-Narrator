

import asyncio
import time
from typing import AsyncIterable, Iterable
import vertexai
import base64
import io
from vertexai.generative_models import GenerativeModel, Part, GenerationResponse, FinishReason, GenerationConfig
from PIL import Image

# Initialize Vertex AI
vertexai.init(project="elemental-leaf-424516-r7", location="southamerica-east1")

# Define the model
model = GenerativeModel(model_name="gemini-1.5-flash-001")

# Base64 encoded image string (replace this with your base64 string)
base64_image = ""

# Decode the base64 string
image_data = base64.b64decode(base64_image)

from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory


# Assuming GenerationResponse and model are already defined
generation_config =   GenerationConfig(temperature=1,
                top_p=0.2,
                top_k=1,
                candidate_count=1,
                max_output_tokens=15,
                stop_sequences=["STOP"]
            )



def gen():
    response_generator: GenerationResponse = model._generate_content(
        [
            Part.from_data(image_data, "image/jpeg"),
            """You are an AI MMA Fight Narrator. Comment on received fight situations dramatically with brief and short words.
                Your response must be no greater than 6 words. Answer directly the dramatic commentary.
                Examples:
                    Scene: fighter throw a kick to the head of the other.
                    You: Ouuu! what a kick!!!
                    Scene: fighter doing a takedown to the other.
                    You: Great takedown!
                    Scene: fighter dodge an attack.
                    You: Wow! Awesome response speed!
    """
        ],generation_config=generation_config,safety_settings={
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            }
    )
    return response_generator


response = gen().candidates[0].content.text
print(response)

"""async for txt in response:
        candidate = txt.candidates[0]
        if candidate.finish_reason == 1:
            break
        else:
            print(candidate.content.text)"""
