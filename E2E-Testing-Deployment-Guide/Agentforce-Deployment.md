# Agentforce Testing & Deployment — FDE Presenter Guide

# PART 2 — AGENTIC DEPLOYMENT *(15 minutes)*

**Section promise:** *"An agent is metadata. Everything we know about Salesforce release management applies — with a few new steps."*

### 2.1 — An agent is a bundle of linked metadata *(2 min)*

**Key message:** Moving an agent means moving *all* its files together — miss one dependency and the deploy fails, or worse, deploys an agent that silently can't act.

| Metadata type | What it represents |
|---|---|
| **`AiAuthoringBundle`** | The **draft** agent as an Agent Script `.agent` file — human-readable, easy to review in PRs |
| **`Bot` / `BotVersion`** | Top-level agent record + versions (only one version is active) |
| **`GenAiPlannerBundle`** | The reasoning-engine config, generated when a version is committed/published |
| **`GenAiPlugin` / `GenAiFunction`** | Subagents (topics) and actions |
| **`GenAiPromptTemplate`** | Prompt templates used by actions |
| **`AiEvaluationDefinition`** | Testing Center test suites |
| **Dependencies** | ApexClass, Flow, custom objects/fields, permission sets, **Data Library / Data Cloud** assets |

> **Insight:** the **draft** lives in `AiAuthoringBundle`; the **runtime** (`Bot` + `GenAiPlannerBundle`) is created on commit, and committed versions are **immutable** — which is exactly what makes rollback reliable. New builder needs **API v66.0+**; always check the Agentforce DX "Move an agent" guide for your target API version.

### 2.2 — Git, SFDX project & package.xml *(3 min)*

**Key message:** Git is the source of truth; the SFDX project is the folder shape; `package.xml` is the manifest that says *what moves*.

- An **SFDX project** (`sfdx-project.json` + `force-app/`) is how agent source lives on disk — everything you click in Builder is also **text you can diff and review** in a pull request.
- **`package.xml`** lists metadata types + members to retrieve or deploy. Use **exact member names as retrieved** — don't guess suffixes. Generate a starter from an org.
- Use the **`Agent` pseudo-type** to retrieve/deploy an agent and its parts in one go. Keep **one manifest per release**, committed with the change.

```bash
# generate a starter manifest from an org, then retrieve
sf project generate manifest --from-org client-dev --output-dir manifest
sf project retrieve start --manifest manifest/package.xml --target-org client-dev
sf project retrieve start --metadata "Agent:Service_Agent" --target-org client-dev
```

```xml
<!-- package.xml (excerpt) -->
<types><members>Service_Agent</members><name>AiAuthoringBundle</name></types>   <!-- draft -->
<types><members>Service_Agent</members><name>Bot</name></types>                  <!-- runtime -->
<types><members>Service_Agent*</members><name>GenAiPlannerBundle</name></types>
<types><members>GetOrderStatusAction</members><name>ApexClass</name></types>
<types><members>Service_Agent_Access</members><name>PermissionSet</name></types>
<types><members>Service_Agent_Tests</members><name>AiEvaluationDefinition</name></types>
<version>66.0</version>
```

> **IDE shortcut:** the VS Code **Org Browser** (Salesforce Extension Pack, also works in Cursor) lets you browse `Bot` / `GenAiPlannerBundle` / `AiAuthoringBundle` and retrieve with one click — great for *discovery* in a new org. For *repeatable* releases, graduate to a manifest.

### 2.3 — Salesforce CLI: retrieve → validate → deploy *(3 min)*

**Key message:** The single most valuable production habit — **validate first, quick-deploy in the window.**

```bash
# validate against production days before the window (nothing is committed)
sf project deploy validate --manifest manifest/package.xml \
  --target-org YOUR-ORG --test-level RunLocalTests

# quick-deploy the already-validated job during the change window
sf project deploy quick --job-id 0AfXX00000000001 --target-org YOUR-ORG

# then turn the draft into a version and activate it
sf agent publish authoring-bundle --api-name Service_Agent --target-org YOUR-ORG
sf agent activate --api-name Service_Agent --version 2 --target-org YOUR-ORG
```

**Habits that save go-lives:**
- Use `--test-level RunLocalTests` (or `RunSpecifiedTests`) for production.
- **Deploy dependencies before the agent.**
- Agents run **as a user**, and usernames differ by org — use string replacements in `sfdx-project.json`, never hard-code.
- After deploying, **publish/deploy the planner bundle, then activate** the version.

