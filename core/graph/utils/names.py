# NOMBRE DE LOS AGENTES, FUNDAMENTAL ESCRIBIR BIEN
narrator_text = "narrator_text"
narrator_vision = "narrator_vision"
narrator_voice = "narrator_voice"

# NOMBRE DE LAS TOOLS, PONER CORRECTAMENTE
rollback = "rollback"
delegate = "delegate"
youtube_tool = "youtube"
script_executor = "script_executor"
tool_node = "tools"

# agregar aca todos los que puede llamar el orhcestrator, es para el prompt!
# ver: narrator_text_node - system prompt


#OPERATING SYSTEM
narrator_vision_call = f"\nNAME: '{narrator_vision}' ACTION:This agent is a python coder that executes scripts and interact with the operating system api via python."

narrator_text_possible_agent_calls = [narrator_vision_call]
