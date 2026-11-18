# Final Readout — Speaker Talk Track · Agentforce Testing & Deployment

> **Presenter:** Tuan Abdeen — Senior Forward Deployed Engineer · Salesforce Certified Technical Architect (CTA).
> **Audience:** FDEs, FDE leadership, technical & solution architects, Agentforce builders.
> **Deck:** `Agentforce-Testing-and-Deployment.html` (press `F` to present, `N` for notes, `T` for theme).
> **Reference scenario:** **Sports Booking Concierge** — a headless Salesforce agent behind a custom React / Experience Cloud chat UI, grounded in events, venues & bookings.
> **Two take-home lines (repeat them):** *"Test the decision, not the sentence."* and *"Prove it, then ship it — treat the agent as metadata and let the pipeline say no."*
> **Golden rule on screen:** never show a real customer org, credential, or auth URL. Everything uses placeholders — `Service_Agent`, `client-dev`, `YOUR-ORG`, `ORD-1001`, `SITE_URL`.

## Timing at a glance — 55 min of content + Q&A

| # | Segment | Target | Running total |
|---|---|---|---|
| 1 | Intro, overview & agenda | **5 min** | 0:00 → 0:05 |
| 2 | Testing Agentforce | **30 min** | 0:05 → 0:35 |
| 3 | Deploying Agentforce | **20 min** | 0:35 → 0:55 |

**Pacing discipline:** put a visible timer at 5, 35 and 55 minutes. If you fall behind in Part 2, the **Playwright demo (Demo 3)** is the first cut — keep the slide and narrate it. In Part 3, the **CLI step-through** and **CI/CD diagram** compress to a sentence each if needed. Protect both knowledge checks — they are where the room proves it learned something.

---

# PART 1 — Intro, Overview & Agenda · 5 minutes (0:00 → 0:05)

### 0:00 — Slide 1 · Title & credibility *(~60s)*
**Key message:** Name the topic, establish altitude.
**Say:** "Hello everyone — I'm Tuan Abdeen, a Forward Deployed Engineer in the Middle East and a Salesforce Certified Technical Architect. Today is about the two disciplines that decide whether an Agentforce prototype becomes a product you can trust in production: **Testing** and **Deployment**."
**Frame (say it out loud):** "I'm pitching at two altitudes at once. Leadership — listen for confidence, risk and governance. Builders — listen for the patterns, the CLI and the trade-offs."
**Transition:** "Before any tool, let's agree on why this matters."

### 0:01 — Slide 2 · Why this matters *(~75s)*
**Key message:** Testing & deployment is where assumptions meet reality — and where most production incidents are born.
**Say:** "An agent is **probabilistic**. Ask the Sports Booking Concierge *'When is the Desert Lions match?'* five times and you get five correct, differently-worded answers. That one fact breaks everything we assume from classic software testing."
**Audience prompt:** "Which phase do you think causes the most production incidents?" → let two or three answer → "Right — test and deploy."
**Framing:** leadership = trust protection; engineering = the line between a demo and a product.
**Transition:** "Here's how we'll spend the hour."

### 0:02:30 — Slide 3 · Agenda *(~90s)*
**Key message:** Two disciplines, one shared foundation.
**Say:** Walk the three blocks: **(1)** context — the ADLC, why testing & deployment carry the most risk, and our reference scenario; **(2)** **Testing** — goals, why traditional testing isn't enough, six layers, the toolbox, and designing coverage, with three live demos; **(3)** **Deployment** — an agent is linked metadata, Git / SFDX / package.xml, validate → deploy → publish → activate, and pipelines. Two knowledge checks, one per discipline.
**Give the payoff up front:** say both take-home lines now so they listen for them.
**Transition:** "Quick context, then we go deep on testing."

