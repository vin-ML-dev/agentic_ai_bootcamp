"""
Day 2 - Ordinary response vs Tool call request

Same ticket, asked two ways:
    1. Without tools -> the model replies with normal text
    2. With a tool   -> the model replies with a tool call (tool name + arguments)

We only PRINT the tool call. We do NOT run it, so no record is changed.

Run: python compare_responses.py
"""

import json
from pathlib import Path

from model_client import ask_model, ask_model_with_tools
from prompts import SYSTEM_PROMPT, ADD_TICKET_NOTE_TOOL

TICKET_ID = "T-1001"

# 1. Find the ticket in our sample data
tickets = json.loads(Path("data/sample_tickets.json").read_text())
for ticket in tickets:
    if ticket["ticket_id"] == TICKET_ID:
        break

print("Ticket:", ticket["message"])

# 2. Messages: system = instructions, user = the ticket
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Ticket {TICKET_ID}: {ticket['message']}"},
]

# 3. Ordinary response
response = ask_model(messages)
text_reply = response.choices[0].message.content

print("\n--- 1. Ordinary response ---")
print(text_reply)
print("Tokens used:", response.usage.total_tokens)

# 4. Tool call request (same messages + the tool)
response = ask_model_with_tools(messages, [ADD_TICKET_NOTE_TOOL])
tool_call = response.choices[0].message.tool_calls[0]

tool_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)  # JSON text -> Python dict

print("\n--- 2. Tool call request ---")
print("Tool:     ", tool_name)
print("Arguments:", arguments)
print("Tokens used:", response.usage.total_tokens)
print("\nThis is only a PROPOSED action. It was NOT executed.")

# 5. Save the comparison
comparison = {
    "ticket_id": TICKET_ID,
    "ordinary_response": text_reply,
    "tool_call": {"tool": tool_name, "arguments": arguments},
    "executed": False,
}
Path("outputs").mkdir(exist_ok=True)
Path("outputs/comparison.json").write_text(json.dumps(comparison, indent=2))
print("Saved to outputs/comparison.json")
