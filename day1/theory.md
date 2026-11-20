# Day 1: Start Your Customer Support Agent Project

**Today's topics**
1. What an agent does
2. The Customer Support Agent and its practice support system
3. Python setup, GitHub account creation, and basic Git commands
4. Running a supplied LangGraph workflow with synthetic ticket data

---

## 1. What an Agent Does

An **agent** is a program that does three things:

| Step | Meaning | Support example |
|---|---|---|
| **Interpret a request** | Understand what the user wants | "Where is my order O-9001?" → customer wants order status |
| **Use tools** | Call functions to get facts or do work | Look up order O-9001 in the support system |
| **Complete a task** | Give a final answer or result | "Your order is shipped and arrives tomorrow" |

**Chatbot vs Agent**

- A **chatbot** only replies with text from what it already knows.
- An **agent** can **check real records** using tools and then act on the result.

> Simple way to remember: **Understand → Use tools → Finish the task**

---

## 2. Our Project: The Customer Support Agent

We build **one project** for the whole course and add to it every day.

**The agent handles:**
- Order-status questions
- Delayed deliveries
- Ticket follow-ups

**What the agent does:**
1. Checks **ticket, order, delivery, and policy** records
2. **Asks for missing information** (for example, no order ID)
3. **Proposes** one of these:
   - a ticket note
   - a status change
   - an escalation
4. A **human reviewer approves** the change before it is made

> Important: the agent only **proposes**. A human **approves** before any record is changed.

### The Practice Support System (Sandbox)

We do **not** use real customer accounts. We use a **practice support system** that has:
- **Synthetic (fake) tickets and orders** – safe to use and share
- Approved update endpoints – the only allowed ways to change records
- Audit records – a history of every change
- Controlled failure examples – to practice handling errors

We will run this practice backend on **Day 4**. Today we only use sample ticket data.

---

## 3. Python Setup, GitHub, and Basic Git

### Python setup

```bash
python --version                  # check Python is installed (3.10+)
python -m venv .venv              # create a virtual environment
source .venv/bin/activate         # activate it (Windows: .venv\Scripts\activate)
pip install -r requirements.txt   # install packages
```

A **virtual environment** keeps this project's packages separate from other projects.

### GitHub account

1. Go to **github.com** and sign up
2. Create a new repository named `customer-support-agent`
3. We push our work to this repository **at the end of every class**

### Basic Git commands

| Command | What it does |
|---|---|
| `git init` | Start tracking a folder with Git |
| `git status` | See which files changed |
| `git add .` | Select all changed files for the next commit |
| `git commit -m "message"` | Save a snapshot with a message |
| `git remote add origin <url>` | Link the folder to your GitHub repository |
| `git push -u origin main` | Upload your commits to GitHub |

### Keep secrets out of Git

- Real keys and passwords go in **`.env`** → this file is **never** committed
- **`.env.example`** shows the setting names with fake values → this file **is** committed
- **`.gitignore`** tells Git to ignore `.env`

---

## 4. Running a Supplied LangGraph Workflow

**LangGraph** lets us build an agent as a **graph**: a set of steps connected by arrows.

| Word | Meaning |
|---|---|
| **State** | The information shared between steps (ticket ID, ticket, next step) |
| **Node** | One step – a normal Python function |
| **Edge** | An arrow saying which step runs next |
| **START / END** | Where the graph begins and finishes |

**Our starter graph:**

```
START → read_ticket → propose_next_step → END
```

- `read_ticket` – loads the ticket from `data/sample_tickets.json`
- `propose_next_step` – decides what the agent should do next
- The result is saved to `outputs/next_step.json`

Today the decision uses simple rules. On **Day 2** we add an AI model, and on **Day 5** we build graphs ourselves in detail.

**Sample tickets and their proposed next step:**

| Ticket | Message | Proposed next step |
|---|---|---|
| T-1001 | What is the status of my order? | Look up the order status |
| T-1002 | My delivery is late | Check delivery and delay policy, propose escalation |
| T-1003 | Following up on my ticket | Check previous notes, propose a ticket note |
| T-1004 | Where is my order? (no order ID) | Ask the customer for their order ID |

---

## Hands-on

1. Create the project folder and virtual environment
2. Install packages: `pip install -r requirements.txt`
3. Copy settings: `cp .env.example .env`
4. Run the graph on a sample ticket:
   ```bash
   python graph.py T-1001
   ```
5. Open `outputs/next_step.json` and check the saved next step
6. Run it again with `T-1002`, `T-1003`, and `T-1004`

---

## Git: Commit and Push

Commit the starter graph, synthetic sample data, README, dependencies, and example environment file — **without credentials**.

```bash
git init
git add graph.py data/ README.md requirements.txt .env.example .gitignore
git status                        # make sure .env is NOT listed
git commit -m "Day 1: starter graph and sample tickets"
git branch -M main
git remote add origin https://github.com/<your-username>/customer-support-agent.git
git push -u origin main
```

---

## Quick Recap

- An agent **interprets a request, uses tools, and completes a task**
- Our agent **proposes** support actions; a **human approves** record changes
- We use a **practice support system** with fake data, never real customers
- A LangGraph graph is made of **state, nodes, and edges**
- Every class ends with a **commit and push**, and `.env` is **never** committed