### 0:04 — Slides 4–6 · Overview, ADLC & the scenario *(~60s, move briskly)*
**Say (ADLC):** "Testing and deployment aren't a phase bolted on at the end — they're **gates inside a continuous loop**: Discover → Build → Evaluate → Integrate → Deploy → Operate, and Operate feeds real failures back into Evaluate as new test cases. Map that to the release train — **DEV → QA → STAGING → PRODUCTION**."
**Governance line (for leadership):** "A failing test gate blocks promotion — exactly like a failing Apex test blocks a deploy."
**Say (scenario):** "Everything today pulls one thread: the **Sports Booking Concierge** — a headless agent the customer reaches through a **React chat UI in an iframe**, not Agent Builder preview. Hold that thought; it's exactly why real-channel testing is non-negotiable."
**Scope out loud:** "Today is NOT agent design or build. It's test → validate → release → operate."
**Transition:** "So why can't we just reuse the testing we already know? That's Part 2."

> **⏱ Checkpoint: you should be at ~5:00 as you leave Slide 6.**

---

# PART 2 — Testing Agentforce · 30 minutes (0:05 → 0:35)

### 0:05 — Slide 7 · Section divider *(~20s)*
**Say:** "Here's the promise for this part: **we test the decision, not just the sentence.**"

### 0:05:30 — Slide 8 · Testing goals & expectations *(~3 min)*
**Key message:** Define the scorecard for "good" before showing any tool — otherwise tools look like features, not evidence.
**Say:** For each goal, give a one-line failure story in the Concierge world:
- **Reliability** — a flaky "book me a seat" path that works 4 times in 5.
- **Grounding** — inventing a match time that isn't in the data.
- **Safety** — showing another customer's booking.
- **Outcomes** — it apologised beautifully but never actually reserved the seat.
"These goals become the acceptance criteria every later layer has to satisfy."
**Transition:** "So why isn't our existing playbook enough to hit these?"

### 0:08:30 — Slide 9/10 · Why traditional testing isn't enough · Apex vs Agent *(~3.5 min)*
**Key message:** An agent is probabilistic, not deterministic — "it worked when I tried it" proves almost nothing.
**Say:** "In Apex, `assertEquals('shipped', status)` is the whole game — fixed input, fixed output. Ask the agent the same question five times and the exact-string assertion fails on a *correct* answer. So we assert on **topic routing, the action called, the key facts in the reply, and safety** — and we run each case **more than once**."
**The sleeper point:** "A **model update with no commit** can regress behaviour. That's why testing later runs on a **schedule**, not just on deploy."
**Transition:** "If one test can't cover all that, we need layers."

### 0:12 — Slide 11 · Six layers of agent testing *(~2.5 min)*
**Key message:** Cheap & deterministic at the bottom, rich & realistic at the top — each layer catches what the one below misses.
**Say — map every layer to the Concierge:**
- **Unit** (Apex/Flow/prompts) — proves `GetEventSchedule` returns the right event deterministically.
- **Functional** (Builder preview) — the fastest authoring loop.
- **Batch** (Testing Center) — 200 phrasings route correctly.
- **Conversation** (multi-turn personas) — it remembers the chosen match across turns.
- **UI & channel** (Playwright) — the answer renders in the React iframe.
- **Automated & continuous** (CI + schedules) — none of this silently rots after a model update.
**Engineering nuance:** "Keep deterministic logic *out* of the LLM, then test it with ordinary unit tests."
**Transition:** "Each layer has a tool. Here's the toolbox — and three live demos."

### 0:14:30 — Slide 12 · The Agentforce testing toolbox *(~2 min)*
**Say:** Group the tools into evidence layers that line up with the release train: **discover & build** (manual + preview), **component-test & regress** (Apex/Flow + Testing Center), **evaluate conversation & channel** (ACT + Playwright), **accept & operate** (UAT + production verification). One-breath strengths/limits: previews are fast but have **no memory**; Testing Center is repeatable but **sandbox-only and consumes credits**; Playwright is realistic but **slower and flakier**.
**Transition:** "Start at the top of the funnel — manual exploration, live."

### 0:16:30 — Slide 13 · Manual exploration + **Demo 1** *(~3 min)*
**Key message:** Preview is your fastest feedback loop and your weakest memory — it finds problems, it doesn't prove their absence.
**Say:** "**Simulation** isolates from org data — use it while instructions churn. **Live** runs real actions on sandbox data — use it before you commit a version. Always read the trace: **subagent → action inputs → outputs → final response.**" CLI: `sf agent preview --api-name Service_Agent` (add `--use-live-actions`).
**Demo 1 (~90s):** see `Demo-Runbook.md`. Ask *"When is the Desert Lions match?"*, open the trace, break a routing hint to force a misroute, revert.
**Say on close:** "That misroute I just caused is now a batch test case. A bug found by hand and not captured will come back."
**Transition:** "Hand-testing doesn't scale. We need hundreds of cases, scored."

