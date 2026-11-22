"""
A simple LangGraph agent, explained step by step.

What this agent does:
  - Chats with you.
  - Can use one tool: a (fake) weather lookup.
  - Remembers the conversation across turns (memory).

Setup (run once in your terminal):
    pip install -U langgraph langchain langchain-openai python-dotenv

    Then create a file named .env in the SAME folder as this script, containing:
        OPENAI_API_KEY=sk-your-key-here
    (No quotes, no spaces around '='. Never share or upload this file.)

Run:
    python simple_langgraph_agent.py
"""

# ---------------------------------------------------------------------------
# STEP 0: Load the API key and imports
# ---------------------------------------------------------------------------
# load_dotenv() reads the .env file and puts OPENAI_API_KEY into the environment.
# The OpenAI library then finds the key automatically — no need to pass it in code.
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("OPENAI_API_KEY not found. Create a .env file next to this script "
                     "with the line:  OPENAI_API_KEY=sk-your-key-here")

from langchain.chat_models import init_chat_model   # one helper to load any LLM
from langchain_core.tools import tool                # decorator to turn a function into a tool

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver


# ---------------------------------------------------------------------------
# STEP 1: Define the TOOL (the agent's "hands")
# ---------------------------------------------------------------------------
# A tool is just a normal Python function with the @tool decorator.
# IMPORTANT: the docstring is what the LLM reads to decide WHEN to use the tool,
# so describe clearly what it does and what input it needs.

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Fake data to keep the example simple. In a real agent, call a weather API here.
    fake_weather = {
        "delhi": "28°C, hazy",
        "mumbai": "31°C, humid",
        "bangalore": "24°C, pleasant",
    }
    return fake_weather.get(city.lower(), f"Sorry, no weather data for {city}.")


tools = [get_weather]


# ---------------------------------------------------------------------------
# STEP 2: Load the LLM (the agent's "brain") and give it the tool
# ---------------------------------------------------------------------------
# init_chat_model works with many providers. "openai:" means use OpenAI;
# the part after it is the model name (any model from OpenAI's models page works).
llm = init_chat_model("openai:gpt-4o-mini")

# bind_tools tells the LLM: "this tool exists, you may ask to call it".
# The LLM does NOT run the tool itself — it only replies with "please call get_weather('Delhi')".
llm_with_tools = llm.bind_tools(tools)


# ---------------------------------------------------------------------------
# STEP 3: Define the STATE (the shared notebook)
# ---------------------------------------------------------------------------
# MessagesState is a ready-made state with one field: "messages" (a list).
# Every node reads this list and ADDS new messages to it (it appends, not overwrites).


# ---------------------------------------------------------------------------
# STEP 4: Define the NODES (the workers)
# ---------------------------------------------------------------------------
# A node is a function: it receives the current state and returns an UPDATE to it.

def agent_node(state: MessagesState):
    """The 'thinking' step: send the conversation to the LLM and get its reply."""
    response = llm_with_tools.invoke(state["messages"])
    # The reply is either a normal answer OR a request to call get_weather.
    return {"messages": [response]}

# The 'acting' step: ToolNode is prebuilt. It looks at the LLM's last message,
# runs get_weather if the LLM asked for it, and adds the result to the state.
tool_node = ToolNode(tools)


# ---------------------------------------------------------------------------
# STEP 5: Build the GRAPH (connect nodes with edges)
# ---------------------------------------------------------------------------
builder = StateGraph(MessagesState)

# 5a. Add the nodes, each with a name.
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# 5b. Normal edge: the graph always starts at the agent.
builder.add_edge(START, "agent")

# 5c. Conditional edge: after the agent speaks, decide where to go.
#     tools_condition is prebuilt and checks the LLM's last message:
#       - LLM asked for get_weather -> go to "tools"
#       - LLM gave a final answer   -> go to END
builder.add_conditional_edges("agent", tools_condition)

# 5d. Normal edge: after the tool runs, go BACK to the agent so it can
#     read the weather result and write the final answer. This is the LOOP:
#
#        START -> agent -> (needs weather?) --yes--> tools --+
#                   ^                                        |
#                   +----------------------------------------+
#                   |
#                   +--no--> END
builder.add_edge("tools", "agent")


# ---------------------------------------------------------------------------
# STEP 6: Add MEMORY and COMPILE
# ---------------------------------------------------------------------------
# A checkpointer saves the state after every step, so the agent remembers
# earlier messages. MemorySaver keeps it in RAM (lost when the program stops).
memory = MemorySaver()

# compile() turns the blueprint into a runnable app.
app = builder.compile(checkpointer=memory)


# ---------------------------------------------------------------------------
# STEP 7: RUN the agent
# ---------------------------------------------------------------------------
# thread_id = a conversation ID. Same thread_id = the agent remembers earlier turns.
config = {"configurable": {"thread_id": "chat-1"}}

if __name__ == "__main__":
    print("Weather agent. Type 'quit' to exit.")
    print("Try: 'Weather in Delhi?'  then  'And Mumbai?'\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit", "q"}:
            break
        if not user_input:
            continue

        # .invoke()              -> runs everything, returns ONLY the final result at the end.
        # .stream()              -> returns output after EACH step, while the agent is working,
        #                            so you can see what the agent is doing.
        # stream_mode="values"    -> each step gives the FULL list of messages so far.
        # step["messages"][-1]    -> the newest message (the step that just happened).
        for step in app.stream(
            {"messages": [("user", user_input)]},
            config,
            stream_mode="values",
        ):
            step["messages"][-1].pretty_print()
        print()