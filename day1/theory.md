# Day 1: Start Your Customer Support Agent Project

**What we learn today**
1. What an agent does
2. Our project: the Customer Support Agent and its practice support system
3. Python setup, GitHub account, and basic Git commands
4. Running a ready-made LangGraph workflow with fake ticket data

---

## Words You Will Hear in This Project

| Word | Simple meaning |
|---|---|
| **Customer support** | The team that helps customers when they have a problem with an order. |
| **Ticket** | A customer's complaint or question saved in the system, e.g. "Where is my order?" |
| **Ticket ID** | A unique number for each ticket, like `T-1001`, so we can find it easily. |
| **Order** | Something a customer bought from the shop. |
| **Order ID** | A unique number for each order, like `O-9001`. |
| **Delivery** | The journey of the order from the shop to the customer's home. |
| **Policy** | The shop's rules, e.g. "If delivery is more than 5 days late, escalate it." |
| **Record** | Any saved information in the system – a ticket, an order, or a delivery. |
| **Ticket note** | A short comment added to a ticket, e.g. "Checked order, it is shipped." |
| **Ticket status** | The current stage of a ticket, e.g. `open`, `in progress`, `resolved`, `closed`. |
| **Status change** | Moving a ticket from one stage to another, e.g. `open` → `resolved`. |
| **Escalation** | Passing a difficult ticket to a senior person or a human team. |
| **Reviewer** | The person who checks the agent's suggestion. |
| **Approve / Reject** | Reviewer says **yes** (do it) or **no** (don't do it). |
| **Synthetic data** | Fake data made for practice. It looks real but belongs to no real person. |

---

## 1. What Is an Agent?

Think of a **helper at a shop's customer care desk**.

A customer says: *"Where is my order?"*
The helper:
1. **Understands** the question
2. **Checks** the computer for the order
3. **Answers** the customer

An **AI agent** does the same thing, but as a program.

```
   ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
   │   1. UNDERSTAND  │ ──► │   2. USE TOOLS   │ ──► │   3. FINISH      │
   │   the request    │     │   to get facts   │     │   the task       │
   └──────────────────┘     └──────────────────┘     └──────────────────┘
   "Where is my order?"      Look up the order        "Your order arrives
                                                       tomorrow"
```

**What is a tool?**
A tool is just a **Python function** the agent can call, like `get_order_status("O-9001")`.

**Chatbot vs Agent**

| Chatbot | Agent |
|---|---|
| Only talks | Talks **and** does work |
| Answers from what it remembers | **Checks real records** using tools |
| "Orders usually take 5 days" | "Your order O-9001 was shipped today" |

---

## 2. Our Project: The Customer Support Agent

### In one line

> We are building a **smart support helper** that reads a customer's problem, checks the records, and **suggests** what to do. A **human** says yes or no before anything is changed.

We build **one project** and add a little more to it every day.

### What problems does it handle?

- 📦 **Order status** – "Where is my order?"
- 🚚 **Late delivery** – "My order is late"
- 🔁 **Follow-up** – "Any update on my old ticket?"

### The whole project in one picture

```
            ┌─────────────────────────────┐
            │   Customer sends a ticket   │
            │   "My order is late"        │
            └──────────────┬──────────────┘
                           ▼
            ┌─────────────────────────────┐
            │   Agent reads the ticket    │
            └──────────────┬──────────────┘
                           ▼
                ┌─────────────────────┐
                │ Is any information  │
                │ missing? (order ID) │
                └───┬─────────────┬───┘
                YES │             │ NO
                    ▼             ▼
   ┌────────────────────┐   ┌─────────────────────────────┐
   │ Ask the customer   │   │ Agent checks the records:   │
   │ for the missing    │   │ ticket, order, delivery,    │
   │ information        │   │ policy                      │
   └────────────────────┘   └──────────────┬──────────────┘
                                           ▼
                            ┌─────────────────────────────┐
                            │ Agent SUGGESTS an action:   │
                            │ • add a ticket note         │
                            │ • change ticket status      │
                            │ • escalate (send to human)  │
                            └──────────────┬──────────────┘
                                           ▼
                            ┌─────────────────────────────┐
                            │ Human reviewer checks it    │
                            └───────┬───────────────┬─────┘
                            APPROVE │               │ REJECT
                                    ▼               ▼
                   ┌─────────────────────┐   ┌──────────────────┐
                   │ Record is updated   │   │ Nothing changes  │
                   │ and checked         │   │                  │
                   └─────────────────────┘   └──────────────────┘
```

> 🔑 **Golden rule:** The agent only **suggests**. A **human approves** before any record is changed.

### The Practice Support System (Sandbox)

We will **never** use real customers' data. Instead we use a **practice system** – like a **flight simulator** for pilots. You can practice safely without real risk.

It has:
- **Fake tickets and orders** – safe to use and share
- **Approved ways to update records** – the only allowed doors for changes
- **Audit records** – a diary of every change made
- **Planned errors** – so we can practice fixing problems

```
   ┌──────────────┐   asks for data    ┌───────────────────────────┐
   │              │ ─────────────────► │  Practice Support System  │
   │    Agent     │                    │  (fake tickets & orders)  │
   │              │ ◄───────────────── │                           │
   └──────────────┘   sends back facts └───────────────────────────┘
```

We start this practice system on **Day 4**. Today we only use a small file of fake tickets.

---

## 3. Python Setup, GitHub, and Git

### Python setup

```bash
python --version                  # check Python is installed (3.10 or newer)
python -m venv .venv              # create a virtual environment
source .venv/bin/activate         # turn it on (Windows: .venv\Scripts\activate)
pip install -r requirements.txt   # install the packages we need
```

**What is a virtual environment?**
A separate box for this project's packages, so they don't mix with other projects.

### What are Git and GitHub?

- **Git** = a tool on your computer that saves every version of your code, so you can go back anytime.
- **GitHub** = a website that stores your Git code online, so you can share it and never lose it.

> **Git** saves your code. **GitHub** keeps it online.

### Create a GitHub account

1. Go to **github.com** and sign up
2. Click **New repository**, name it `customer-support-agent`
3. You will upload your work here **at the end of every day**

### How Git saves your work

```
   ┌─────────────┐   git add   ┌─────────────┐  git commit  ┌─────────────┐  git push  ┌─────────────┐
   │ Your files  │ ──────────► │  Selected   │ ───────────► │  Saved on   │ ─────────► │  Saved on   │
   │ (changed)   │             │  files      │              │  your PC    │            │  GitHub     │
   └─────────────┘             └─────────────┘              └─────────────┘            └─────────────┘
```

### Basic Git commands

| Command | What it does |
|---|---|
| `git init` | Start using Git in this folder |
| `git status` | Show which files changed |
| `git add .` | Pick all changed files to save |
| `git commit -m "message"` | Save a snapshot with a short note |
| `git remote add origin <url>` | Connect your folder to GitHub |
| `git push -u origin main` | Upload your saved work to GitHub |

### Keep secrets out of GitHub 🔒

Passwords and API keys must **never** go online.

| File | What's inside | Upload to GitHub? |
|---|---|---|
| `.env` | Your **real** keys | ❌ Never |
| `.env.example` | **Fake** example values | ✅ Yes |
| `.gitignore` | List of files Git should ignore (like `.env`) | ✅ Yes |

---

## 4. Running a LangGraph Workflow

### What is LangGraph?

**LangGraph** helps us build an agent as a **flowchart of steps**.

Each box is a step. Arrows show which step runs next.

### 4 words to know

| Word | Simple meaning | In our project |
|---|---|---|
| **State** | A notebook shared by all steps | ticket ID, ticket, next step |
| **Node** | One step (a Python function) | `read_ticket`, `propose_next_step` |
| **Edge** | An arrow from one step to the next | `read_ticket → propose_next_step` |
| **START / END** | Where it begins and stops | — |

### Our starter graph

```
   ┌─────────┐     ┌───────────────┐     ┌─────────────────────┐     ┌───────┐
   │  START  │ ──► │  read_ticket  │ ──► │  propose_next_step  │ ──► │  END  │
   └─────────┘     └───────────────┘     └─────────────────────┘     └───────┘
                    Opens the ticket       Decides what to do
                    from the file          next
```

### How the State (notebook) fills up

```
   At START                 After read_ticket           After propose_next_step
   ┌──────────────────┐     ┌──────────────────┐        ┌──────────────────────────┐
   │ ticket_id: T-1001│     │ ticket_id: T-1001│        │ ticket_id: T-1001        │
   │ ticket:    ?     │ ──► │ ticket:   {...}  │ ─────► │ ticket:   {...}          │
   │ next_step: ?     │     │ next_step: ?     │        │ next_step: "Look up the  │
   └──────────────────┘     └──────────────────┘        │            order status" │
                                                        └──────────────────────────┘
```

### How `propose_next_step` decides

```
                    ┌──────────────────────┐
                    │  Is order ID empty?  │── YES ──► Ask the customer for their order ID
                    └──────────┬───────────┘
                               │ NO
                               ▼
                    ┌──────────────────────┐
                    │ Says "late"/"delay"? │── YES ──► Check delivery & policy, suggest escalation
                    └──────────┬───────────┘
                               │ NO
                               ▼
                    ┌──────────────────────┐
                    │Says "follow"/"update"│── YES ──► Check old notes, suggest a ticket note
                    └──────────┬───────────┘
                               │ NO
                               ▼
                    ┌──────────────────────┐
                    │Says "status"/"where"?│── YES ──► Look up the order status
                    └──────────┬───────────┘
                               │ NO
                               ▼
                    Send to a human support agent
```

Today this uses **simple rules** (keywords). From **Day 2**, an AI model will help make this decision.

### Our fake tickets

| Ticket | Customer says | Agent suggests |
|---|---|---|
| T-1001 | What is the status of my order? | Look up the order status |
| T-1002 | My delivery is late | Check delivery & policy, suggest escalation |
| T-1003 | Any update? I am following up | Check old notes, suggest a ticket note |
| T-1004 | Where is my order? *(no order ID)* | Ask the customer for their order ID |

---

## Hands-on

1. Create the project folder and virtual environment
2. Install packages: `pip install -r requirements.txt`
3. Make your settings file: `cp .env.example .env`
4. Run the graph on one ticket:
   ```bash
   python graph.py T-1001
   ```
5. Open `outputs/next_step.json` and see the saved next step
6. Try the other tickets: `T-1002`, `T-1003`, `T-1004`

---

## Git: Commit and Push

Upload the starter graph, fake ticket data, README, packages list, and example settings file — **no real keys**.

```bash
git init
git add graph.py data/ README.md requirements.txt .env.example .gitignore
git status                        # check that .env is NOT in the list
git commit -m "Day 1: starter graph and sample tickets"
git branch -M main
git remote add origin https://github.com/<your-username>/customer-support-agent.git
git push -u origin main
```

---

## Quick Recap

- An agent **understands → uses tools → finishes the task**
- Our agent **suggests** support actions; a **human approves** changes
- We practice on a **fake support system**, never real customers
- LangGraph = **State** (notebook) + **Nodes** (steps) + **Edges** (arrows)
- Save and upload your work every day; **never** upload `.env`
