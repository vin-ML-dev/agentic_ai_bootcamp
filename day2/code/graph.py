"""
Day 1 - Starter LangGraph workflow for the Customer Support Agent.

What it does:
    1. read_ticket        -> loads one sample ticket
    2. propose_next_step  -> decides what the agent should do next
    3. saves the proposed next step to outputs/next_step.json

No AI model is used yet (we add the model on Day 2).
Nothing is changed in any record - we only PROPOSE a next step.

Run:
    python graph.py T-1001
"""

import json
import sys
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ---------------------------------------------------------------------------
# 1. State: the information shared between the steps (nodes) of the graph
# ---------------------------------------------------------------------------
class TicketState(TypedDict):
    ticket_id: str
    ticket: dict
    next_step: str


# ---------------------------------------------------------------------------
# 2. Nodes: each node is a normal Python function
#    It receives the state and returns the fields it wants to update
# ---------------------------------------------------------------------------
def read_ticket(state: TicketState) -> dict:
    tickets = json.loads(Path("data/sample_tickets.json").read_text())

    for ticket in tickets:
        if ticket["ticket_id"] == state["ticket_id"]:
            print(f"Read ticket {ticket['ticket_id']}: {ticket['message']}")
            return {"ticket": ticket}

    raise ValueError(f"Ticket {state['ticket_id']} not found")


def propose_next_step(state: TicketState) -> dict:
    ticket = state["ticket"]
    message = ticket["message"].lower()

    if not ticket["order_id"]:
        next_step = "Ask the customer for their order ID"
    elif "late" in message or "delay" in message:
        next_step = "Check delivery record and delay policy, then propose escalation"
    elif "follow" in message or "update" in message:
        next_step = "Check previous ticket notes, then propose a ticket note"
    elif "status" in message or "where" in message:
        next_step = "Look up the order status"
    else:
        next_step = "Escalate to a human support agent"

    print(f"Proposed next step: {next_step}")
    return {"next_step": next_step}


# ---------------------------------------------------------------------------
# 3. Build the graph: START -> read_ticket -> propose_next_step -> END
# ---------------------------------------------------------------------------
builder = StateGraph(TicketState)

builder.add_node("read_ticket", read_ticket)
builder.add_node("propose_next_step", propose_next_step)

builder.add_edge(START, "read_ticket")
builder.add_edge("read_ticket", "propose_next_step")
builder.add_edge("propose_next_step", END)

graph = builder.compile()


# ---------------------------------------------------------------------------
# 4. Run the graph on one sample ticket and save the proposed next step
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ticket_id = sys.argv[1] if len(sys.argv) > 1 else "T-1001"

    result = graph.invoke({"ticket_id": ticket_id})

    output = {"ticket_id": ticket_id, "next_step": result["next_step"]}
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/next_step.json").write_text(json.dumps(output, indent=2))

    print("Saved to outputs/next_step.json")
