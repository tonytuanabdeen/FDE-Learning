# Presenter Talk Track — Agentforce Testing & Deployment

> **Audience:** FDEs, FDE leadership, technical & solution architects, Agentforce builders.
> **Duration:** 30–35 minutes incl. demos and interaction.
> **Deck:** `Agentforce-Testing-and-Deployment.pptx` (19 slides). The same notes live in each slide's presenter-notes pane.
> **Two take-home lines (repeat them):** *"Test the decision, not the sentence."* and *"Treat the agent as metadata — ship it with its dependencies and let the pipeline say no."*
> **Golden rule on screen:** never show a real customer org, credential, or auth URL. All examples use placeholders — `Service_Agent`, `client-dev`, `YOUR-ORG`, `ORD-1001`.

**Suggested pacing (35 min):** Intro & context (slides 1–6) ≈ 7 min · Testing concepts (7–10) ≈ 7 min · Toolbox & tools incl. 3 demos (11–16) ≈ 14 min · Designing tests (17–18) ≈ 4 min · Knowledge check + close (19) ≈ 3 min. If you fall behind, cut the **Playwright demo** first (keep the slide); protect the knowledge check.

---

## Slide 1 — Introduction
**Key message:** Establish credibility and name the topic.
**Say:** "Hello everyone, I'm Tuan Abdeen, a Salesforce Certified Technical Architect — one of roughly 400 globally — and a Forward Deployed Engineer in the Middle East. Today we explore one of the most important aspects of delivering production-ready Agentforce solutions: Testing & Deployment."
**Frame:** This session is pitched at two altitudes at once — leadership gets confidence and governance; engineers get patterns, CLI, and trade-offs.
**Transition:** "Before any tool, let's agree on *why* this matters."

## Slide 2 — Setting the objectives
**Key message:** Testing & deployment is where assumptions meet reality — and where most production incidents are born.
**Say:** Walk the six objectives; dwell on *behave consistently* and *earn confidence before production*. Make the probabilistic point concrete: the same question asked five times yields five correct but differently-worded answers.
**Audience prompt:** "Which phase causes the most production incidents?" → test & deploy.
**Leadership framing:** risk management and trust protection. **Engineering framing:** the line between a prototype and a product.
**Transition:** "Here's how we'll spend our time."

## Slide 3 — Agenda
**Key message:** Two disciplines — testing then deployment — on one shared foundation.
**Say:** Note the context block comes first (overview, ADLC, WISMO, why testing matters). Tell them format: demos interleaved, a knowledge check at the end. Give the two take-home lines up front so they listen for the payoff.
**Transition:** "Let's start with the big picture."

## Slide 4 — Overview *(section divider)*
**Say (≈15s):** "Three things set the frame before the deep content — where testing and deployment sit in the lifecycle, the reference scenario we reuse all session, and why agentic testing needs a different mindset."

## Slide 5 — The Agent Development Lifecycle (ADLC)
**Key message:** Testing and deployment are *gates inside a continuous loop*, not a phase bolted on at the end.
**Say:** Walk Discover → Build → Evaluate → Integrate → Deploy → Operate, and stress the loop back: Operate (production monitoring + session traces) feeds new failures into Evaluate as fresh test cases. Then the release train — **DEV → QA → STAGING → PRODUCTION** — and map gates to stages: unit + functional at DEV; batch, multi-turn and red-team at QA; UAT and channel validation at STAGING; activate, verify, monitor at PROD.
**Governance line (for leadership):** "A failing test gate blocks promotion — exactly like a failing Apex test blocks a deploy."
**Transition:** "Everything from here uses one concrete scenario."

## Slide 6 — The reference scenario: WISMO
**Key message:** One thread pulled through every demo.
**Say:** Architecture, kept deliberately simple — a custom React conversational UI on an Experience Cloud site, talking to a headless Salesforce **Service Agent** via the Agent API, grounded in Orders/Cases/knowledge. Why headless + React matters: the customer never touches Agent Builder preview — they touch your React UI *in an iframe* — which is exactly why real-channel (Playwright) testing is non-negotiable.
**Scope out loud:** today is NOT agent design or build. It is test → validate → release → operate.
**Transition:** "So why can't we just reuse the testing we already know?"

