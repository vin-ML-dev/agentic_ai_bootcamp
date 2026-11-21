# Customer Support Agent

An AI agent that investigates a support ticket, proposes a resolution, and (later in the course) carries out an approved update.

**Day 1 status:** A starter LangGraph workflow reads a sample ticket and saves a proposed next step.

## Project files

```
customer-support-agent/
├── examples/                # 4 small programs to learn LangGraph step by step
├── graph.py                 # starter LangGraph workflow
├── data/sample_tickets.json # synthetic (fake) ticket data
├── requirements.txt         # Python packages
├── .env.example             # example settings, no real credentials
├── .gitignore               # keeps .env and secrets out of Git
└── README.md
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install packages
pip install -r requirements.txt

# 3. Create your own settings file (never commit .env)
cp .env.example .env             # Windows: copy .env.example .env
```

## Learn LangGraph first (examples)

Run these in order. Each one adds one new idea.

```bash
python examples/01_hello_graph.py      # State, one node, START and END
python examples/02_two_nodes.py        # two nodes, passing data
python examples/03_decide_in_node.py   # if/else decision inside a node
python examples/04_ticket_from_file.py # read a ticket file, save the result
```

## Run

```bash
python graph.py T-1001
```

Output:

```
Read ticket T-1001: Hi, what is the status of my order O-9001?
Proposed next step: Look up the order status
Saved to outputs/next_step.json
```

Try the other sample tickets: `T-1002`, `T-1003`, `T-1004`.

## Graph

```
START -> read_ticket -> propose_next_step -> END
```
