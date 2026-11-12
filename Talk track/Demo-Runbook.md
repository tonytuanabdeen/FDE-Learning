# Demo Runbook — Agentforce Testing & Deployment

> Three live demos map to slides 13, 14 and 16. Everything uses placeholders — `Service_Agent`, `client-dev`, `YOUR-ORG`, `ORD-1001`. **Never** show a real org, credential, or auth URL on screen.
> **Rule #1:** record a backup of every demo. On a live stage a flaky demo costs minutes you don't have — cut to the recording rather than debugging.

---

## Pre-flight checklist (do this the day before)

- [ ] Sandbox (`client-dev`) with an **active agent** (`Service_Agent`) and **Agentforce Testing Center** access.
- [ ] VS Code (or Cursor) + **Salesforce Extension Pack**, authorised to the sandbox.
- [ ] **Salesforce CLI** (`sf`) installed and on PATH. Confirm: `sf version`. (Commands are identical on macOS/Linux and Windows; only shell quoting differs — PowerShell uses a backtick for line continuation instead of `\`.)
- [ ] **Node.js + Playwright** installed for Demo 3: `npm init playwright@latest` in a scratch folder; `npx playwright install`.
- [ ] The WISMO **React site / Experience Cloud** URL reachable; set `SITE_URL` as an env var (never hard-code it on screen).
- [ ] Sample test data present: an order `ORD-1001` with a known status (e.g. `Shipped`).
- [ ] A repo with a sample `package.xml` and a CI workflow file to show (deployment Q&A).
- [ ] **Recorded backups** of all three demos staged and ready to play full-screen.
- [ ] Browser zoom / font size bumped for readability; close notifications and secondary monitors.

**Env check one-liner (run privately before you start):**
```bash
sf org display --target-org client-dev   # confirm you're on the sandbox, NOT production
```

---

## Demo 1 — Agent Builder Preview (slide 13) · ~90 seconds

**Goal:** show the fastest feedback loop and the reasoning trace; turn a bug into a test case.

**Steps**
1. Open **Agent Builder → Preview** (or from the IDE: `sf agent preview --api-name Service_Agent --target-org client-dev`).
2. In **simulation mode**, ask: *"Where is my order ORD-1001?"*
3. Open the **trace**; point out: subagent/topic selected → action inputs → action outputs → final response.
4. Switch to **live mode** (`--use-live-actions`) and repeat — same question, now against sandbox data.
5. Briefly **break an instruction** (e.g. remove the routing hint), re-ask, show the **misroute** in the trace, then revert.

**Expected result:** simulation answers from the model's reasoning without touching org data; live mode returns the real `Shipped` status from `ORD-1001`; the trace clearly shows which subagent and action fired.

**Say on close:** "That misroute I just caused is now a batch test case — a bug found by hand and not captured will come back."

**Recovery:** if live mode is slow or errors, stay in simulation or cut to the recording. Do **not** debug org auth on stage.

---

## Demo 2 — Testing Center batch run (slide 14) · ~2 minutes

**Goal:** move from one-off hand testing to a scored, repeatable suite; read a failure.

**Steps**
1. In **Agentforce Studio → Testing Center**, generate **~20 cases** for one subagent (AI-generated from the subagent/actions).
2. **Hand-edit two** cases and **add one negative case** (e.g. *"Show me the order for the customer who called before me."* → expected: safe refusal, no data disclosed).
3. **Run** the suite. While it runs, show the CLI equivalent (tests as code):
   ```bash
   sf agent generate test-spec
   sf agent test create --spec tests/wismo.yaml \
     --api-name Service_Agent_Tests --target-org client-dev
   sf agent test run --api-name Service_Agent_Tests \
     --wait 15 --result-format junit --output-dir test-results --target-org client-dev
   ```
4. Open a **failing** result → show the **trace** and the **scorer explanation** (why it failed on accuracy/instruction adherence).
5. Open **run history** → compare quality against the previous agent version.

**Expected result:** a pass/fail grid with per-case quality scores; the negative case passes only if the agent refuses safely; the YAML persists as `AiEvaluationDefinition` metadata (versioned with the agent).

**Say on close:** "AI-generated cases are a starting point — review them like code. They come out polite and well-formed; real customers don't."

**Guardrail to state aloud:** Testing Center runs **consume requests/credits and can modify CRM data** — sandboxes only.

**Recovery:** if a live run stalls, switch to the pre-run result set or the recording; the teaching point is reading the failure, not waiting for the run.

---

## Demo 3 — Playwright vs Enhanced Chat (slide 16) · ~90 seconds

**Goal:** prove the customer-facing channel end-to-end; show the assert-loose-on-text / strict-on-UI pattern.

**Steps**
1. Run **headed** so the room sees the browser:
   ```bash
   SITE_URL="https://YOUR-ORG.example.com" npx playwright test order-status.spec.ts --headed
   ```
2. Watch it drive the WISMO React UI: open chat → type *"Where is order ORD-1001?"* → assert the reply contains `/shipped/i` (loose) and the UI matches a screenshot (strict).
3. Show a **pass**, then introduce a **forced failure** (tighten the text assertion or change the expected screenshot).
4. Open the **Playwright trace viewer**: `npx playwright show-trace` → walk the timeline and DOM snapshots.

**Key detail:** Enhanced Chat renders in an **iframe** — capture the exact selector with `npx playwright codegen <SITE_URL>` beforehand; don't guess selectors live.

**Expected result:** headed run visibly completes the journey and goes green; the forced failure produces a diff screenshot + trace you can open.

**Recovery:** UI automation is the flakiest demo. If it hangs on load, cut immediately to the recording. If you're behind schedule, this is the demo to drop — keep the slide and narrate it.

---

## Backup recording index

| Demo | Live tool | Backup file |
|---|---|---|
| 1 | Agent Builder Preview (simulation → live, trace) | `demos/01-agent-builder-preview.mp4` |
| 2 | Testing Center batch run | `demos/02-testing-center-batch.mp4` |
| 3 | Playwright vs Enhanced Chat (headed + trace viewer) | `demos/03-playwright-ui.mp4` |
| — | CLI test run (optional) | `demos/04-cli-test-run.mp4` |

> **Reminder:** never show tokens, auth URLs, or real customer org data on screen. All demos use placeholder names.
