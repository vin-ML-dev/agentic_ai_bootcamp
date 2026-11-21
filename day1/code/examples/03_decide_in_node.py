"""
Example 3: A node that makes a decision with if / else
New ideas:
    - a node returns ONLY the field it changes (other fields stay safe)
    - simple keyword rules to decide a next step

    START -> read_message -> decide_reply -> END

Run: python examples/03_decide_in_node.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str    # what the customer wrote
    cleaned: str    # message in small letters
    reply: str      # what we decide to do


# Node 1: clean the message
def read_message(state: State) -> dict:
    return {"cleaned": state["message"].lower()}   # only updates "cleaned"


# Node 2: decide the reply using keywords
def decide_reply(state: State) -> dict:
    text = state["cleaned"]

    if "late" in text:
        reply = "Sorry for the delay, we will check your delivery"
    elif "where" in text:
        reply = "Let me look up your order"
    else:
        reply = "Passing your message to our team"

    return {"reply": reply}                         # only updates "reply"


builder = StateGraph(State)
builder.add_node("read_message", read_message)
builder.add_node("decide_reply", decide_reply)

builder.add_edge(START, "read_message")
builder.add_edge("read_message", "decide_reply")
builder.add_edge("decide_reply", END)

graph = builder.compile()

# Run the SAME graph with different messages
for msg in ["Where is my ORDER?", "My parcel is LATE", "I want a new phone"]:
    result = graph.invoke({"message": msg})
    print(f"{msg:22} -> {result['reply']}")
