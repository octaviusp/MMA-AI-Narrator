from langgraph.prebuilt import ToolNode

from core.runnables.tools.tool_factory import ToolFactory

tools_node_run = ToolNode(ToolFactory.all)