## Slide 7 — Agentforce testing *(section divider)*
**Say:** Repeat the promise: "We test the decision, not just the sentence." Then into goals.

## Slide 8 — Why testing matters: goals & expectations
**Key message:** Define the scorecard for "good" before showing any tool — otherwise tools look like features, not evidence.
**Say:** For each goal give a one-line failure story: reliability (a flaky refund path), grounding (a made-up refund window), safety (leaking another customer's order), outcomes (it apologised nicely but never cancelled the order). These six become the acceptance criteria the later layers satisfy.
**Transition:** "So why isn't our existing test playbook enough to hit these?"

## Slide 9 — Why traditional testing isn't enough
**Key message:** An agent is probabilistic, not deterministic — "it worked when I tried it" proves almost nothing.
**Say:** Talk down the rows; spend most time on **What you assert** and **What triggers a retest**. "In classic Apex, `assertEquals('shipped', status)` is the whole game. Ask an agent 'where's my order?' five times and you get five correct but different sentences — assert on the exact string and a right answer fails. So we assert on topic routing, the action called, the key facts in the reply, and safety — and we run each case more than once." The sleeper row: a **model update with no commit** can regress behaviour — which is why testing later runs on a schedule.
**Transition:** "If one test can't cover all that, we need layers."

## Slide 10 — A multi-layer testing strategy
**Key message:** Each layer catches what the one below misses; cheap/deterministic at the bottom, rich/realistic at the top.
**Say:** Map to WISMO — unit proves `GetOrderStatus` returns the right status; batch proves 200 phrasings route correctly; multi-turn proves the agent remembers the order number across turns; red team proves it won't show another customer's order; UI proves the answer renders in the React iframe; continuous proves none of this silently rots after a model update. Engineering nuance: keep deterministic logic *out* of the LLM, then test it with normal unit tests.
**Transition:** "Each layer has a tool. Here's the toolbox."

## Slide 11 — Testing tools *(subsection divider)*
**Say:** Signal the shift from strategy to tooling. Frame tools as an end-to-end workflow, not a feature list; deep-dive the ones with demos.

## Slide 12 — The Agentforce testing toolbox
**Key message:** Eight methods grouped into four evidence layers that line up with the release train.
**Say:** Discover & build — manual exploration surfaces risks; previews give the fastest authoring loop. Component-test & regress — Apex/Flow give deterministic assertions on the tools, Testing Center makes findings repeatable and regression-grade. Evaluate conversation & channel — ACT validates multi-turn outcome & state; Playwright proves the customer-facing channel. Accept & operate (highlighted) — UAT is business sign-off, production verification is released-system health. One-breath strengths/limits: previews are fast but have no memory; Testing Center is repeatable but sandbox-only and consumes credits; Playwright is realistic but slower and flakier.
**Transition:** "Let's start at the top of the funnel — manual exploration, live."

## Slide 13 — Manual exploration *(+ Demo 1)*
**Key message:** Preview is your fastest feedback loop and your weakest memory — it finds problems, it doesn't prove their absence.
**Say:** Simulation isolates from org data (use while instructions churn); live runs real actions against sandbox data (use before you commit a version). Read the reasoning trace every time: subagent → action inputs → outputs → final response. CLI path: `sf agent preview --api-name Service_Agent` (add `--use-live-actions`).
**Demo 1 (~90s):** see runbook. Close with: "That misroute is now a test case."
**Transition:** "Hand-testing doesn't scale. We need hundreds of cases, scored."

## Slide 14 — Batch / bulk testing *(+ Demo 2)*
**Key message:** One suite, hundreds of utterances, a scored pass/fail grid comparable across versions.
**Say:** Three ways to create cases (AI-generated, Q&A from knowledge, your own CSV/YAML); each case asserts expected subagent, actions and outcome; scorers cover accuracy, completeness, coherence, conciseness, latency, instruction adherence. **Guardrail:** runs consume requests/credits and can modify CRM data — sandboxes only. **Tests as code:** the YAML spec becomes `AiEvaluationDefinition` metadata, versioned and deployed with the agent; `junit` output is what CI dashboards read.
**Demo 2 (~2 min):** see runbook. Say: "AI-generated cases are a starting point — review them like code. They come out polite and well-formed; real customers don't."
**Transition:** "Batch covers single turns. Real chats have many."

## Slide 15 — Agentforce Conversational Testing (ACT) *(slide only)*
**Key message:** Real chats have more than one message — does the agent remember, and does it recover?
**Say:** Distinguish three tools: Testing Center's **Conversation History** column (earlier turns in, next reply checked; last turn must be the agent); **ACT**, which simulates a full multi-turn dialogue with a synthetic persona; and the **Agent API harness** for long/branching scripts, custom LLM-as-judge scoring, or load (needs an External Client App, client-credentials flow). Design personas like real people — frustrated customer, non-native speaker, someone who changes their mind. Measure **turns-to-resolution**, not just pass/fail.
**Optional verbal demo cue:** "remember my name" with memory on (both turns pass) vs off (turn 2 fails).
**Transition:** "Even a perfect brain fails if the customer can't see the answer. Enter Playwright."

## Slide 16 — Playwright & real-channel testing *(+ Demo 3)*
**Key message:** Testing Center checks the brain; Playwright checks what the customer actually sees — iframe rendering, rich content, handoff, file upload.
**Say:** Assertion philosophy is the lesson — **assert loosely on the agent's wording** (regex/keywords, because it's non-deterministic), **strictly on UI state** (screenshots, visibility, DOM). Enhanced Chat renders in an iframe — capture the exact selector with `npx playwright codegen`.
**Demo 3 (~90s):** see runbook. This is the flakiest demo — the one to drop if you're behind (keep the slide).
**Transition:** "Tools are necessary but not sufficient — coverage is a design problem."