> `sf` commands are identical on macOS/Linux and Windows — only shell quoting differs (Windows PowerShell uses backticks for line continuation instead of `\`).

### 2.4 — Org-based vs package-based development *(2 min)*

| | **Org-based** | **Package-based (unlocked / 2GP)** |
|---|---|---|
| **Unit of release** | A set of changes in a manifest | A versioned, installable package |
| **Source of truth** | The org (or Git via CLI/DevOps Center) | **Git, always** |
| **Best for** | Single-org customers, fast first releases | Multi-team/multi-org programmes, ISVs, reusable agents |
| **Rollback** | Redeploy previous metadata; reactivate prior version | Install a previous package version |
| **Watch out for** | Org drift, missed dependencies | Setup effort, dependency design, not-yet-packageable metadata |

> **FDE guidance:** most engagements **start org-based**. Recommend packages when the customer runs **multiple orgs** or wants a **reusable agent** across business units. Check the **Metadata Coverage Report** for packaging support before committing to a package design.

### 2.5 — Deployment tooling: from clicks to pipelines *(3 min)*

**Key message:** We rarely pick the tool — the customer usually has one. Be fluent enough to plug the agent into whatever exists.

- **Change sets** — original point-and-click between connected orgs. No version control, no rollback, limited support for newer agent metadata. **Not recommended for agent work.**
- **Salesforce DevOps Center** — free, **Git-backed** release tool with work items + pipeline stages; good for admin/mixed teams moving off change sets. Confirm current agent-metadata support.
- **CLI scripts** — the commands above wrapped in a shell/Node script, run by a person. Great for first releases and rehearsals; graduate to CI/CD once stable.
- **CI/CD platforms** — **GitHub Actions, Bitbucket Pipelines**, Azure DevOps, Jenkins, GitLab CI all run the same CLI commands headlessly with **JWT auth**. You own the pipeline, secrets, and maintenance.
- **Data 360 (Data Cloud) data kits** — agent knowledge and grounding data are **data, not metadata**. Package and move Data Cloud assets via **data kits**, and index the Data Library, as a **separate deploy path**. Plan for it early — it's the step people forget.

```yaml
# .github/workflows/agent-ci.yml  (Bitbucket/Azure differ only in syntax)
on: pull_request
jobs:
  validate-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install --global @salesforce/cli
      - run: |                                   # JWT auth — secrets live in the store, never the repo
          sf org login jwt --client-id "${{ secrets.SF_CLIENT_ID }}" \
            --jwt-key-file server.key --username "${{ secrets.SF_CI_USER }}" \
            --instance-url https://test.salesforce.com --alias ci
      - run: sf project deploy start --manifest manifest/package.xml --target-org ci --test-level RunLocalTests
      - run: |                                   # draft → version
          sf agent publish authoring-bundle --api-name Service_Agent --target-org ci
          sf agent activate --api-name Service_Agent --version "${{ vars.AGENT_VERSION }}" --target-org ci
      - run: sf agent test run --api-name Service_Agent_Tests --wait 20 --result-format junit --output-dir test-results --target-org ci  # the gate
```

The pipeline shape is always the same — **PR → deploy to CI sandbox → publish & activate → agent test gate → validate prod → quick deploy** — only the YAML syntax changes between GitHub Actions, Bitbucket, and Azure DevOps.

### 2.6 — ISV DevOps tools *(2 min)*

For large programmes, audit needs, and mixed admin/developer teams:

- **Copado** — runs **natively on Salesforce**; user stories, pipelines, compliance tracking. Built for larger, governed teams.
- **Gearset** — **comparison-driven** deploys, problem analysers, documented Agentforce metadata support. Fast to adopt, popular with mixed teams.
- **AutoRABIT** — CI/CD with strong **security/compliance** features for regulated industries.
- **Flosum** — **100% native** on the platform; popular where **data residency** matters.

> **Ask every vendor:** *Do you support the agent metadata types today — show me a deployment. Can I run my own CLI test job as a pipeline step? Does a failing agent test block promotion? What's the audit trail and rollback story?* This area moves fast — verify current support before committing.

### 2.7 — Go-live steps people forget + common gotchas *(1 min)*

**After the deploy:** confirm dependencies landed → provision data (Data Cloud data kits, Data Library, knowledge) → publish/commit the version → **activate** → assign permissions → connect channels → smoke test → turn on monitoring → **rollback plan ready** (reactivate the previous immutable version).

**Common gotchas:** manifest API version too low · missing `GenAiFunction`/`GenAiPlugin` dependencies fail the planner bundle · agent-user username copied from the source org · trying to edit a committed (immutable) version · scratch orgs without Agentforce/Data Cloud provisioned (use sandboxes) · "it's only a read action" testing in production.

---
---

# Q&A #2 — DEPLOYMENT KNOWLEDGE CHECK *(5 minutes)*

> Same format. ✅ = correct.

**Q1. Where does the *draft* of an Agent Script agent live as metadata?**
- A) ✅ **`AiAuthoringBundle`**
- B) `BotVersion`
- C) `CustomObject`
- D) `GenAiPromptTemplate`
*Why: committing/publishing turns the draft into `Bot` + `GenAiPlannerBundle` runtime metadata.*

**Q2. Which command checks a production deployment *without committing* it?**
- A) `sf org open`
- B) ✅ **`sf project deploy validate`**
- C) `sf project deploy start` with no flags
- D) `sf agent activate`
*Why: validate first, then `sf project deploy quick --job-id` inside the change window.*

**Q3. What is the `package.xml` in a deployment?**
- A) The agent's reasoning configuration
- B) A log of past deployments
- C) ✅ **The manifest listing which metadata types and members to retrieve/deploy**
- D) The CI/CD pipeline definition
*Why: generate a starter with `sf project generate manifest --from-org`; keep one per release in Git.*

**Q4. A customer runs multiple orgs and wants one reusable agent across business units. Which approach fits best?**
- A) Change sets
- B) Org-based development
- C) ✅ **Package-based development (unlocked / 2GP)**
- D) Manual metadata copy
*Why: package-based gives versioned, installable units with Git as the source of truth; check the Metadata Coverage Report first.*

**Q5. Agent **knowledge / grounding data** from Data Cloud (Data 360) is deployed how?**
- A) Inside `package.xml` with the rest of the metadata
- B) ✅ **As a separate path — Data Cloud data kits / Data Library indexing**
- C) It deploys automatically with the Bot
- D) Via change sets only
*Why: data is not metadata — plan the data-kit path early; it's the most-forgotten go-live step.*

---
---

# OPEN FLOOR — AUDIENCE QUESTIONS *(10 minutes)*

**Transition line:** *"Two things to take back to your first engagement: **test the decision, not the sentence**, and **treat the agent as metadata — ship it with its dependencies and let the pipeline say no.** Now, your questions."*

**Likely questions — have crisp answers ready:**
- *"How many test cases is enough?"* → Start 5 happy / 3 edge / 2 negative **per subagent**; grow from real failures.
- *"How do we handle flaky/non-deterministic results?"* → Run each case N times, pass at a threshold (e.g. 4/5); track the trend, not one run.
- *"Blocking gate from day one?"* → No — non-blocking ~2 weeks, then blocking once the team trusts the numbers.
- *"Scratch orgs for agents?"* → Usually no — use sandboxes; scratch orgs often lack Agentforce/Data Cloud provisioning.
- *"Which ISV tool should we pick?"* → No tool wins everywhere; match to team shape, budget, and release cadence — and verify current agent-metadata support.

**First-week homework for attendees:**
1. Build a small agent in your dev sandbox.
2. Write 10 test cases and run them from the CLI.
3. Retrieve the agent, write its `package.xml`, deploy to a second sandbox.
4. Run one promptfoo red-team scan against it.

---

## Appendix — Resources to share in chat

- The Agent Development Lifecycle (Salesforce Architects)
- Agentforce DX: agent metadata
- Agentforce DX: move an agent to a new org
- Agentforce Testing Center (Salesforce Help)
- The new Agentforce metadata & development lifecycle (Developer blog)
- OWASP Top 10 for LLM Applications

## Appendix — Demo backup index

| Demo | Live tool | Backup recording |
|---|---|---|
| 1 | Agent Builder Preview (simulation → live, trace) | `demos/01-agent-builder-preview.mp4` |
| 2 | Testing Center batch run | `demos/02-testing-center-batch.mp4` |
| 3 | Playwright vs Enhanced Chat (headed + trace viewer) | `demos/04-playwright-ui.mp4` |
| — | CLI test run (optional) | `demos/03-cli-test-run.mp4` |
| — | Org browser retrieve (optional, deployment) | `demos/05-org-browser-retrieve.mp4` |
| — | Pipeline run (optional, deployment) | `demos/06-pipeline-run.mp4` |

> **Reminder:** never show tokens, auth URLs, or real customer org data on screen. All demos use placeholder names.
