from core.runnables.tools.rollback import Rollback
from core.runnables.tools.delegate import Delegate
from core.runnables.tools.script_executor import ScriptExecutor

from langchain_core.tools import Tool

class ToolFactory:
    """
        Tools Factory Static class.
        A centralized manner to recovery tools.
    """
    ScriptExecutor = ScriptExecutor()
    """
        Ejecuta scripts en el sistema operativo del usuario y permite interaectuar con este.
    """
    Delegate = Delegate()
    """
        Delega el control del runtime a otro agente, 
        en la mayoria de casos solo usa esta tool el narrator_text.
    """
    Rollback = Rollback()
    """
       Devuelve el control hacia el narrator_text,
       mayormente despues de que un subagente temrine su tarea, devuelve el control al
       narrator_text
    """

    none = []
    all: Tool = [Rollback, Delegate, ScriptExecutor]