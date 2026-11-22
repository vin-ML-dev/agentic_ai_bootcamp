"""
Example 1: The smallest possible graph
New idea: State, one Node, START and END

    START -> say_hello -> END

Run: python examples/01_hello_graph.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# State = the data shared inside the graph
class State(TypedDict):
    message: str


# Node = a normal Python function
def say_hello(state: State) -> dict:
    # Use the user's message if provided; otherwise use the default
    user_message = state.get("message", "").strip()

    if user_message:
        return {"message": user_message}

    return {"message": "Hello from LangGraph!"}


# Build the graph
builder = StateGraph(State)

builder.add_node("say_hello", say_hello)
builder.add_edge(START, "say_hello")
builder.add_edge("say_hello", END)

graph = builder.compile()


# Get input from the user
user_input = input("Enter your message: ")

# Run the graph
result = graph.invoke({"message": user_input})

print("\nOutput:", result["message"])
