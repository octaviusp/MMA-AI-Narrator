from core.runnables.executor.runnable_executor import GoogleRunnableExecutor, NvidiaVisionModel, OpenAIVisionModel
from core.runnables.extra_runnables.google_custom_runnable import GoogleRunnable
from core.runnables.models_selection.vision_selection import VisionRecognition
from core.graph.utils.names import narrator_vision


prompt = """
Analyze the provided images of an MMA fight:
Movements: Identify specific movements (e.g., jab, cross, uppercut, kick).
Techniques: Highlight techniques used (e.g., armbar, choke, takedown).
Dominance: Indie which fighter is dominating and control positions (e.g., mount, side control).
Context: Describe fight dynamics, momentum shifts, and strategies.
Focus only on the two fighters. Make a brief summary of what is happening right now.
"""

google_runnable = GoogleRunnable(name=narrator_vision,prompt=prompt, project_id="elemental-leaf-424516-r7", location="southamerica-east1")
runnable = GoogleRunnableExecutor(runnable=google_runnable)
#runnable = NvidiaVisionModel(vision_prompt=prompt,
#                            name=narrator_vision,
#                            model=VisionRecognition.Model.nvidia_neva_22b.value)

#client = VisionRecognition.OpenAI_Vision()
#runnable = OpenAIVisionModel(client=client, vision_prompt=prompt, name=narrator_vision)