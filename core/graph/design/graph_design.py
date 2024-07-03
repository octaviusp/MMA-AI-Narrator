import time
from core.graph.nodes.agents import (
    narrator_text_node,
    narrator_vision_node,
    narrator_voice_node)

from core.graph.state.state_definition import State
from core.graph.utils.names import (
    narrator_text,
    narrator_vision,
    narrator_voice,
)

from core.runnables.executor.runnable_executor import RunnableExecutor

from logger.logger import Logger

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END


############################################################
#################### NAMES, GRAPHS, RUNNABLES        #######
############################################################

Logger.info("Setting up Graph... ", __name__)

graph = StateGraph(State)

############################################################
#################### ASYNCS DEFINITIONS  #######
############################################################

narrator_text_runnable = RunnableExecutor(narrator_text_node.runnable)
async def narrator_text_run_func(state: State, config: RunnableConfig):
    start = time.time()
    response = await narrator_text_runnable.__call__(state, config=config)
    Logger.info(f"- Narrator TEXT runnable time elapsed: {time.time() - start}", __name__)
    return response

narrator_vision_runnable = narrator_vision_node.runnable
async def narrator_vision_run_func(state: State, config: RunnableConfig):
    start = time.time()
    response = await narrator_vision_runnable.__call__(state, config=config)
    Logger.info(f"- Narrator VISION runnable time elapsed: {time.time() - start}", __name__)
    return response

narrator_voice_runnable = narrator_voice_node.runnable
async def narrator_voice_run_func(state: State, config: RunnableConfig):
    start = time.time()
    response = await narrator_voice_runnable.__call__(state, config=config)
    Logger.info(f"- Narrator VOICE runnable time elapsed: {time.time() - start}", __name__)
    return response

# narrator_text agent
narrator_text_run = narrator_text_run_func
# vision system agent
narrator_vision_run = narrator_vision_run_func
# speech recognition system
narrator_voice_run = narrator_voice_run_func
    
############################################################
#################### GRAPH FLOW DESIGN               #######
############################################################

try:
    Logger.info("Creating graph design... ", __name__)

    #graph.add_node(narrator_text, (narrator_text_run))
    graph.add_node(narrator_vision, (narrator_vision_run))
    graph.add_node(narrator_voice, (narrator_voice_run))

    # Edges
    #graph.add_edge(narrator_vision, END)
    graph.add_edge(narrator_vision, narrator_voice)
    #graph.add_edge(narrator_text, narrator_voice)
    graph.add_edge(narrator_voice, END)

    graph.set_entry_point(narrator_vision)
    
    Logger.info(f"Graph entry point... {narrator_vision}", __name__)

    # Guardando la instancia del grafo creada
    graph_created = graph
    Logger.info(f"Graph created successfully!", __name__)
except Exception as e:
    Logger.critical("Error creating the graph: " + str(type(e)), __name__)
