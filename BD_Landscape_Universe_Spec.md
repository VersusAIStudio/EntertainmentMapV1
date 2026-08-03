# BD Landscape Universe — Standardized Spec & Build Procedure

**Purpose.** Turn "where entertainment work is happening and who is doing it" into one scalable, filterable web. Paramount is company #1 (proof of concept). The same schema drops in Netflix, Disney, Amazon, WBD, and so on — and because companies share vendors and people, they connect into a single universe instead of separate charts.

**What this document is.** The definition of the data model, the color/confidence system, and the exact procedure to add the next company. Anyone on the team can follow it to keep the map consistent. It pairs with the working prototype (`index.html`).

---

## 1. The core idea

The inspiration poster (Media Universe 2026) is a *snapshot* — bubbles sized by market cap. What we're building is a *relationship graph* — who flows work to whom. Same visual family, different engine.

Every row in the Paramount spreadsheet is really a set of **nodes** and **connections** in disguise. Once the data is modeled that way, the picture assembles itself and stays consistent as it grows.

The single most important design decision: **entities are shared across companies.** A vendor that works for both Paramount and Netflix is *one node* touching both. That shared node is a bridge — and the bridges are where the strategic insight lives (who's entrenched everywhere, where the whitespace is, what warm route reaches two clients at once).

---

## 2. Node types (the five things on the map)

| Node | What it is | Example | Sizing |
|---|---|---|---|
| **Company** | Top-level client universe | Paramount | Fixed (root) |
| **Division** | Brand / network / platform / studio inside the company | Paramount+, BET, Pictures | By # of connected projects |
| **Project** | A single campaign or piece of work | UFC opener, SpongeBob Sphere | By connections |
| **Player** | Any external company doing the work — agency, production co, post house, platform, sponsor, brand partner | Droga5, O Positive, Versus | By # of projects (recurrence) |
| **Person** | A decision-maker or credited contact | Katherine Kelly, Matt Hernandez | By opportunity score |

**Versus is a Player node too** — the home team — and is always drawn in gold so we can instantly see where we already have a footprint in any universe.

## 3. Edge types (the connections)

| Edge | Direction | Meaning |
|---|---|---|
| `hierarchy` | Company → Division | Org structure |
| `commissions` | Division → Project | This team gave out this work |
| `made-by` | Project → Player | This vendor did this work |
| `credited` | Project → Person | Person publicly credited on the work |
| `worked-with` | Player → Division | Derived: this vendor has done work for this team |
| `decision-maker` | Division → Person | Person who approves work here |

## 4. Required fields per node

Keeping these fields identical across companies is what makes the universe scalable. This *is* the standardized procedure.

- **Project:** name · division · work-type tags · confidence (High/Med/Low) · credited contacts · players · source(s) · notes
- **Player:** name · type (agency / production / post / platform / sponsor / brand) · repeat-relationship? · divisions worked with (derived) · signature color (recurring players only)
- **Person:** name · division · title · role/attribution label · confidence · route/access notes · opportunity score (0–100, when ranked)

**Attribution labels** (carried straight from Rob's rules, never blur them): *Confirmed commissioner* · *Confirmed stakeholder* · *Likely decision-maker* · *Responsible team identified*.

## 5. Color & confidence system

- **Divisions** are color-banded by group (each division a distinct hue) so you can see at a glance where work concentrates — the equivalent of the poster's colored sectors.
- **Players** get a **signature color** once they recur (Rob's "purple = Anomaly" convention). In the Paramount set, purple family = the anchor agency (Droga5); **Versus = gold, reserved forever.** New recurring players get the next color off the palette and keep it in every universe.
- **People** are heat-shaded by opportunity score (brighter = higher priority) and sized the same way.
- **Confidence** is a consistent green / amber / red chip on every project and person. This is also where the known data gap lives: **project budgets are not public** — size/cost stays flagged, not guessed.

## 6. The three lenses (one graph, three questions)

The prototype answers Rob's six goals through three toggleable views over the *same* data:

1. **Work-flow** — Company → Division → Project → Player. *Where does work go and who does it?* (Goals 1, 2, 3)
2. **Partners** — Players as hubs linked to the divisions they serve. *Who's entrenched, who recurs, where's the whitespace?* (Goals 2, 4, 6) — and cross-company bridges surface here.
3. **Access** — People linked to their divisions, sized/heated by opportunity score. *Who do we call first and what's the route?* (Goal 5)

Plus live filters (division, confidence) and search, so the team can isolate, e.g., "every Medium-confidence Paramount+ project" or "everything Versus already touches."

---

## 7. Procedure to add company #2 (and every one after)

1. **Run the same deep-research prompt** (Rob's Paramount prompt) with the new company swapped in. Output is the same tab structure: Landscape Map · Players · Decision-Makers · Opportunity Targets.
2. **Fill the identical columns.** Do not invent new fields; the schema in §4 is fixed. Consistency is the whole point.
3. **Reuse existing Player and Person names verbatim.** If O Positive already exists from Paramount, use the exact same string — that's what fuses the two universes into one and creates the bridge node automatically.
4. **Assign colors only to *new* recurring players.** Existing signature colors (and Versus gold) never change.
5. **Drop the rows into the loader.** The graph rebuilds; shared vendors/people now link the companies; counts and lenses keep working with zero layout effort.

That last property — add data, the picture updates itself — is the "scalable & predictable" requirement from the brief.

## 8. What the proof of concept already proves

- 10 divisions · 39 projects · 47 players · 30 people, fully modeled and connected (212 relationships), zero dangling links.
- All three lenses, filtering, search, and click-through detail working.
- Versus footprint visible instantly (gold) — currently concentrated in Paramount+/DTC, Pluto, and Nickelodeon.
- The single known gap is honestly flagged: **no public budgets**, so project size is a research target, not a fabricated number.

## 9. Where this can go next

- **Embed / linkable nodes** (Rob's Miro ask): attach the LinkedIn URL, headshot, and video-of-the-work to each Player/Person/Project — the schema already has a slot for it.
- **Live data source:** back the graph with Airtable or a sheet so BD updates flow in without touching code.
- **Bridge highlighting:** once company #2 is in, auto-flag every node that touches more than one company — the highest-leverage targets.
- **Export a Miro-ready layout** from the same dataset for presentation, satisfying both the brief's tool and the scalable engine underneath.

*Data source: Carrie's Paramount deep research (Versus 2026 project). Proof of concept due Aug 5.*
