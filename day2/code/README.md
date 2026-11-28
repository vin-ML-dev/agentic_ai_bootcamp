# Customer Support Agent

An AI agent that investigates a support ticket, proposes a resolution, and (later in the course) carries out an approved update.

**Day 2 status:** The agent calls an AI model. For the same ticket, we compare an ordinary text answer with a tool call request. The tool call is only printed, never executed.

## Project files

```
customer-support-agent/
├── graph.py                 # Day 1: starter LangGraph workflow
├── model_client.py          # Day 2: course API client
├── prompts.py               # Day 2: system prompt and tool description
├── compare_responses.py     # Day 2: ordinary response vs tool call
├── data/sample_tickets.json # synthetic (fake) ticket data
├── requirements.txt         # Python packages
├── .env.example             # example settings, no real credentials
├── .gitignore               # keeps .env and secrets out of Git
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
```

Open `.env` and fill in `MODEL_API_KEY`, `MODEL_BASE_URL` and `MODEL_NAME`.

## Run

```bash
python compare_responses.py
```

Example output:

```
Ticket: Hi, what is the status of my order O-9001?

--- 1. Ordinary response ---
Your order is probably on its way.
Tokens used: 80

--- 2. Tool call request ---
Tool:      add_ticket_note
Arguments: {'ticket_id': 'T-1001', 'note': 'Customer asked for status of order O-9001.'}
Tokens used: 80

This is only a PROPOSED action. It was NOT executed.
Saved to outputs/comparison.json
```
