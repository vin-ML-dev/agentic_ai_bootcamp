"""
Example 4: Read a ticket from a file and save the result
New ideas:
    - a node reads data from a JSON file
    - the state can hold a whole dictionary (the ticket)
    - save the final result to a file

    START -> load_ticket -> suggest_step -> END

This is almost the same as the Day 1 graph.py!

Run (from the project folder): python examples/04_ticket_from_file.py
"""

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    ticket_id: str   # given by us at the start
    ticket: dict     # filled by load_ticket
    next_step: str   # filled by suggest_step


# Node 1: find the ticket in the JSON file
def load_ticket(state: State) -> dict:
    tickets = json.loads(Path("../data/sample_tickets.json").read_text())  # list of dicts

    for ticket in tickets:
        if ticket["ticket_id"] == state["ticket_id"]:
            return {"ticket": ticket}

    raise ValueError("Ticket not found")


# Node 2: suggest a next step from the ticket details
def suggest_step(state: State) -> dict:
    ticket = state["ticket"]

    if ticket["order_id"] is None:
        return {"next_step": "Ask the customer for their order ID"}
    return {"next_step": f"Look up order {ticket['order_id']}"}


builder = StateGraph(State)
builder.add_node("load_ticket", load_ticket)
builder.add_node("suggest_step", suggest_step)

builder.add_edge(START, "load_ticket")
builder.add_edge("load_ticket", "suggest_step")
builder.add_edge("suggest_step", END)

graph = builder.compile()

result = graph.invoke({"ticket_id": "T-1004"})
print("Next step:", result["next_step"])

# Save only the useful part of the result
Path("outputs").mkdir(exist_ok=True)                        # create folder if missing
output = {"ticket_id": result["ticket_id"], "next_step": result["next_step"]}
Path("outputs/example_result.json").write_text(json.dumps(output, indent=2))
print("Saved to outputs/example_result.json")
