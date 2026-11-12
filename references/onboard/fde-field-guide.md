# FDE field guide

**From a new laptop to a client handover.**

A field guide for forward deployed engineers working on Salesforce and Agentforce with Claude Code. Work through tracks 1 and 2 once; use tracks 3 and 4 as ongoing reference.

> This document was generated from `fde-field-guide.html`. The interactive version supports per-OS commands (macOS/Linux vs Windows), search, progress tracking, and an integration-pattern picker. Where commands differ by OS, both are shown below.

**Team values** (edit these in the HTML `TEAM` block before handing the guide to new joiners — shown here with their placeholder defaults):

| Key | Value |
|---|---|
| Help channel | `#fde-help` |
| Skills repo | `https://github.com/YOUR-ORG/fde-claude-skills` |
| Project template | `https://github.com/YOUR-ORG/fde-project-template` |
| Handover owner | `your.name@company.com` |
| Security contact | `security@your-company.com` |

---

## 1. Set up your machine

*VS Code, Salesforce CLI, Claude Code*

Work through this once, top to bottom. It takes about half a day, most of it waiting for installs. Finish with the smoke test so you know everything works before your first project.

**Time:** about 3 to 4 hours. **Needs:** admin rights on your laptop, a GitHub account, a Salesforce sandbox login.

### Foundations

Everything else sits on top of these four tools.

#### Install Git, Node.js, a JDK and the GitHub CLI

Node runs the Salesforce CLI, LWC tests and Playwright. A JDK (17 or 21) is required by the Apex language server and Code Analyzer.

Install (macOS / Linux):

```bash
brew install git node@22 gh
brew install --cask temurin@21
```

Install (Windows):

```powershell
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install GitHub.cli
winget install EclipseAdoptium.Temurin.21.JDK
```

Verify:

```bash
git --version
node --version
java -version
gh --version
```

> **Tip:** On macOS without Homebrew, install it first from brew.sh. On Windows, open a new terminal after installing so the PATH refreshes.

#### Set up Git identity, SSH key and GitHub login

Use your work email so commits are attributed correctly. Sign in to GitHub once with the CLI and let it upload the SSH key.

Configure:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@company.com"
git config --global init.defaultBranch main
git config --global pull.rebase true
ssh-keygen -t ed25519 -C "you@company.com"
gh auth login
```

> **Careful:** Never commit auth files, .env files or org auth URLs. You will set up .gitignore rules in track 2, but build the habit now.

### Editor

One editor profile for everything: Apex, LWC, Playwright and Claude Code.

#### Install VS Code and the extensions

Install VS Code from code.visualstudio.com, then enable the "code" shell command (Command Palette, "Shell Command: Install code command in PATH") and run this block.

Extensions:

```bash
code --install-extension salesforce.salesforcedx-vscode
code --install-extension salesforce.sfdx-code-analyzer-vscode
code --install-extension anthropic.claude-code
code --install-extension ms-playwright.playwright
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension eamodio.gitlens
code --install-extension bierner.markdown-mermaid
code --install-extension redhat.vscode-yaml
```

- Salesforce Extension Pack covers Apex, LWC, SOQL builder, org browser and Apex Replay Debugger.
- Code Analyzer flags security and quality issues in Apex and LWC before a reviewer does.
- Playwright extension lets you run and record UI tests from the editor.

#### Apply the recommended workspace settings

Put these in your user settings (Command Palette, "Preferences: Open User Settings (JSON)").

`settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "salesforcedx-vscode-core.show-cli-success-msg": false,
  "salesforcedx-vscode-apex.java.home": ""
}
```

> **Tip:** If Apex features do not start, set salesforcedx-vscode-apex.java.home to your JDK folder (the value of JAVA_HOME).

### Salesforce CLI

The sf command is how you deploy, test and automate everything.

#### Install the Salesforce CLI (sf)

Install the current CLI. Do not install the old sfdx v7 package alongside it.

Install and verify:

```bash
npm install --global @salesforce/cli
sf --version
sf update
```

#### Log in to your first sandbox with a clear alias

Use a client prefix plus the environment name. Never make production your default org.

Authorize:

```bash
sf org login web --alias client-dev --instance-url https://test.salesforce.com --set-default
sf org list
sf org display --target-org client-dev
```

- Aliases: client-dev, client-sit, client-uat, client-prod.
- Sandboxes log in at test.salesforce.com. Production and Developer Edition use login.salesforce.com (the default).
- Auth tokens expire. If you see an expired token error, just log in again.

> **Careful:** sf org display --verbose prints a secret auth URL. Do not paste its output into chat, tickets or Claude prompts.

#### Install Code Analyzer and check the agent commands

Code Analyzer runs static analysis from the terminal and in CI. The agent commands are what you will use to test Agentforce agents in track 3.

Plugins:

```bash
sf plugins install code-analyzer
sf code-analyzer run --workspace force-app --view table
sf agent --help
sf agent test --help
```

> **Tip:** Agentforce CLI commands are evolving quickly. If sf agent test is missing, run sf update first, then check the release notes for the plugin.

#### Optional: create a scratch org

Only if the project uses scratch orgs and you have access to a Dev Hub.

Scratch org:

```bash
sf org login web --alias devhub --set-default-dev-hub
sf org create scratch --definition-file config/project-scratch-def.json --alias scratch1 --duration-days 7 --set-default
```

### Claude Code

Your AI pair engineer, inside the terminal and VS Code.

#### Install Claude Code and sign in

Use the account your company approved. The first run opens a browser to log in.

Install (macOS / Linux):

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
claude
```

