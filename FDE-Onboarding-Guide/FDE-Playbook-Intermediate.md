# This is the FDE Onboarding Playbook: Intermediate Mode (Project Setup)

A field guide for Forward Deployed Engineers (FDEs) working on Salesforce and Agentforce. This builds on the Beginner playbook — before you start, make sure you have finished it: Git, Node, the Salesforce CLI (`sf`), the GitHub CLI (`gh`), VS Code, and Claude Code are all installed and signed in.

> **Note:** All names below are placeholders. Replace `YOUR-ORG` (your GitHub org), `acme-fde` (the project), and `client-dev` (an org alias) with your real values. Never put real customer data, credentials, or org auth URLs in files, commands, or chat — use placeholders like `CUSTOMER_1`.

## 1. 🚀 Setting up a GitHub FDE Project

A project lives in one Git repository. You will either join an existing project or start a new one.

### Pick a folder for your work

Keep all FDE projects in one place so they are easy to find.

Create it (macOS / Linux):

```bash
mkdir -p ~/dev/fde && cd ~/dev/fde
```

Create it (Windows / PowerShell):

```powershell
mkdir $HOME\dev\fde -Force; cd $HOME\dev\fde
```

### Option A — Join an existing project

Clone the repo your lead gives you, then open it in VS Code.

```bash
gh repo clone YOUR-ORG/acme-fde
cd acme-fde
code .
```

### Option B — Start a new project

If you are creating the project, scaffold it first (Section 3), then create the repo and push.

```bash
cd acme-fde
git init -b main
gh repo create YOUR-ORG/acme-fde --private --source . --remote origin
git add . && git commit -m "chore: initial project scaffold"
git push -u origin main
```

> **Note:** Use the team project template if one exists (ask your lead). It gives you the folders, CI, pull request template, and a starter `CLAUDE.md` in one step.

### Branching basics

- Create short-lived branches from `main`, named like `feature/TICKET-123-short-name`.
- Keep pull requests small; one approval and a green build before merge.
- Never force-push `main`.

```bash
git switch -c feature/TICKET-123-order-status
# ...make changes...
git add . && git commit -m "feat: add order status action"
git push -u origin HEAD
gh pr create --fill
```

## 2. 📁 Project folder structure

A Salesforce DX project has a predictable layout. Learn where things go before you add to it.

```text
acme-fde/
├─ force-app/main/default/     # all Salesforce metadata (Apex, LWC, objects, flows…)
│  ├─ classes/                 # Apex classes and tests
│  ├─ lwc/                     # Lightning Web Components
│  ├─ objects/                 # custom objects and fields
│  └─ flows/                   # flows
├─ config/                     # scratch org definition files
├─ manifest/                   # package.xml manifests for retrieve/deploy
├─ scripts/                    # apex / shell helper scripts
├─ specs/                      # agent test specs, design notes
├─ docs/                       # ADRs, HANDOVER.md, diagrams
├─ .claude/                    # Claude Code project config (CLAUDE.md, settings, skills)
├─ .gitignore
├─ sfdx-project.json           # defines package directories and API version
└─ README.md
```

- `force-app/main/default` is the source of truth for everything you deploy.
- `sfdx-project.json` tells the CLI where your source lives. Do not delete it.
- `docs/` is where your handover and decisions live — treat it as a deliverable, not an afterthought.

## 3. ⚙️ Create a placeholder Salesforce DX project

If you are not cloning an existing project, generate a fresh one to work in.

### Step 1 — Generate the project

```bash
sf project generate --name acme-fde --template standard --manifest
cd acme-fde
```

Verify the project was created:

```bash
sf project list ignored --help >/dev/null 2>&1 && echo "sf is working"
ls force-app/main/default
```

### Step 2 — Authorize a sandbox with a clear alias

Use a `client-env` naming pattern. Sandboxes log in at `test.salesforce.com`.

```bash
sf org login web --alias client-dev --instance-url https://test.salesforce.com --set-default
sf org list
sf org display --target-org client-dev
```

> **Note:** Never make production your default org. Production and Developer Edition use `login.salesforce.com` (the default host); sandboxes use `test.salesforce.com`. If you see an expired-token error later, just run `sf org login web` again with the same alias.

### Step 3 — Pull a baseline from the org

Bring the org's current metadata into your project so you start from a known state.

```bash
sf project generate manifest --from-org client-dev --output-dir manifest
sf project retrieve start --manifest manifest/package.xml --target-org client-dev
git add . && git commit -m "chore: baseline metadata from client-dev"
```

### Step 4 — (Optional) Create a scratch org

Only if the project uses scratch orgs and you have a Dev Hub.

