# GigScan 🔍

**Autonomous Economic Intent Detection Agent for the Freelance Economy**

Built for VETROX AGENTIC 3.0 Hackathon | Track 4: The Scholar

> *"We are not looking for toys. We are looking for species."* — AGENTIC 3.0 Manifesto

GigScan is a new species of agent: an autonomous economic actor that monitors opportunity streams, reasons about economic intent, and executes strategic outreach — all without human intervention.

---

## The Problem: Death by a Thousand Scrolls

The autonomous economy is here, but freelancers ans small agencies are still hunting manually.

Every day, potential clients post on X, LinkedIn, Telegram, and Discord — expressing pain, asking for help, announcing funding. These are **economic intent signals** buried under thousands of irrelevant posts.

The current workflow is broken:
- **Manual scanning** = 2+ hours/day lost to scrolling
- **Hesitation** = missed timing kills deals
- **Underpricing** = no systematic budget detection
- **Inconsistency** = some days you hunt, some days you don't

**Result:** High-leverage freelancers and boutique agencies lose an estimated $15k - $30k in annual revenue simply due to 'Signal Decay' - the window between an opportunity appearing in a community and a human noticing it.

## The Solution: An Autonomous Economic Agent

GigScan is not a chatbot. It's an agent that:

1. **Observes** — Continuously monitors opportunity streams
2. **Reasons** — Applies deep economic intent detection using Gemini
3. **Plans** — Matches opportunities to your specific offer menu
4. **Executes** — Generates strategic, ready-to-send outreach

The human stays in the loop only for the final send. Everything else is autonomous.

---

## Philosophy of Design

### Assumption Challenged: "Agents should automate everything"

Wrong. Premature automation creates spam and destroys trust.

GigScan automates **observation, reasoning, and planning** — but keeps humans in the execution loop. The agent drafts; the human sends. This is intentional:

- **Preserves authenticity** — responses feel human because they are human-approved
- **Avoids platform bans** — no auto-DM behavior that triggers spam filters
- **Builds trust** — the agent is a co-pilot, not an autopilot

### Assumption Challenged: "More data = better results"

Wrong. Most opportunity-finding tools try to aggregate everything.

GigScan does the opposite: **aggressive qualification filtering**. We optimize for signal-to-noise ratio, not volume. A freelancer with 3 high-confidence, budget-qualified leads beats one with 100 maybes.

### Assumption Challenged: "Agents need complex infrastructure"

Wrong. The best agents have elegant, minimal architectures.

GigScan's core is a single reasoning loop:

```
Observe (stream) → Reason (Gemini) → Plan (match) → Execute (draft)
```

No database. No complex state. No authentication flows. Pure reasoning.

This means GigScan works with **any text source**: X posts, LinkedIn messages, Upwork jobs, Telegram chats, Discord servers. The intelligence is in the reasoning, not the plumbing.

### The Elegance

The agent embodies a simple insight: **Economic intent has a fingerprint.**

When someone says "Just raised our seed, need help with narrative" — that's not just text. It's a structured signal:
- **Budget indicator:** High (funding announced)
- **Urgency:** High (post-raise momentum)
- **Need:** Specific (narrative help)
- **Decision speed:** Fast (small team, funded)

GigScan reads these fingerprints and acts on them.

### Why Gemini?

- **Superior Inference:** Complex economic reasoning without hallucination
- **Speed:** Sub-2 second analysis enables real-time monitoring
- **Context:** Understands nuanced professional intent across domains

---

## Quick Start

### Prerequisites

- Python 3.9+
- Gemini API key ([Get one free](https://aistudio.google.com/))

### Installation

```bash
git clone https://github.com/yourusername/gigscan.git
cd gigscan
pip install -r requirements.txt
```

### Run

```bash
# Set your API key
export GEMINI_API_KEY="your-key-here"

# Interactive mode (manual analysis)
python gigscan.py

# 🤖 AUTONOMOUS MODE - watch a file for new posts
python gigscan.py --watch posts.txt

# Batch mode - analyze a file of posts
python gigscan.py --batch posts.txt
```

---

## Usage Modes

### 1. Autonomous Watch Mode (Recommended for Demo)

The agent monitors a file continuously and analyzes new posts automatically:

```bash
python gigscan.py --watch posts.txt
```

```
🤖 GIGSCAN AUTONOMOUS MODE ACTIVATED
============================================================
📁 Watching: posts.txt
⏱️  Check interval: 5s
🛑 Press Ctrl+C to stop

👀 [14:32:01] Watching... (analyzed: 0, opportunities: 0)
🔍 [14:32:15] Analyzing new post...

============================================================
🎯 OPPORTUNITY DETECTED
============================================================
⏰ Time: 14:32:17
📊 Confidence: 95%
💰 Budget: high | ⚡ Urgency: high
...
```

In another terminal, add posts to the file:
```bash
echo "Just raised our seed! Need help with narrative." >> posts.txt
```

The agent detects and analyzes automatically. **Zero human intervention.**

### 2. Interactive Mode

```bash
python gigscan.py
```

Paste posts manually for one-off analysis.

### 3. Batch Mode

```bash
python gigscan.py --batch posts.txt
```

Analyze all posts in a file at once.

---

## Customization

Edit the top of `gigscan.py` to match your profile:

```python
YOUR_SKILLS = """
- Your skill 1
- Your skill 2
"""

YOUR_OFFERS = [
    {
        "name": "Your Offer Name",
        "description": "What you deliver",
        "price": "$X",
        "ideal_for": "Who this is for"
    }
]
```

---

## Technical Architecture

```
                    ┌─────────────────────────────────────┐
                    │        AUTONOMOUS AGENT LOOP        │
                    └─────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
   ┌───────────┐              ┌───────────┐              ┌───────────┐
   │  OBSERVE  │      →       │  REASON   │      →       │  EXECUTE  │
   │  Stream   │              │  Gemini   │              │  Draft &  │
   │  Monitor  │              │  Engine   │              │  Log      │
   └───────────┘              └───────────┘              └───────────┘
```

**Components:**
- **Stream Monitor** — File watcher, batch input, or interactive
- **Reasoning Engine** — Gemini-powered economic intent detection
- **Offer Matcher** — Maps problems to your service menu
- **Response Generator** — Style-aware outreach drafting
- **Opportunity Logger** — JSON log of qualified leads

---

## Judging Criteria Alignment

| Criteria | Weight | How GigScan Delivers |
|----------|--------|---------------------|
| **Autonomy** | 30% | Watch mode runs continuously. Agent observes, reasons, and executes independently. Human only approves final send. |
| **Technical Craft** | 25% | Clean architecture. Single-file elegance. Rate limit protection. Extensible to any data source. |
| **Innovation** | 25% | Not a chatbot — an economic agent. Introduces "economic intent fingerprinting" as a new pattern. |
| **Utility** | 20% | Solves a real $20k+ annual 'Revenue Leak' caused by Signal Decay. Already in production use by the builder. |

---

## Roadmap

### Phase 1: MVP ✅
- Core reasoning engine
- Interactive + Batch + **Autonomous Watch** modes
- Opportunity logging

### Phase 2: Multi-Source Integration
- X/Twitter API
- Telegram monitoring  
- Upwork job feed
- Discord scanning

### Phase 3: Full Autonomy
- Scheduled scanning
- Push notifications
- One-click send queue

### Phase 4: Platform
- Multi-user SaaS
- Custom profiles
- Analytics

---

## License

MIT — Fork it, improve it, ship it.

---

## Author

Built with urgency by a founder who needed this yesterday.

*The future belongs to the builders who ship.*