Install (Windows):

```powershell
irm https://claude.ai/install.ps1 | iex
claude --version
claude
```

Alternative via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

Health check:

```bash
claude doctor
```

> **Careful:** Company policy: conversations are retained and may be reviewed by administrators. Do not paste real customer data, secrets or credentials. Use placeholders such as CUSTOMER_1.

#### Connect Claude Code to VS Code

Install the Claude Code extension (done above), then open the integrated terminal in your project and run claude. The extension also adds a side panel with diff views.

In a Claude Code session:

```
/ide
/status
```

- Selected lines and open files are shared with Claude automatically.
- Edits appear as diffs in the editor, so you review before accepting.

#### Add Salesforce skills to Claude Code

Skills are folders with a SKILL.md that teach Claude how your team does specific jobs (Apex, LWC, Flow, deploys). They load only when relevant, so they cost very little context.

Option A: install from the team marketplace:

```
/plugin marketplace add YOUR-ORG/fde-claude-skills
/plugin install salesforce-skills@fde-claude-skills
/plugin list
```

Option B: copy skills by hand (personal, all projects) — macOS / Linux:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/YOUR-ORG/fde-claude-skills /tmp/fde-skills
cp -R /tmp/fde-skills/skills/* ~/.claude/skills/
ls ~/.claude/skills
```

Option B: copy skills by hand (personal, all projects) — Windows:

```powershell
mkdir $HOME\.claude\skills -Force
git clone https://github.com/YOUR-ORG/fde-claude-skills $HOME\fde-skills
Copy-Item $HOME\fde-skills\skills\* $HOME\.claude\skills -Recurse -Force
dir $HOME\.claude\skills
```

- Recommended starter set: Apex (bulkification, triggers, tests), LWC, Flow, SOQL and data, metadata deploy, Agentforce agent design, and testing.
- Project-specific skills go in the repo at .claude/skills. Personal skills go in ~/.claude/skills.
- Ask in a session "What skills do you have available?" to confirm they loaded.

> **Careful:** A skill can instruct Claude to run commands. Only install skills from your team repo or sources you have read. Open the SKILL.md before you trust it.

> **Tip:** The repo URL and marketplace name above are placeholders. Replace SKILLS_REPO with the URL set in TEAM at the top of this file, and ask your lead for the approved list.

#### Connect the Salesforce DX MCP server

Lets Claude query orgs, read metadata and run tests through a structured tool instead of guessing shell commands.

Add for this machine:

```bash
claude mcp add salesforce -- npx -y @salesforce/mcp --orgs DEFAULT_TARGET_ORG --toolsets orgs,metadata,data,users
claude mcp list
```

> **Tip:** Limit it to sandboxes and only the toolsets you need. Check the Salesforce DX MCP docs for current flag names, as they can change between versions.

#### Write your personal CLAUDE.md

~/.claude/CLAUDE.md applies to every project. Keep it short and about you, not the client.

`~/.claude/CLAUDE.md`:

```md
# About me
- Forward deployed engineer working mostly on Salesforce and Agentforce.
- Explain trade-offs briefly, then recommend one option.

# Working style
- Plan first for anything touching more than 3 files.
- Show me the diff before committing. Small commits with clear messages.
- Never run deploys to an org or push to GitHub without asking.
- Never include real customer data in files, commands or search queries.
```

### Test tooling and extras

Set these up now so they are ready on day one of a project.

#### Install Playwright browsers

Used for UI automation in track 3. Install the browser once per machine.

Install:

```bash
npx playwright install --with-deps chromium
npx playwright --version
```

#### Install the handy extras

- Salesforce Inspector Reloaded (Chrome extension): inspect fields, run SOQL, export data.
- Bruno or Postman: test REST callouts and Salesforce APIs.
- jq: parse the JSON that sf and Playwright produce.
- Draw.io or the Mermaid preview in VS Code: architecture diagrams.
- Data Loader or sf data commands: bulk data work.

jq — macOS / Linux: `brew install jq` · Windows: `winget install jqlang.jq`

#### Run the smoke test

If every line prints a version or status, you are ready. Fix anything that fails before moving on.

Smoke test:

```bash
git --version && node --version && java -version
sf --version && sf org list
gh auth status
claude --version
npx playwright --version
code --list-extensions | grep -E "salesforce|claude|playwright"
```

> **Tip:** Stuck? Post the error text (not screenshots of secrets) in #fde-help.

---

## 2. Start a project well

*Repo, CLAUDE.md, project skills*

Do this in the first two days of an engagement, before feature work starts. A good starting setup means Claude, your teammates and your future self all understand the project the same way.

**Time:** about half a day per project. **Output:** a repo with CI, a CLAUDE.md, project skills and a decision log.

### Repository foundation

Create it once and make it hard to break.

#### Create the project and the GitHub repo

Start from the team template if one exists. Otherwise generate a standard DX project.

Scaffold:

```bash
sf project generate --name acme-fde --template standard --manifest
cd acme-fde
git init -b main
gh repo create YOUR-ORG/acme-fde --private --source . --remote origin
git add . && git commit -m "chore: initial project scaffold"
git push -u origin main
```

> **Tip:** Team template: https://github.com/YOUR-ORG/fde-project-template (placeholder). Using it gives you the folders, CI, PR template and CLAUDE.md skeleton in one go.

#### Add a safe .gitignore

`.gitignore`:

```gitignore
# Salesforce local state
.sf/
.sfdx/
.localdevserver/
.vscode/settings.json

# Secrets and sessions
.env
.env.*
auth*.txt
.auth/

# Node and test output
node_modules/
reports/
playwright-report/
test-results/

# Claude Code local-only settings
.claude/settings.local.json
```

#### Agree the branching and pull request rules

- Short-lived branches from main, named feature/TICKET-123-short-name.
- Protect main: pull request required, one approval, CI must pass, no force pushes.
- Small pull requests. If a PR needs a long explanation, split it.
- Use a PR template that asks for: what changed, how it was tested, deploy notes, rollback.

`.github/pull_request_template.md`:

```md
## What changed

## How it was tested
- [ ] Apex tests
- [ ] LWC Jest
- [ ] Agent tests
- [ ] Playwright

## Deploy notes
(manual steps, data changes, permission sets)

## Rollback plan
```

#### Add a validation check to every pull request

The pipeline authenticates to a sandbox, validates the deployment and runs local tests. The auth URL is stored as a GitHub secret, never in the repo.

Get the auth URL once (keep it private):

```bash
sf org display --target-org client-dev --verbose --json | jq -r .result.sfdxAuthUrl
gh secret set SFDX_AUTH_URL_DEV
```

`.github/workflows/validate.yml`:

```yaml
name: validate
on:
  pull_request:
    branches: [main]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm install --global @salesforce/cli
      - name: Authenticate
        run: |
          echo "${{ secrets.SFDX_AUTH_URL_DEV }}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias ci-org
          rm auth.txt
      - name: Validate deployment
        run: sf project deploy validate --source-dir force-app --target-org ci-org --test-level RunLocalTests --wait 60
```

> **Tip:** Prefer a dedicated integration user and JWT login for shared pipelines. The auth URL approach is fine for a first iteration.

### Claude Code project setup

Commit these files so the whole team gets the same Claude behaviour.

#### Write the project CLAUDE.md

Claude reads this at the start of every session. Keep it under about 100 lines: commands, structure, conventions and hard rules. Update it whenever you correct Claude twice about the same thing.

`CLAUDE.md`:

```md
# Project: ACME service transformation

## Context
- Goal: deflect 30% of order-status cases with an Agentforce agent.
- Clouds: Service Cloud, Experience Cloud, Data Cloud. Integration: order API via Named Credential.

## Orgs
- client-dev: sandbox, default target
- client-sit, client-uat: sandboxes, deploy only via pipeline
- client-prod: READ ONLY. Never deploy, never run DML.

## Layout
- force-app/main/default: metadata
- specs/agent: Agentforce test specs
- tests/e2e: Playwright tests
- docs: ADRs (docs/adr), HANDOVER.md

## Commands
- Validate: sf project deploy validate --source-dir force-app --target-org client-dev --test-level RunLocalTests
- Apex tests: sf apex run test --target-org client-dev --test-level RunLocalTests --code-coverage --result-format human --wait 30
- LWC tests: npm run test:unit
- Agent tests: sf agent test run --api-name Order_Agent_Regression --target-org client-dev --wait 15
- UI tests: npx playwright test

## Conventions
- Apex: one trigger per object, logic in handler classes, bulk-safe, no SOQL or DML in loops, 85% coverage target.
- LWC: small components, no hardcoded IDs, wire adapters over imperative calls where possible.
- Names: Acme_ prefix for custom metadata, verbs for Apex actions (GetOrderStatus).

## Rules
- Never commit secrets, auth URLs or customer data. Use placeholders like CUSTOMER_1.
- Ask before deploying to any org or pushing to GitHub.
- Update docs/HANDOVER.md when architecture changes.
- Record any significant design choice as an ADR in docs/adr.
```

#### Set shared permissions in .claude/settings.json

Allow the safe, frequent commands. Ask before anything that changes an org or the remote. Deny anything that touches secrets.

`.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(sf org list:*)",
      "Bash(sf apex run test:*)",
      "Bash(sf project deploy validate:*)",
      "Bash(sf agent test:*)",
      "Bash(npx playwright test:*)",
      "Bash(npm run test:unit:*)"
    ],
    "ask": [
      "Bash(sf project deploy start:*)",
      "Bash(git push:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./.auth/**)",
      "Bash(rm -rf:*)"
    ]
  }
}
```

> **Tip:** Personal overrides go in .claude/settings.local.json, which stays out of git. Hooks (for example, auto-format after edits) are also configured here. See the Claude Code docs on hooks.

#### Create project-specific skills

Turn anything you explain twice into a skill. Start with these three: validate-deploy, release-notes and the handover skill in track 3.

`.claude/skills/validate-deploy/SKILL.md`:

```md
---
name: validate-deploy
description: Validate the current branch against the dev sandbox with local tests and summarise failures. Use before opening a pull request or when asked to check the build.
---

# Validate deploy

1. Run git status and confirm the working tree is what the user expects.
2. Run: sf project deploy validate --source-dir force-app --target-org client-dev --test-level RunLocalTests --wait 60
3. If it fails, group errors by component and by cause (compile, test failure, coverage, missing dependency).
4. Propose the smallest fix for each group. Do not apply fixes without confirmation.
5. Finish with a three-line summary: result, failing components, next step.
```

`.claude/skills/release-notes/SKILL.md`:

```md
---
name: release-notes
description: Draft client-friendly release notes from merged pull requests and git history since the last tag.
---

# Release notes

1. Find the last tag with git describe --tags --abbrev=0.
2. List commits and merged PRs since that tag.
3. Group into: New, Improved, Fixed, Needs attention (manual steps).
4. Write in plain language for a business reader. No class or field API names in headlines.
5. Save to docs/releases/ with the date in the filename.
```

- The description is what triggers the skill, so say when to use it.
- Keep SKILL.md short. Put long reference material in a separate file in the same folder and link to it.

#### Share project MCP servers with the team

Project scope:

```bash
claude mcp add salesforce --scope project -- npx -y @salesforce/mcp --orgs client-dev --toolsets orgs,metadata,data
cat .mcp.json
```

> **Careful:** Point shared MCP servers at sandboxes only. Never at production.

### Org strategy and discovery

Decide these early. They are painful to change later.

#### Inventory the orgs and pull a baseline

Know which orgs exist, who owns them, and what is in them before you change anything.

Baseline:

```bash
sf project generate manifest --from-org client-dev --output-dir manifest
sf project retrieve start --manifest manifest/package.xml --target-org client-dev
git add . && git commit -m "chore: baseline metadata from client-dev"
```

- Write the org list, owners and refresh schedule into CLAUDE.md and the README.
- Agree who can deploy to UAT and production, and how.

#### Run the technical kickoff checklist

- Success measures: what number moves, and by when?
- Current state: orgs, clouds, installed packages, existing automations and technical debt.
- Integrations: systems, owners, auth method, rate limits, sandboxes available.
- Data: sources, volumes, quality, retention, masking in sandboxes.
- Security: sharing model, field-level security, compliance constraints, where AI may touch data.
- Delivery: environments, release cadence, change approval, who signs off.
- People: client counterparts, decision makers, escalation path.

#### Start the decision log (ADRs)

One short file per significant decision. It becomes the best part of your handover later.

`docs/adr/0001-use-platform-events-for-order-updates.md`:

```md
# 1. Use platform events for order updates

Date: 2026-01-15
Status: Accepted

## Context
Orders change in the ERP and Salesforce must reflect updates within a minute.

## Options considered
1. Polling with a scheduled job: simple, but delayed and wasteful.
2. Platform events published by middleware: near real time, decoupled.
3. Direct callout on page load: always fresh, but slow and rate limited.

## Decision
Option 2.

## Consequences
- Need replay handling and monitoring for event delivery.
- Middleware team owns the publisher.
```

#### Agree the data handling rules

- Customer data stays in the client org. It does not go into prompts, tickets or screenshots.
- Use masked or synthetic data in sandboxes. Use placeholders (CUSTOMER_1, ACCT_XXXX) when asking Claude for help.
- Test data comes from scripts you can re-run, not copies of production.
- If you think data was exposed, stop and contact security@your-company.com. Do not investigate it yourself.

---

## 3. Design, hand over, test

*Architecture, handover docs, Apex, agent and Playwright testing*

This is where you move from building features to owning outcomes: designing solutions the client can run, documenting them so the next person is productive in a day, and proving they work with repeatable tests.

**Time:** ongoing. Start with the testing setup in your first sprint, because everything else gets easier with it.

### Architecture design

Think on paper first. Claude is good at drafting and challenging, you own the decisions.

#### Follow a design workflow

- Clarify the outcome and constraints (volumes, latency, security, who operates it).
- Draw the context: users, Salesforce clouds, external systems, data flows.
- Design the data model and the security model before any automation.
- Choose integration patterns per flow (use the picker below).
- For agents: define topics, actions, instructions, guardrails and escalation.
- List risks and non-functional needs: limits, error handling, monitoring, rollback.
- Write ADRs for each real decision. Review with a peer before building.

> **Tip:** Use Claude in plan mode (Shift+Tab twice) for design. It explores your repo read-only and proposes a plan, and you approve before anything changes.

#### Prompt: draft a solution architecture

Prompt template:

```
I need a solution architecture for this requirement:
[paste requirement, using placeholders for customer names]

Constraints: [volumes, latency, security, release cadence, licences]
Existing context: read CLAUDE.md, docs/adr and force-app before answering.

Produce:
1. Context and assumptions (list anything you are guessing)
2. Data model changes (objects, fields, relationships, sharing)
3. Integration approach per flow, with the pattern and why
4. Automation split (declarative vs Apex vs LWC) with reasons
5. Governor limit and scalability risks
6. Security and data privacy considerations
7. Two alternatives you rejected and why
8. Open questions for the client
9. A Mermaid diagram of the main flow

Do not write code yet.
```

#### Diagrams as code with Mermaid

Diagrams that live in the repo stay up to date because Claude can edit them. Preview in VS Code with the Mermaid extension.

`docs/diagrams/order-status.mmd`:

```
sequenceDiagram
  actor Customer
  participant Chat as Agentforce agent
  participant Flow as Apex action GetOrderStatus
  participant NC as Named Credential
  participant ERP as Order API
  Customer->>Chat: Where is my order?
  Chat->>Flow: orderNumber
  Flow->>NC: GET /orders/{id}
  NC->>ERP: authenticated call
  ERP-->>Flow: status, ETA
  Flow-->>Chat: structured result
  Chat-->>Customer: Plain language answer
  Note over Chat: Escalate to a human if order not found twice
```

#### Agent design canvas (Agentforce)

Fill this in before you open Agent Builder. It becomes the source for your test cases.

`docs/agent-design.md`:

```md
# Agent: Order Support

## Purpose
One sentence on the job the agent does and for whom.

## Topics
| Topic | Scope (what it handles) | Out of scope |
|---|---|---|
| order_status | Where is my order, delivery estimate | Changing an address |
| returns | Start a return, explain policy | Refund exceptions |

## Actions
| Action | Type | Inputs | Outputs | Error handling |
|---|---|---|---|---|
| GetOrderStatus | Apex invocable | orderNumber | status, eta | not found, timeout |

## Instructions and guardrails
- Tone, language, what to never say.
- Never reveal data for an order the verified customer does not own.

## Escalation
- When and how to hand off to a human, with what context.

## Grounding data
- Knowledge articles, Data Cloud objects, fields in scope.

## Test plan
- 3+ utterances per topic, plus off-topic, adversarial and ambiguous inputs.
```

#### Integration pattern picker

Pick what you need to do. This is a starting point for the conversation, not a replacement for design.

| You need to... | Pattern | Approach | Watch for |
|---|---|---|---|
| Show external data inside Salesforce in real time | **Callout with a Named Credential** | Call the API from Apex or an External Service, authenticated by a Named Credential. Cache what you can. For data you never want to copy, consider External Objects or Data Cloud zero-copy. | Watch callout limits and timeouts. Never callout from a trigger synchronously. |
| Tell another system when Salesforce data changes | **Change Data Capture or Platform Events** | Use CDC for record changes with minimal build effort. Use custom Platform Events when you need a business-level message with a defined payload. | Plan for replay, event volume allocations and consumer monitoring. |
| Receive updates from another system | **Platform Events, Salesforce APIs or Apex REST** | Prefer the standard REST or Composite APIs through a connected app or external client app. Publish Platform Events when the sender should not wait. Use Apex REST only for custom logic. | Authenticate with a dedicated integration user and least-privilege permission sets. |
| Load or sync large volumes | **Bulk API 2.0 or middleware** | Use Bulk API 2.0 for large batch loads and extracts. Use an integration platform if you need transformation, retries and monitoring. | Agree on a schedule and an external ID for upserts. |
| Long-running or heavy processing | **Queueable or Batch Apex, with an event on completion** | Move the work out of the user transaction. Queueable for chained jobs, Batch Apex for large data sets. Publish a Platform Event when done so the UI or agent can react. | Design for idempotency. Jobs can retry. |
| Let an agent act on a back-end system | **Invocable Apex or Flow action with a Named Credential** | Expose a narrow action with typed inputs and outputs. Keep the logic in Apex or Flow, not in the prompt. Return structured errors the agent can explain. | Enforce record access in the action, not just in agent instructions. |

### Technical handover document

Handover is a deliverable, not an afterthought. Generate the first 80 percent from the repo, then edit.

#### What a good handover contains

- Overview: business goal, scope, what is live and what is not.
- Architecture: context diagram, data model, integration flows, key ADRs.
- Component inventory: apex, flows, LWCs, agents, permission sets, with owner and purpose.
- Configuration and secrets: where they live (never the values), how to rotate them.
- Environments and deployment: orgs, pipeline, manual steps, rollback.
- Test evidence: latest results for Apex, agent and UI tests with links.
- Runbook: monitoring, common failures, who to call.
- Known issues, technical debt and recommended next steps.
- Access: who has which roles, how to request access.

#### Create a handover skill

`.claude/skills/handover/SKILL.md`:

```md
---
name: handover
description: Generate or refresh docs/HANDOVER.md, the technical handover document, from the repo, metadata, ADRs and latest test reports. Use at sprint end, go-live, or when an engineer rolls off the project.
---

# Technical handover

Read first: CLAUDE.md, docs/adr/*, docs/agent-design.md, reports/** (latest results), git log for the last 30 days.

Write docs/HANDOVER.md with these sections, in order:
1. Overview (goal, scope, status)
2. Architecture (embed Mermaid diagrams from docs/diagrams)
3. Data model (objects and fields we added or changed)
4. Component inventory (table: type, API name, purpose, owner, test coverage)
5. Integrations (system, direction, auth method, Named Credential name, error handling)
6. Agents (topics, actions, guardrails, test results summary)
7. Environments and deployment (orgs, pipeline, manual steps, rollback)
8. Test evidence (pass/fail counts and coverage from reports/, with the report dates)
9. Runbook (monitoring, common failures, escalation)
10. Known issues and next steps
11. Open questions

Rules:
- Facts must come from the repo or reports. If you cannot verify something, add it under Open questions.
- Never write secrets, auth URLs or real customer data. Name where they are stored instead.
- Keep tables for inventories and prose for reasoning.
- End with a "Last generated" line with the date and the commit hash.
```

Generate it:

```bash
claude -p "Use the handover skill to refresh docs/HANDOVER.md" --permission-mode acceptEdits
```

> **Tip:** Run it at the end of every sprint, not only at the end of the project. Review the diff like code. Treat anything marked Open questions as your to-do list.

#### Review checklist before you hand it over

- A new engineer can deploy to a sandbox using only the document.
- Every integration lists its owner and credential location.
- Test evidence is dated and links to real reports.
- No secrets or customer data anywhere in the file.
- The handover owner (your.name@company.com) has read it end to end.

### Backend testing: Apex and LWC

Fast tests that run on every pull request.

#### Test strategy at a glance

- Many Apex and LWC unit tests: fast, run on every PR.
- A smaller set of agent tests: run the agent against known utterances.
- A few UI tests with Playwright: cover the most important journeys only.
- Manual exploratory testing for what automation cannot judge, such as tone and layout.

#### Run Apex tests and produce results files

JUnit XML plugs into CI dashboards. The JSON file is easy for Claude and scripts to summarise.

Apex with coverage:

```bash
sf apex run test --target-org client-dev --test-level RunLocalTests --code-coverage --result-format junit --output-dir reports/apex --wait 30
sf apex run test --target-org client-dev --test-level RunLocalTests --code-coverage --result-format json --output-dir reports/apex-json --wait 30
```

- Production deployments need at least 75 percent org-wide coverage. Aim for 85 percent and meaningful assertions, not coverage for its own sake.
- Create data in @TestSetup methods or a test data factory. Never use SeeAllData=true.

#### Run LWC Jest tests

LWC:

```bash
npm install --save-dev @salesforce/sfdx-lwc-jest
npm run test:unit -- --coverage
```

### Agent testing (Agentforce)

Agents are not fully deterministic, so test what matters: right topic, right actions, acceptable outcome.

#### Write an agent test spec

Generate a starter spec with the CLI so field names match your version, then edit it.

Generate a starter:

```bash
sf agent generate test-spec --output-dir specs/agent
```

`specs/agent/order-agent-testSpec.yaml`:

```yaml
name: Order Agent Regression
description: Core order support journeys
subjectType: AGENT
subjectName: Order_Support_Agent
testCases:
  - utterance: Where is my order ORDER_1?
    expectedTopic: order_status
    expectedActions:
      - GetOrderStatus
    expectedOutcome: The agent gives the order status and expected delivery date.
  - utterance: I want to return the shoes from ORDER_2
    expectedTopic: returns
    expectedActions: []
    expectedOutcome: The agent explains the return process and does not promise a refund.
  - utterance: What is the weather in Paris?
    expectedTopic: off_topic
    expectedActions: []
    expectedOutcome: The agent politely declines and offers help with orders.
```

- Cover each topic, plus off-topic, adversarial (ask for another customer data), ambiguous and multi-turn cases.
- Use synthetic data in the sandbox so the expected outcomes are stable.

> **Tip:** Ask Claude to draft test cases from docs/agent-design.md, then review them yourself. You know which edge cases the client cares about.

#### Create, run and export agent test results

Run:

```bash
sf agent test create --spec specs/agent/order-agent-testSpec.yaml --api-name Order_Agent_Regression --target-org client-dev
sf agent test run --api-name Order_Agent_Regression --target-org client-dev --wait 15 --result-format junit --output-dir reports/agent
sf agent test run --api-name Order_Agent_Regression --target-org client-dev --wait 15 --result-format json --output-dir reports/agent-json
```

- Check topic and action matches first. They are the most reliable signals.
- Treat outcome checks as softer. Re-run a failing case 3 times before you decide it is a real regression.
- Re-create the test definition after changing the spec file.

> **Careful:** Agent CLI commands and flags are still evolving. Confirm exact options with sf agent test run --help on your version.

### UI testing with Playwright

Test the journeys a user would actually take in Lightning or an Experience site.

#### Set up Playwright with reports and traces

Install:

```bash
npm init playwright@latest
npm install --save-dev @playwright/test
```

`playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 90_000,
  retries: process.env.CI ? 1 : 0,
  globalSetup: './tests/e2e/global-setup.ts',
  reporter: [
    ['list'],
    ['html', { outputFolder: 'reports/playwright-html', open: 'never' }],
    ['junit', { outputFile: 'reports/playwright-junit.xml' }],
    ['json', { outputFile: 'reports/playwright.json' }],
  ],
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'], storageState: '.auth/state.json' } },
  ],
});
```

#### Log in once with the Salesforce CLI session

No passwords in test code, and no MFA prompts. The CLI creates a one-time front door URL for the org you are already authorized to.

`tests/e2e/global-setup.ts`:

```typescript
import { chromium, FullConfig } from '@playwright/test';
import { execSync } from 'node:child_process';

export default async function globalSetup(_config: FullConfig) {
  const org = process.env.SF_ORG ?? 'client-dev';
  const raw = execSync('sf org open --target-org ' + org + ' --url-only --json').toString();
  const url = JSON.parse(raw).result.url; // contains a session token: never log it

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);
  await page.waitForURL(/lightning\.force\.com/, { timeout: 60_000 });
  process.env.SF_BASE_URL = new URL(page.url()).origin;
  await page.context().storageState({ path: '.auth/state.json' });
  await browser.close();
}
```

> **Careful:** .auth/state.json holds a live session. It is in .gitignore. Keep it there, and use sandboxes only.

#### Write resilient Lightning tests

`tests/e2e/account.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

test.use({ baseURL: process.env.SF_BASE_URL });

test('a new account can be created', async ({ page }) => {
  await page.goto('/lightning/o/Account/new');
  await page.getByLabel('Account Name').fill('PW Test Account');
  await page.getByRole('button', { name: 'Save', exact: true }).click();
  await expect(page.getByText(/Account .* was created/)).toBeVisible();
});
```

- Prefer getByRole, getByLabel and getByText. Avoid long CSS paths and auto-generated IDs.
- Playwright locators pierce open shadow DOM, which most Lightning components use.
- Use expect(...).toBeVisible() for waits instead of fixed sleeps.
- Create and clean up your own test data. Do not depend on records someone else made.
- If relative URLs fail, set baseURL explicitly in the config.

#### Test the agent through the chat UI

Use this for a few end-to-end journeys that prove the deployed experience works. Use the CLI agent tests for broad coverage.

`tests/e2e/agent-chat.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

test.use({ baseURL: process.env.SF_BASE_URL });

test('agent handles a return question', async ({ page }) => {
  await page.goto('/s/'); // Experience site with the agent embedded
  await page.getByRole('button', { name: /chat|agent/i }).click();

  const input = page.getByRole('textbox', { name: /message/i });
  await input.fill('I want to return my order ORDER_1');
  await input.press('Enter');

  const reply = page.locator('[class*="conversationEntry"]').last(); // adjust to your widget
  await expect(reply).toContainText(/return|refund/i, { timeout: 45_000 });
  await expect(reply).not.toContainText(/something went wrong|error/i);
});
```

- Assert on intent and key facts, not exact wording.
- Allow longer timeouts, then fail with a screenshot and trace.
- Keep each journey independent so one failure does not hide others.

> **Tip:** The chat widget selectors above are placeholders. Use npx playwright codegen on your site to find stable locators.

### Test results and reporting

Evidence that anyone can open: reports in CI, plus a plain-language summary.

#### Run everything in CI and keep the reports

`.github/workflows/test.yml`:

```yaml
name: test
on:
  pull_request:
  workflow_dispatch:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm install --global @salesforce/cli
      - name: Authenticate
        run: |
          echo "${{ secrets.SFDX_AUTH_URL_DEV }}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias client-dev
          rm auth.txt
      - name: Apex tests
        run: sf apex run test --target-org client-dev --test-level RunLocalTests --code-coverage --result-format junit --output-dir reports/apex --wait 30
      - name: Agent tests
        if: always()
        run: sf agent test run --api-name Order_Agent_Regression --target-org client-dev --wait 15 --result-format junit --output-dir reports/agent
      - name: UI tests
        if: always()
        run: |
          npx playwright install --with-deps chromium
          npx playwright test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports
          path: reports/
```

> **Tip:** if: always() makes sure agent and UI tests still run when Apex fails, so you see the full picture in one run.

#### Generate a plain-language test report with Claude

Download the artifacts into reports/, then ask for a summary a project manager can read.

Prompt:

```
Read everything under reports/ (JUnit XML and JSON for Apex, agent tests and Playwright).

Write docs/test-report.md with:
1. Headline: total passed, failed, skipped per suite, and Apex coverage percentage.
2. Failures: for each, the test name, the likely cause in one sentence, and the file or component to look at.
3. Flaky candidates: anything that failed on retry or looks non-deterministic (especially agent tests).
4. Coverage gaps: classes under 85 percent coverage.
5. Recommendation: ready to promote to the next environment, yes or no, and why.

Facts only from the reports. Mark anything you cannot verify. Include the date and commit hash.
```

---

## 4. Everything else

*First week, habits, troubleshooting, learning*

The things nobody puts in a setup guide, but that decide whether the first month goes well. Skim this now. Come back when something goes wrong.

### Your first week

A realistic plan for a new joiner.

#### Week one plan

- Day 1: finish track 1 and run the smoke test. Join #fde-help and say hello.
- Day 2: read the project CLAUDE.md, ADRs and handover doc. Authorize all project orgs.
- Day 3: pick a small, real ticket. Use plan mode, then implement with tests.
- Day 4: open a pull request. Walk the reviewer through your Claude-assisted workflow.
- Day 5: present what you learned and fix one thing in this guide or the CLAUDE.md.

### Working well with Claude Code

Habits that separate fast from fast and wrong.

#### Daily habits

- Plan first for anything non-trivial (Shift+Tab to switch modes). Review the plan, then let it build.
- Give it a way to check itself: tests to run, a validate command, a Playwright test.
- Read every diff. You are accountable for every line that ships.
- Small tasks and small commits. Start a fresh session (/clear) between unrelated tasks.
- When context gets long, run /compact. Put anything durable in CLAUDE.md instead.
- Reference files directly with @path so Claude reads the right thing.
- If Claude gets something wrong twice, fix the cause: add a rule to CLAUDE.md or a skill.

Useful commands:

```
/clear      start fresh
/compact    summarise and shrink the context
/memory     edit CLAUDE.md files
/agents     manage subagents
/mcp        see connected servers
/permissions  review allowed commands
```

#### Subagents for focused reviews

A subagent has its own context and instructions. Good for review tasks that should not pollute your main session.

`.claude/agents/apex-reviewer.md`:

```md
---
name: apex-reviewer
description: Reviews Apex changes for bulkification, governor limits, security (CRUD/FLS, sharing) and test quality. Use after Apex edits.
tools: Read, Grep, Glob, Bash
---

You are a senior Salesforce developer reviewing a diff.
Check: SOQL or DML in loops, missing bulk handling, hardcoded IDs, with sharing, FLS enforcement,
test assertions that prove behaviour, and test data created in @TestSetup.
Report findings by severity with file and line. Do not edit files.
```

### Security and client trust

Small mistakes here are big problems.

#### Non-negotiables

- No real customer data, credentials or auth URLs in prompts, commits, screenshots or tickets.
- Work in sandboxes. Production is read-only unless a deploy is approved through the pipeline.
- Rotate any credential you pasted by accident, then tell your lead.
- Check that skills, MCP servers and plugins come from a trusted source before installing.
- Run Code Analyzer before every pull request.
- Claude conversations are retained and may be reviewed by administrators under company policy.

Code Analyzer before a PR:

```bash
sf code-analyzer run --workspace force-app --view table
```

### Troubleshooting

The ten-minute fixes.

#### sf: command not found

Open a new terminal. If it persists, make sure npm global binaries are on your PATH.

Find the folder:

```bash
npm config get prefix
```

#### Apex features do not start in VS Code

The Apex language server cannot find Java. Install a JDK 17 or 21, then set salesforcedx-vscode-apex.java.home to the JDK folder and reload the window.

#### Expired access or refresh token

Sandbox sessions expire. Log in again with the same alias.

Re-authorize:

```bash
sf org login web --alias client-dev --instance-url https://test.salesforce.com
```

#### Deploy conflicts or unexpected overwrites

Preview before you deploy. Use ignore-conflicts only when you are sure about the direction.

Preview:

```bash
sf project deploy preview --source-dir force-app --target-org client-dev
```

#### Agent tests pass sometimes and fail sometimes

Expected with generative outputs. Check topic and action first, loosen outcome wording, run the case three times, and only worry about consistent failures. Look at the agent instructions if the same utterance routes to different topics.

#### Playwright cannot find an element in Lightning

Run npx playwright codegen against the org to see what Playwright suggests. Wait for the visible state you need instead of a fixed time, and check whether a modal or spinner is covering the element. Use the trace viewer on a failing run.

Explore and debug:

```bash
npx playwright codegen
npx playwright show-trace path/to/trace.zip
```

#### Claude forgets decisions or repeats mistakes

Long sessions lose detail. Capture the decision in CLAUDE.md or an ADR, then /clear and continue.

### Delivery and client habits

Technical skill gets you in the room. These keep you there.

#### Weekly status update template

Status:

```
Week of [date]
Done: what shipped or was decided, in business terms.
Next: top three things for next week.
Risks and blockers: what could slip, what you need, from whom, by when.
Decisions needed: the question, the options, your recommendation.
Metrics: the number we are trying to move, and where it stands.
```

#### Demo and expectation tips

- Demo on realistic synthetic data, from a sandbox you have rehearsed in.
- Show failures and guardrails for agents, not just the happy path.
- Say what is out of scope early and in writing.
- Estimate in ranges and name your assumptions. Re-estimate when an assumption breaks.

#### Know the Salesforce release rhythm

Salesforce ships three major releases a year (Spring, Summer, Winter). Sandboxes get previews first, so check release notes for features and retirements that affect your project.

### Learning and reference

Where to go deeper.

#### Learning path

- Trailhead: Apex, LWC, Flow, Agentforce and Data Cloud modules.
- Certifications worth targeting: Platform Developer I and II, JavaScript Developer I, Agentforce Specialist.
- Docs: developer.salesforce.com, the Claude Code docs, playwright.dev.
- Release notes: read the sections for the clouds on your current project.

#### Glossary

- **FDE:** forward deployed engineer, embedded with the client to deliver working outcomes.
- **Sandbox:** copy of production metadata for dev and test. **Scratch org:** short-lived, source-driven org.
- **DX:** Salesforce developer experience, the source-based workflow with the sf CLI.
- **Topic and action:** Agentforce building blocks. A topic is a job the agent can do, actions are what it can run.
- **Skill:** a folder of instructions Claude loads when relevant.
- **CLAUDE.md:** the file Claude reads at the start of every session.
- **ADR:** architecture decision record.
- **MCP:** Model Context Protocol, a standard for connecting Claude to tools like orgs and databases.

#### Team links and owners

Edit the TEAM block at the top of the HTML file to keep these current.

- Help channel: #fde-help
- Skills repo: https://github.com/YOUR-ORG/fde-claude-skills
- Project template: https://github.com/YOUR-ORG/fde-project-template
- Guide owner: your.name@company.com
- Security contact: security@your-company.com