## Slide 17 — Designing effective tests *(subsection divider)*
**Say:** Pivot from "which tool" to "what to test." Counter the trap: teams measure coverage by number of prompts instead of diversity of scenarios, personas, data and outcomes.

## Slide 18 — Building effective agent test scenarios
**Key message:** Good coverage is not more prompts — it is systematic variation across **scenario, persona, data, outcome**.
**Say:** Walk the four dimensions with WISMO — Scenario (the ambiguous "it's late", the unsupported "change my delivery address"); Persona (logged-in vs anonymous, non-native speaker, someone who must be *denied* another customer's order); Data (no match, one match, many matches, stale status, boundary values); Outcome (right action, safe refusal, clarification, escalation). Give the starting recipe so they leave with a number: **5 happy / 3 edge / 2 negative per subagent**, varying tone/length/typos/language, each suite run more than once. The boundary trio: the allowed request, the denied request, the manipulated request.
**Transition:** "Let's lock in the principles with a quick knowledge check."

## Slide 19 — Knowledge check
**Run as a poll, not a lecture.** Let the room answer in chat, reveal, give the one-line why.
1. **Why not assert an exact string?** → Replies are non-deterministic. *Assert on topic, action & meaning instead.*
2. **Why `System.runAs(agentUser)`?** → Test with the agent's real permissions. *The #1 silent failure: works for admin, not the agent user.*
3. **Where do Testing Center runs happen?** → Sandboxes only. *Runs consume credits and can modify CRM data.*
4. **Model update, no code change — what catches a regression?** → Scheduled runs + production monitoring. *Agents drift without a commit.*
5. **Which tool checks what the customer sees?** → Playwright. *Testing Center checks the brain; Playwright checks the rendered channel.*
**Close** on the two take-home lines, then open the floor.

### Likely open-floor questions — have crisp answers ready
- *"How many test cases is enough?"* → Start 5 happy / 3 edge / 2 negative **per subagent**; grow from real failures.
- *"How do we handle flaky results?"* → Run each case N times, pass at a threshold (e.g. 4/5); track the trend, not one run.
- *"Blocking gate from day one?"* → No — non-blocking ~2 weeks, then blocking once the team trusts the numbers.
- *"Scratch orgs for agents?"* → Usually no — use sandboxes; scratch orgs often lack Agentforce/Data Cloud provisioning.
- *"Deployment in one line?"* → An agent is linked metadata (`AiAuthoringBundle` draft → `Bot`/`GenAiPlannerBundle` runtime). Validate first, quick-deploy in the window, then publish & activate; Data Cloud knowledge moves as a **separate data-kit path**.
