# This is the FDE Onboarding Playbook: Beginner Mode (Tool Setup)

A field guide for Forward Deployed Engineers (FDEs) working on Salesforce and Agentforce. 

## 1. 🚀 Getting Access to FDE GitHub

Step 1: Request Access Through IdentityIQ

1. Log into Salesforce Okta
2. Go to EIP Enterprise IGA Platform (https://securityhub.internal.salesforce.com/iam/ignite/ignite-home)
3. Click Manage User Access > Select Yourself > Click Next 
4. Search for and select GHEC_forward-deployed-engineering-emu_Users
5. Click Next > Put in a Business Justification > Click Submit
    1. If a “Complete Work Item” window appears, select No for the “Do you have a case number for this request?” dropdown and click Proceed
    2. Please note the provisioning process requires manager approval and may take 1-3 business days


## 2. Baseline check: Set up your machine

*VS Code, Salesforce CLI, Claude Code*

Before you build anything, make sure your machine is ready. Work through these three steps in order.

### Foundations

#### Step 1 — Install Node.js

Salesforce CLI and Claude Code both need Node.js. 

Verify:

```bash
node -v    # should show v22.x
npm -v     # confirms npm is installed
```

If you don't have it: Install (macOS / Linux):

```bash
brew install node    # Mac, via Homebrew
```

Install (Windows):

```powershell
winget install OpenJS.NodeJS.LTS
```

#### Step 2 — Install Java

A JDK (17 or 21) is required by the Apex language server and Code Analyzer.

Verify:

```bash
java -version
```

If you don't have it: Install (macOS / Linux):

```bash
brew install openjdk
```

Install (Windows):

```powershell
winget install --id EclipseAdoptium.Temurin. LTS --exact
```

#### Step 3 — Install Git

Git is a version control tool that tracks code changes, supports collaboration, and lets you restore earlier versions of a project.

Verify:

```bash
git --version
```

If you don't have it: Install (macOS / Linux):

```bash
brew install git
```

Install (Windows):

```powershell
winget install --id Git.Git --exact
```

#### Step 4 — Install Github CLI

GitHub CLI lets you manage repositories, issues, and pull requests from your terminal.

Verify:

```bash
gh --version
```

If you don't have it: Install (macOS / Linux):

```bash
brew install gh
```

Install (Windows):

```powershell
winget install --id GitHub.cli --exact
```

#### Step 5 — Install the Salesforce CLI

Salesforce CLI lets you manage Salesforce orgs and develop Salesforce apps from your terminal. The sf command is how you deploy, test and automate everything.

Verify:

```bash
sf --version
```

If you don't have it: Install (macOS / Linux):

```bash
npm install --global @salesforce/cli
sf --version
sf update
```

Install (Windows):

```powershell
winget install --id Salesforce.cli --exact
```

## 3. IDE Setup: Install VS Code and the extensions

VS Code is a free editor with Salesforce extensions that help you write and deploy Salesforce code, including Apex and Lightning Web Components.

```bash
brew install --cask visual-studio-code
```

Install (Windows):

```powershell
winget install --id Microsoft.VisualStudioCode --exact
```

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

> **Note:** Install Salesforce extensions
Open VS Code, open the Extensions panel, search for Salesforce Extension Pack by Salesforce, and select Install.

## 4. Set up Git identity, SSH key and GitHub login

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

## 4. Claude Code

⚙️ Claude Code: A developer-focused CLI tool for coding, debugging, deployments, and engineering workflows. For engineers who want to build, fix, and ship faster from the terminal or IDE.

Before you start
:check-blue: ZScaler connected
:check-blue: Your @salesforce.com Google account

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

Install (Windows):

```powershell
npm install -g @anthropic-ai/claude-code
claude --version
```

> **Note:** Keep Terminal open while the installer checks your machine, installs Claude Code, and opens your browser for Google sign-in.

### Sign in with Google

A browser tab will open at accounts.google.com.

* Choose your @salesforce.com account.
* Click Continue when prompted.
* When the browser says sign-in is complete, close the tab and return to Terminal.

If the installer says you already have a key, choose Y to regenerate it and continue.

## 5. Add Salesforce skills to Claude Code

Get started — in Claude Code, add the Agentforce Agent Development Lifecycle (ADLC) skills library:

```
npx skills add forcedotcom/sf-skills
claude plugin marketplace add SalesforceAIResearch/agentforce-adlc
claude plugin install agentforce-adlc@agentforce-adlc
claude plugin marketplace add forward-deployed-engineering-emu/fde-skills
```

Launch Claude code in terminal:
```
claude
```