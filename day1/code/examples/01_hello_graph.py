"""
Example 1: The smallest possible graph
New idea: State, one Node, START and END

    START -> say_hello -> END

Run: python examples/01_hello_graph.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# State = the data shared inside the graph (here, only one field)
class State(TypedDict):
    message: str


# Node = a normal Python function
# It gets the state and returns the field it wants to update
def say_hello(state: State) -> dict:
    return {"message": "Hello from LangGraph!"}


# Build the graph
builder = StateGraph(State)              # 1. create a graph that uses our State
builder.add_node("say_hello", say_hello) # 2. add the node (name, function)
builder.add_edge(START, "say_hello")     # 3. START  -> say_hello
builder.add_edge("say_hello", END)       # 4. say_hello -> END

graph = builder.compile()                # 5. make it ready to run

# Run the graph with a starting state
result = graph.invoke({"message": ""})

print(result)  # {'message': 'Hello from LangGraph!'}