```bash
sf org login web --alias devhub --set-default-dev-hub
sf org create scratch --definition-file config/project-scratch-def.json --alias scratch1 --duration-days 7 --set-default
```

### Step 5 — Validate a deployment (no changes yet)

A dry run confirms your project and org connection work end to end.

```bash
sf project deploy validate --source-dir force-app --target-org client-dev --test-level RunLocalTests
```

## 4. 🔒 Safe `.gitignore` and secrets hygiene

Before your first commit, make sure local state and secrets can never be checked in.

`.gitignore`:

```gitignore
# Salesforce local state
.sf/
.sfdx/
.localdevserver/

# Secrets and sessions
.env
.env.*
auth*.txt
.auth/

# Node and test output
node_modules/
reports/

# Claude Code local-only settings
.claude/settings.local.json
```

> **Note:** `sf org display --verbose` prints a secret auth URL. Do not paste its output into chat, tickets, or Claude prompts. If you ever paste a credential by accident, rotate it and tell your lead.

## 5. 🤖 Claude Code best practices

Claude Code is most useful when the project tells it how you work. Set these up once per project.

### Write a project `CLAUDE.md`

Claude reads this at the start of every session. Keep it under ~100 lines: context, commands, conventions, and hard rules. Update it whenever you correct Claude twice about the same thing.

`CLAUDE.md`:

```md
# Project: ACME service transformation

## Context
- Goal: deflect order-status cases with an Agentforce agent.
- Clouds: Service Cloud, Experience Cloud, Data Cloud.

## Orgs
- client-dev: sandbox, default target
- client-uat: sandbox, deploy only via pipeline
- client-prod: READ ONLY. Never deploy, never run DML.

## Commands
- Validate: sf project deploy validate --source-dir force-app --target-org client-dev --test-level RunLocalTests
- Apex tests: sf apex run test --target-org client-dev --test-level RunLocalTests --code-coverage --wait 30
- LWC tests: npm run test:unit

## Conventions
- Apex: one trigger per object, logic in handler classes, bulk-safe, no SOQL/DML in loops.
- Names: Acme_ prefix for custom metadata; verbs for Apex actions (GetOrderStatus).

## Rules
- Never commit secrets, auth URLs, or customer data. Use placeholders like CUSTOMER_1.
- Ask before deploying to any org or pushing to GitHub.
- Update docs/HANDOVER.md when architecture changes.
```

### Set shared permissions in `.claude/settings.json`

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
      "Bash(sf project deploy validate:*)"
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

> **Note:** Personal overrides go in `.claude/settings.local.json`, which stays out of Git (see Section 4).

### Daily habits

- **Plan first.** For anything non-trivial, switch to plan mode (press `Shift+Tab`). Claude explores the repo read-only and proposes a plan; you approve before any change.
- **Give it a way to check itself.** Point Claude at a validate command or the test suite so it can confirm its own work.
- **Read every diff.** You are accountable for every line that ships. Small tasks, small commits.
- **Keep context clean.** Start a fresh session with `/clear` between unrelated tasks; run `/compact` when a session gets long. Put anything durable in `CLAUDE.md`, not the chat.
- **Point precisely.** Reference files with `@path/to/file` so Claude reads the right thing.
- **Fix the cause.** If Claude gets something wrong twice, add a rule to `CLAUDE.md` or create a skill — don't just correct it again.
- **Protect data.** Never paste real customer data, credentials, or auth URLs. Use placeholders such as `CUSTOMER_1`.

### Useful in-session commands

```text
/clear        start fresh
/compact      summarise and shrink the context
/memory       edit CLAUDE.md files
/agents       manage subagents
/mcp          see connected servers
/permissions  review allowed commands
```

### Launch Claude Code in the project

```bash
cd acme-fde
claude
```

## 6. ✅ Verify your project is ready

Run these from the project root. If each step succeeds, you are ready to start feature work.

```bash
sf org display --target-org client-dev     # shows your connected sandbox
sf project deploy validate --source-dir force-app --target-org client-dev --test-level RunLocalTests
git status                                  # clean tree, on a feature branch
ls .claude/CLAUDE.md CLAUDE.md 2>/dev/null  # project guidance exists
```

- [ ] Repo cloned or created and pushed to `YOUR-ORG`
- [ ] Standard folder structure in place, `sfdx-project.json` present
- [ ] Sandbox authorized with a clear alias; production is **not** the default
- [ ] Baseline metadata retrieved and committed
- [ ] `.gitignore` blocks secrets and local state
- [ ] `CLAUDE.md` and `.claude/settings.json` committed
- [ ] A deploy **validate** passes with local tests

Next up: start your first ticket — plan it with Claude, build with tests, and open a small pull request.
