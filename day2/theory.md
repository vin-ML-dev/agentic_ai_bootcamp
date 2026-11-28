# Day 2: LLM Basics for Agents

**What we learn today**
1. Messages, tokens, context limits, and generation settings
2. Calling an instruction-following model through the course API client
3. Structured responses and model-requested tool calls
4. Proposed action vs executed action

---

## Words You Will Hear Today

| Word | Simple meaning |
|---|---|
| **LLM** | Large Language Model. An AI that reads text and writes text, like ChatGPT or Claude. |
| **Model** | Short name for the LLM we use. |
| **Prompt** | The text we send to the model. |
| **Response** | The text (or data) the model sends back. |
| **Message** | One piece of the conversation, with a role: `system`, `user` or `assistant`. |
| **Token** | A small piece of text the model reads. A word can be one or more tokens. |
| **Context limit** | The maximum number of tokens the model can handle at one time. |
| **Generation settings** | Options that control how the model writes, like `temperature` and `max_tokens`. |
| **API** | A way for our Python code to talk to another program over the internet. |
| **API client** | Python code that sends our request to the model and brings back the answer. |
| **API key** | A secret password that lets us use the model. Kept in `.env`. |
| **Structured response** | An answer in a fixed format (like JSON), not free text. |
| **Tool call** | The model asking our code to run a tool, e.g. "run `add_ticket_note` for ticket `T-1001`". |
| **Arguments** | The input values for a tool, e.g. `ticket_id = "T-1001"`, `note = "Customer asked for order status"`. |
| **Proposed action** | Something the model **suggests** doing. Nothing has happened yet. |
| **Executed action** | Something our code has **actually done**. |

---

## Where Day 2 Fits in Our Project

On Day 1, our graph decided the next step using **simple keyword rules**.
From today, an **AI model** helps make that decision.

```
   Day 1                                   Day 2
   ┌──────────────┐                        ┌──────────────┐
   │   Ticket     │                        │   Ticket     │
   └──────┬───────┘                        └──────┬───────┘
          ▼                                       ▼
   ┌──────────────┐                        ┌──────────────┐
   │ if / else    │                        │  AI model    │
   │ keyword rules│                        │  (LLM)       │
   └──────┬───────┘                        └──────┬───────┘
          ▼                                       ▼
   ┌──────────────┐                        ┌──────────────┐
   │  Next step   │                        │  Next step   │
   └──────────────┘                        └──────────────┘
```

---

## 1. Messages, Tokens, Context Limits, and Generation Settings

### Messages

We talk to the model using a **list of messages**. Each message has a **role**.

| Role | Who writes it | Example |
|---|---|---|
| `system` | Us (the developer) – instructions for the model | "You are a customer support assistant. Be short and polite." |
| `user` | The customer | "Where is my order O-9001?" |
| `assistant` | The model | "Let me check order O-9001 for you." |

```python
messages = [
    {"role": "system", "content": "You are a customer support assistant."},
    {"role": "user", "content": "Where is my order O-9001?"},
]
```

```
   ┌────────────────────────┐
   │ system: instructions   │  ◄── how the model should behave
   ├────────────────────────┤
   │ user: customer message │  ◄── what the customer asked
   └───────────┬────────────┘
               ▼
        ┌─────────────┐
        │    Model    │
        └──────┬──────┘
               ▼
   ┌────────────────────────┐
   │ assistant: reply       │  ◄── what the model answers
   └────────────────────────┘
```

> The model does **not remember** old chats by itself. We send the messages it needs **every time**.

### Tokens

- The model does not read whole words. It reads **tokens** (small pieces of text).
- Example: `"delivery"` may be 1 token, `"undelivered"` may be 2–3 tokens.
- Rough idea: **1 token ≈ ¾ of an English word** (100 tokens ≈ 75 words).

**Why tokens matter:**
- 💰 **Cost** – we pay per token (what we send + what the model writes)
- ⏱️ **Speed** – more tokens = slower answer
- 📏 **Limit** – the model can only handle a fixed number of tokens

### Context limit

- The **context** is everything the model sees at once: our messages **+** its reply.
- The **context limit** is the maximum size of that context, in tokens.
- If we send too much, the request fails or old text must be removed.

```
   ┌──────────────────────── Context limit ────────────────────────┐
   │                                                                │
   │  system message  +  user message  +  ticket data  +  reply    │
   │                                                                │
   └────────────────────────────────────────────────────────────────┘
          Everything must fit inside this box
```

> Send the model **only what it needs** for the ticket, not everything we have.

### Generation settings

Settings that control **how** the model writes its answer.

| Setting | What it does | Simple example |
|---|---|---|
| `temperature` | How **creative / random** the answer is | `0` = same answer every time, `1` = more varied |
| `max_tokens` | The **longest** answer allowed | `200` = reply stops after about 150 words |

> For a support agent we want **steady, repeatable** answers → use a **low temperature** (like `0`).

---

## 2. Calling a Model Through the Course API Client

The model runs on the provider's computers, not ours. Our code talks to it through the **course API client**.

```
   ┌──────────────┐  1. messages +   ┌──────────────┐  2. request   ┌──────────────┐
   │  Our Python  │     settings     │  Course API  │  over the     │    Model     │
   │    code      │ ───────────────► │   client     │  internet ──► │  (provider)  │
   │              │                  │              │               │              │
   │              │ ◄─────────────── │              │ ◄──────────── │              │
   └──────────────┘  4. response     └──────────────┘  3. answer    └──────────────┘
```