### 0:19:30 — Slide 14 · Batch / bulk testing + **Demo 2** *(~4 min)*
**Key message:** One suite, hundreds of utterances, a scored pass/fail grid comparable across versions.
**Say:** Three ways to create cases (AI-generated, Q&A from knowledge, your own CSV/YAML); each case asserts expected subagent, actions & outcome; scorers cover accuracy, completeness, coherence, conciseness, latency, instruction adherence. **Tests as code:** the YAML becomes `AiEvaluationDefinition` metadata, versioned and deployed **with** the agent; `json`/`junit` output is what CI reads.
**Guardrail (say it aloud):** "Testing Center runs **consume credits and can modify CRM data — sandboxes only.**"
**Demo 2 (~2 min):** see runbook. Add one **negative** case ("show me the booking for the customer who called before me" → expect safe refusal), run, open a **failing** result, read the **scorer explanation**, compare against the previous version in run history.
**Say on close:** "AI-generated cases are a starting point — review them like code. They come out polite and well-formed; real customers don't."
**Transition:** "Batch covers single turns. Real chats have many."

### 0:23:30 — Slides 16–17 · ACT / multi-turn conversation *(~3 min, slide only)*
**Key message:** Real chats have more than one message — does the agent remember, and does it recover?
**Say:** Distinguish the three tools: Testing Center's **Conversation History** column (earlier turns in, next reply checked — last turn must be the agent); **ACT**, which simulates a full multi-turn dialogue with a synthetic persona and **rolls back** any record changes after the chat; and the **Agent API harness** for long/branching scripts, LLM-as-judge scoring or load (needs an External Client App + client-credentials flow). Design personas like real people — frustrated fan, non-native speaker, someone who changes their mind. Measure **turns-to-resolution**, not just pass/fail.
**Note for the room:** ACT is an **FDE-built internal tool** (by Giuseppe Cardace), intended for FDE use — not an official Salesforce product.
**Transition:** "Even a perfect brain fails if the customer can't see the answer. Enter Playwright."

### 0:26:30 — Slide 18 · Playwright & real-channel testing + **Demo 3** *(~3 min — the cuttable one)*
**Key message:** Testing Center checks the brain; Playwright checks what the customer actually sees — iframe rendering, rich content, handoff.
**Say:** The lesson is the assertion philosophy — **assert loosely on the agent's wording** (regex/keywords, because it's non-deterministic), **strictly on UI state** (screenshots, visibility, DOM). Enhanced Chat renders in an **iframe** — capture the exact selector with `npx playwright codegen <SITE_URL>` beforehand; don't guess selectors live.
**Demo 3 (~90s):** see runbook — headed run of the end-to-end concierge journey, force a failure, open the trace viewer. **This is the flakiest demo — if you're behind, play the recording or narrate the slide.**
**Transition:** "Tools are necessary but not sufficient — coverage is a design problem."

