"""
Example 2: Two nodes connected one after another
New idea: a node can READ what the previous node wrote

    START -> add_name -> add_greeting -> END

Run: python examples/02_two_nodes.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    message: str


# Node 1: changes the name to capital letters
def add_name(state: State) -> dict:
    print("Running add_name")
    return {"name": state["name"].upper()}


# Node 2: reads the name that Node 1 changed
def add_greeting(state: State) -> dict:
    print("Running add_greeting")
    return {"message": f"Hello, {state['name']}!"}


builder = StateGraph(State)
builder.add_node("add_name", add_name)
builder.add_node("add_greeting", add_greeting)

builder.add_edge(START, "add_name")
builder.add_edge("add_name", "add_greeting")   # add_name runs first, then add_greeting
builder.add_edge("add_greeting", END)

graph = builder.compile()

# We only give "name" at the start. "message" is filled by the graph.
result = graph.invoke({"name": "john"})

print(result)  
