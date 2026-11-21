# LangGraph Basics

## What is LangGraph?

- **LangGraph** is a Python library for building **agents** as a **graph** (a flowchart of steps).
- Each **box** in the flowchart is a step.
- Each **arrow** shows which step runs next.
- All steps share one **notebook** of data, called the **State**.

> LangGraph = **steps** (nodes) + **arrows** (edges) + **shared data** (state)

---

## Why use LangGraph?

- An agent does work in **many steps**: read the request → check records → decide → reply.
- LangGraph lets us write each step as a **small Python function**.
- It lets us **see the whole flow clearly**, like a flowchart.
- It **passes data** between steps for us automatically.

---

## The Big Picture

```
                         ┌───────────────────────────────┐
                         │            STATE              │
                         │   (shared notebook of data)   │
                         │   ticket_id, ticket, next_step│
                         └───────▲──────────────▲────────┘
                     reads &     │              │     reads &
                     updates     │              │     updates
                                 │              │
   ┌─────────┐  edge   ┌─────────┴───┐  edge  ┌─┴───────────┐  edge   ┌───────┐
   │  START  │ ──────► │   NODE 1    │ ─────► │   NODE 2    │ ──────► │  END  │
   └─────────┘         │ (function)  │        │ (function)  │         └───────┘
                       └─────────────┘        └─────────────┘
```

- **START** → where the graph begins
- **Nodes** → do the work, one after another
- **Edges** → decide the order
- **State** → every node can read it and update it
- **END** → where the graph stops

---

## Key Terms

### 1. State

- The **data shared** by all steps in the graph.
- Like a **notebook** passed from one person to the next.
- We define it as a `TypedDict` (a dictionary with fixed field names).

```python
from typing import TypedDict

class State(TypedDict):
    ticket_id: str
    next_step: str
```

### 2. Node

- **One step** of work.
- It is just a **normal Python function**.
- It **gets** the state and **returns** only the fields it wants to change.

```python
def propose_next_step(state: State) -> dict:
    return {"next_step": "Look up the order status"}
```

### 3. Edge

- An **arrow** from one node to another.
- It tells LangGraph: *"after this node, run that node."*

```python
builder.add_edge("read_ticket", "propose_next_step")
```

| Edge type | Meaning | When we learn it |
|---|---|---|
| **Normal edge** | Always go to the same next node | Today |
| **Conditional edge** | Choose the next node based on the state | Later in the course |

### 4. START and END

- **START** → a special point where the graph **begins**.
- **END** → a special point where the graph **stops**.

```python
from langgraph.graph import START, END

builder.add_edge(START, "read_ticket")
builder.add_edge("propose_next_step", END)
```

### 5. StateGraph (the builder)

- The object we use to **build** the graph.
- We tell it which **State** to use, then add nodes and edges.

```python
from langgraph.graph import StateGraph

builder = StateGraph(State)
builder.add_node("read_ticket", read_ticket)
```

### 6. Compile

- Turns our plan into a **graph that can run**.
- LangGraph also **checks** for mistakes here (for example, an edge to a node that doesn't exist).

```python
graph = builder.compile()
```

### 7. Invoke

- **Runs** the graph.
- We give it the **starting state**, and it gives back the **final state**.

```python
result = graph.invoke({"ticket_id": "T-1001"})
print(result["next_step"])
```

---

## How the State Changes Step by Step

When a node returns a field, LangGraph **updates only that field**. The other fields stay the same.

```
   invoke({"ticket_id": "T-1001"})
                │
                ▼
   ┌──────────────────────────┐
   │ ticket_id: T-1001        │
   │ ticket:    (empty)       │
   │ next_step: (empty)       │
   └────────────┬─────────────┘
                ▼
        ┌───────────────┐
        │  read_ticket  │  returns {"ticket": {...}}
        └───────┬───────┘
                ▼
   ┌──────────────────────────┐
   │ ticket_id: T-1001        │
   │ ticket:    {...}   ◄─ new│
   │ next_step: (empty)       │
   └────────────┬─────────────┘
                ▼
     ┌─────────────────────┐
     │  propose_next_step  │  returns {"next_step": "..."}
     └──────────┬──────────┘
                ▼
   ┌──────────────────────────┐
   │ ticket_id: T-1001        │
   │ ticket:    {...}         │
   │ next_step: "Look up  ◄─ new
   │   the order status"      │
   └────────────┬─────────────┘
                ▼
        result (final state)
```

---

## How to Build Any Graph: 5 Steps

```
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │ 1. Define State  │──►│ 2. Write Nodes   │──►│ 3. Add Nodes &   │──►│ 4. Compile       │──►│ 5. Invoke        │
   │   (TypedDict)    │   │  (functions)     │   │    Edges         │   │                  │   │   (run it)       │
   └──────────────────┘   └──────────────────┘   └──────────────────┘   └──────────────────┘   └──────────────────┘
```

### Full example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define State
class State(TypedDict):
    message: str

# 2. Write Nodes
def say_hello(state: State) -> dict:
    return {"message": "Hello from LangGraph!"}

# 3. Add Nodes & Edges
builder = StateGraph(State)
builder.add_node("say_hello", say_hello)
builder.add_edge(START, "say_hello")
builder.add_edge("say_hello", END)

# 4. Compile
graph = builder.compile()

# 5. Invoke
result = graph.invoke({"message": ""})
print(result)   # {'message': 'Hello from LangGraph!'}
```

---

## Quick Summary

| Term | Simple meaning | Code |
|---|---|---|
| **State** | Shared notebook of data | `class State(TypedDict)` |
| **Node** | One step (a function) | `builder.add_node("name", func)` |
| **Edge** | Arrow to the next step | `builder.add_edge("a", "b")` |
| **START / END** | Begin / stop points | `START`, `END` |
| **StateGraph** | The graph builder | `StateGraph(State)` |
| **Compile** | Make the graph ready to run | `builder.compile()` |
| **Invoke** | Run the graph | `graph.invoke({...})` |

> Remember: **Define State → Write Nodes → Connect with Edges → Compile → Invoke**