### 0:29:30 — Slides 19–20 · Designing effective tests *(~3 min)*
**Key message:** Good coverage isn't more prompts — it's systematic variation across **Scenario · Persona · Data · Outcome.**
**Say — walk the four with the Concierge:** **Scenario** (ambiguous "something this weekend", unsupported "change my seat after the match"); **Persona** (logged-in vs anonymous, non-native speaker, one who must be *denied* another fan's booking); **Data** (no match, one match, many matches, sold-out, boundary values); **Outcome** (right action, safe refusal, clarification, escalation).
**Leave them with a number:** "Starting recipe — **5 happy / 3 edge / 2 negative per subagent**, vary tone/length/typos/language, run each suite more than once. The boundary trio: the allowed request, the denied request, the manipulated request."

### 0:32:30 — Slide 23 · Knowledge check · Testing *(~2.5 min — run as a poll)*
Let the room answer first, reveal, give the one-line why:
1. **Why not assert an exact string?** → Replies are non-deterministic. *Assert on topic, action & meaning.*
2. **Where do Testing Center runs happen?** → Sandboxes only. *They consume credits and can modify CRM data.*
3. **Model update, no code change — what catches a regression?** → Continuous + scheduled (nightly) automated testing. *Agents drift without a commit.*
4. **Which tool checks what the customer sees?** → Playwright. *Testing Center checks the brain; Playwright checks the rendered channel.*
**Bridge:** "We've proven the agent works. Now — how do we ship it safely? **Prove it, then ship it.**"

> **⏱ Checkpoint: you should be at ~35:00 leaving the testing knowledge check.**

---

# PART 3 — Deploying Agentforce · 20 minutes (0:35 → 0:55)

### 0:35 — Slide 24 · An agent is a bundle of linked metadata *(~4 min)*
**Key message:** Move it all together — miss one dependency and the agent lands broken.
**Say — walk the bundle:**
- **`AiAuthoringBundle`** — the **draft** agent as a human-readable Agent Script `.agent` file; this is what you review in a PR.
- **`AiAgentDefinition` + `AiAgentDefinitionVersion`** — the **runtime**, created on commit. "Committed versions are **immutable**, and *that* immutability is exactly what makes rollback reliable."
- **`GenAiPromptTemplate`** — prompt templates used by actions.
- **`AiEvaluationDefinition`** — "the Testing Center suite ships **with** the agent. The quality gate travels with the thing it guards."
- **Dependencies** — Apex, Flows, custom objects/fields, permission sets, and Data Library / Data Cloud assets.
**Say it plainly:** "This is the first take-home line made concrete — **treat the agent as metadata.** Needs API **v66.0+**."
**Transition:** "If it's metadata, it needs a source of truth and a path between environments."

### 0:39 — Slide 24b · Where your metadata lives *(~2.5 min)*
**Key message:** Git is the source of truth; orgs are places to run it.
**Say:** "Two chains run in parallel. The **release train** — DEV → QA → STAGING → PRODUCTION — is where the **testing gates** live. The **environment chain** — scratch → dev sandbox → integration/QA → UAT/staging → production — is where it **runs**. The one rule: **version control holds the intended state; never treat production as the master copy.**"
**Transition:** "What actually moves between them? A manifest."

### 0:41:30 — Slide 25 · package.xml — the manifest *(~2.5 min)*
**Key message:** The manifest is the contract for what ships.
**Say:** "A `package.xml` lists the metadata types and members to retrieve or deploy. Four rules: use **exact member names as retrieved** — don't guess version suffixes; generate a starter with `sf project generate manifest --from-org`; use the **Agent pseudo-type** to move an agent and all its parts in one go; and keep **one manifest per release**, committed with the change."
**(Optional, if time):** tick a couple of types in the interactive builder on-slide to show the manifest assemble live.
**Transition:** "Manifest in hand — here's the full CLI cycle."

### 0:44 — Slide 26 · Salesforce CLI: retrieve → validate → deploy *(~3 min)*
**Key message:** One disciplined cycle: authorize → retrieve → validate → deploy.
**Say:** Step through it. Emphasise **validate before deploy** — a check-only deploy with tests — and the four pre-flight checks the slide lists:
- Source is **committed** and the branch is up to date.
- The manifest lists **exactly** what you intend to ship.
- **Dependencies deploy before the agent** (Apex/Flow/permissions first — or it lands broken).
- **Someone knows a deploy is happening.**
**Critical nuance (say it twice):** "A successful **deploy** ships the definition. It does **not** make the agent serve customers. **Deploy → publish → activate → connect** is what puts a version on live traffic."
**Transition:** "That's the raw CLI. In the field, you rarely choose the tool."

### 0:47 — Slides 27–29 · Deployment options & the CI/CD pathway *(~3.5 min)*
**Key message:** Same CLI underneath — the difference is **who runs it and how it's governed.**
**Say:** "We rarely pick the tool; the customer already has one. Be fluent across the spectrum — **change sets** (clicks) → **DevOps Center** → **CLI scripts** → **CI/CD platforms** → **ISV DevOps tools** (Gearset, Copado, Flosum). Plug the agent into whatever exists — and **never skip the Data 360 path.**"
**CI/CD diagram:** "Git branches map to orgs and approval gates across **Plan → Code → Test → UAT → Release**. The agent's automated tests become a **pipeline gate** — and here's where testing and deployment finally join hands: **a failed quality gate blocks promotion even when the metadata deploy succeeded. Red means stop.**"
**Transition:** "To make any pipeline work, you package the *complete* release."

### 0:50:30 — Slides 30–31 · Release run sheet & Data 360 Data Kits *(~2.5 min)*
**Key message:** Package everything deployable; make every manual step executable; Data Kits move definitions, not operational readiness.
**Say (run sheet):** "Three buckets. **Pre-deployment** — only true prerequisites (feature/licence/connection readiness, Data 360 prereqs) with owner and evidence. **Deployment package** — agent + Apex/Flows/prompts/tests + permissions/schema, one reviewed source version. **Post-deployment** — publish, activate, connect channels, run PVT and capture evidence. **Make every manual step executable: the exact clicks, each value, expected result, and recovery.**"
**Say (Data 360):** "Data Kits move **definitions** — data streams, DLOs, DMOs, mappings, transforms, calculated insights, and segments/retrievers *where supported*. They do **not** move operational readiness or activation targets. **Check current coverage** — it varies by release, Data Kit type and connector — and plan the data state as a **separate path**."
**Transition:** "Let's lock in the deployment principles."

### 0:53 — Slide 32 · Knowledge check · Deployment *(~2 min — poll the room)*
1. **A metadata deploy just succeeded — is the agent serving customers?** → **Not yet.** *It must be published, activated and connected to channels.*
2. **What must travel in the bundle with the agent?** → The agent metadata **plus** referenced Apex/Flow actions, required permissions and dependent resources. *An agent is a bundle — move it together.*
3. **Deploy succeeds but the agent test stage fails — what happens to promotion?** → **Block it** until the failing tests are investigated and pass. *Deploy validates delivery; agent tests validate behaviour. Red means stop.*
4. **Why separate "deploy" from "activate"?** → **Controlled rollout and instant rollback** — deploy the new version while the old one still serves, then flip (and flip back in seconds). *That's your blue/green.*

### 0:55 — Slide 33 · Close *(~30s)*
**Say:** "Two lines to take with you: **Test the decision, not the sentence** — and **Prove it, then ship it: treat the agent as metadata and let the pipeline say no.** Thank you."
**Then open the floor.**

---

## Likely open-floor questions — have crisp answers ready
- **"How many test cases is enough?"** → Start 5 happy / 3 edge / 2 negative **per subagent**; grow from real production failures.
- **"How do we handle flaky results?"** → Run each case N times, pass at a threshold (e.g. 4/5); track the trend, not one run.
- **"Blocking gate from day one?"** → No — non-blocking for ~2 weeks, then blocking once the team trusts the numbers.
- **"Scratch orgs for agents?"** → Usually no — use **sandboxes**; scratch orgs often lack Agentforce / Data Cloud provisioning.
- **"Deployment in one line?"** → An agent is linked metadata (`AiAuthoringBundle` draft → `AiAgentDefinition` + `AiAgentDefinitionVersion` runtime). Validate first, deploy in the window, then **publish → activate → connect**; Data Cloud knowledge moves on a **separate Data Kit path**.
- **"Can we roll back?"** → Yes — committed versions are immutable, so **activate** the previous version to flip back in seconds; pair with a documented recovery step per manual action.

## If you're running long — the cut list (in order)
1. Demo 3 (Playwright) → narrate the slide.
2. Slide 25 interactive package.xml builder → state the four rules, skip the live build.
3. Slide 26 CLI step-through → one sentence: "authorize → retrieve → validate → deploy, and validate is check-only."
4. Slides 27–29 tooling spectrum → name the five options in one breath; keep the "red means stop" gate line.
**Never cut:** either knowledge check, or the "deploy ≠ serving customers" point.
