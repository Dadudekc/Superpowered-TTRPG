# arc_loader.py

import json

# Load arcs from arcs.json
with open("data\\arcs.json", "r") as file:
    ARCS_DATA = json.load(file)["arcs"]

def load_arc(arc_number: int):
    """
    Retrieves the arc data for the selected arc.
    Returns None if the arc does not exist.
    """
    for arc in ARCS_DATA:
        if arc["id"] == arc_number:
            return arc
    return None

def list_available_arcs():
    """
    Returns a formatted list of all available arcs.
    """
    return [f"{arc['id']}: {arc['name']} - {arc['description']}" for arc in ARCS_DATA]