**Steps:**
1. Our code prepares the **messages** and **settings**
2. The API client sends them to the model, using our **API key**
3. The model writes an answer
4. The API client gives the **response** back to our code

**Instruction-following model** = a model trained to **follow our instructions** in the `system` message (for example, "reply in one sentence").

### Keep the API key secret 🔒

| File | What's inside | Upload to GitHub? |
|---|---|---|
| `.env` | `MODEL_API_KEY=` your **real** key | ❌ Never |
| `.env.example` | `MODEL_API_KEY=your-api-key-here` | ✅ Yes |

---

## 3. Structured Responses and Tool Calls

### Ordinary response vs Structured response

| Ordinary response | Structured response |
|---|---|
| Free text, like a human writes | Fixed format, like JSON |
| Good for **people** to read | Good for **code** to read |
| "I think we should check the order status for O-9001." | `{"next_step": "check_order_status", "order_id": "O-9001"}` |
| Hard for code to use | Easy for code to use: `data["order_id"]` |

> Our agent's **code** needs to read the answer, so we prefer **structured responses**.

### Model-requested tool calls

- The model **cannot** look up or change records by itself.
- So we tell the model which **tools** exist (name + what it does + what inputs it needs).
- The model can then **ask** us to run a tool. This is a **tool call**.

**Example of a tool call from the model:**

```json
{
  "tool": "add_ticket_note",
  "arguments": {
    "ticket_id": "T-1001",
    "note": "Customer asked for the status of order O-9001."
  }
}
```

| Part | Meaning |
|---|---|
| `tool` | **Which** tool the model wants to use |
| `arguments` | The **inputs** for that tool |

### Same ticket, two kinds of answers

```
                    Ticket T-1001: "Where is my order O-9001?"
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
     ┌───────────────────────┐               ┌───────────────────────┐
     │  Ordinary response    │               │  Tool call request    │
     └───────────┬───────────┘               └───────────┬───────────┘
                 ▼                                       ▼
     "Your order is probably on       {"tool": "add_ticket_note",
      its way. Please wait."            "arguments": {"ticket_id": "T-1001",
                                          "note": "Customer asked..."}}
                 │                                       │
                 ▼                                       ▼
     ⚠️ Free text – hard for           ✅ Clear tool name + arguments
        code to use                       that our code can check
```

> A tool call gives our code a **clear request** it can check before doing anything.

---

## 4. Proposed Action vs Executed Action

This is one of the **most important ideas** in the whole course.

| Proposed action | Executed action |
|---|---|
| The model **suggests** doing something | Our code **actually does** it |
| Just data, like a note on paper | A real change or real lookup |
| Safe – nothing has changed | Can change records |
| Example: `{"tool": "add_ticket_note", "arguments": {...}}` | The note is **really** added to the ticket |

```
   ┌──────────────────┐      ┌──────────────────────┐      ┌──────────────────┐
   │      Model       │ ───► │  PROPOSED action     │ ───► │  Our code checks │
   │  asks for a tool │      │  (only a request)    │      │  the request     │
   └──────────────────┘      └──────────────────────┘      └────────┬─────────┘
                                                                    ▼
                                                         ┌──────────────────────┐
                                                         │  Should we run it?   │
                                                         └────┬────────────┬────┘
                                                          YES │            │ NO
                                                              ▼            ▼
                                                 ┌──────────────────┐  ┌──────────────┐
                                                 │ EXECUTED action  │  │ Nothing      │
                                                 │ (really happens) │  │ happens      │
                                                 └──────────────────┘  └──────────────┘
```

> 🔑 **Golden rule:** A tool call from the model is only a **request**. **Our code decides** whether it runs.
> Record changes will need **human approval** (we build this later in the course).

**Today:** we only **look at** the tool call and its arguments. We do **not** run it and we do **not** change any record.

---

## Hands-on

**Our Day 2 files**

| File | What it does |
|---|---|
| `model_client.py` | Course API client: sends messages to the model |
| `prompts.py` | System prompt and the `add_ticket_note` tool description |
| `compare_responses.py` | Asks about the same ticket twice and compares the answers |

**Steps**

1. Install the packages: `pip install -r requirements.txt`
2. Open `.env` and fill in `MODEL_API_KEY`, `MODEL_BASE_URL` and `MODEL_NAME`
3. Run:
   ```bash
   python compare_responses.py
   ```
4. Compare the two answers for ticket T-1001:
   - **Ordinary response:** free text
   - **Tool call request:** tool name + arguments
5. Inspect the arguments: is the `ticket_id` correct? Does the `note` make sense?
6. Open `outputs/comparison.json` and check `"executed": false`. The note was **not** added – no record was changed

---

## Git: Commit and Push

Commit the model-client code, prompts, settings, and comparison examples — **no real API key**.

```bash
git add model_client.py prompts.py compare_responses.py requirements.txt .env.example outputs/comparison.json
git status                        # make sure .env is NOT in the list
git commit -m "Day 2: model client, prompts and comparison example"
git push origin main
```

---

## Quick Recap

- We talk to the model with **messages**: `system`, `user`, `assistant`
- The model reads **tokens**; tokens affect **cost, speed and limits**
- Everything must fit inside the **context limit**
- `temperature` controls randomness; `max_tokens` controls answer length
- The **API client** sends our messages to the model; the **API key** stays in `.env`
- **Structured responses** are easy for code to read
- A **tool call** is the model **asking** to use a tool with certain **arguments**
- **Proposed ≠ Executed**: the model suggests, **our code decides**
