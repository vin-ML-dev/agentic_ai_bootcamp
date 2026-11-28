"""
Day 2 - Prompt and tool description
"""

# Instructions for the model
SYSTEM_PROMPT = (
    "You are a customer support assistant. "
    "Read the ticket and propose a short note to add to it."
)

# A tool the model is allowed to ASK for.
# It would change a record, so today we only look at the request - we never run it.
ADD_TICKET_NOTE_TOOL = {
    "type": "function",
    "function": {
        "name": "add_ticket_note",
        "description": "Add a short note to a support ticket.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {"type": "string", "description": "Ticket ID, e.g. T-1001"},
                "note": {"type": "string", "description": "The note to add"},
            },
            "required": ["ticket_id", "note"],
        },
    },
}
