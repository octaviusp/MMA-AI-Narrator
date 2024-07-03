import sys
import os

# Get the absolute directory path where the script resides
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
# Calculate the parent directory path
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)

from core.graph.compiled import graph_compiled
from langchain_core.runnables.graph import NodeColors

# Define custom node colors
neon_node_colors = NodeColors(
    start="#39ff14",  # Neon green
    end="#ff073a",    # Neon red
    other="#00ffff"   # Neon cyan
)

# Intentar generar y guardar la imagen del grafo
try:
    # Obtener la imagen del grafo en formato PNG
    graph_image = graph_compiled.get_graph(xray=True).draw_mermaid_png(
        node_colors=neon_node_colors,
        background_color="white",  # Black background
        padding=40
    )

    # Guardar la imagen en un archivo
    with open("./architecture/graph_visualization.png", "wb") as f:
        f.write(graph_image)
    print("Graph image saved as 'graph_visualization.png'.")
except Exception as e:
    print("Failed to generate or save the graph image:", e)

