# About Me

- I’m a forward-deployed engineer (FDE), working primarily with Salesforce and Agentforce.
- I’m building FDE onboarding materials for EMEA South builders. This repo holds that content: staged playbooks (`FDE-Onboarding-Guide/`), an interactive field guide (`references/`), and a GitHub profile card (`README.md` + `readme-prompt/`). It is content, not an app — no build, tests, or packaging.

# Working Style

- Start by confirming required access and prerequisites are in place — repository permissions, accounts, and core tooling such as an IDE, Git, Node, a JDK, the Salesforce CLI, and Claude Code.
- Explain setup steps clearly so builders can prepare their FDE and AI tooling before they begin. Give both macOS/Linux and Windows commands so anyone can follow along.
- Work iteratively: confirm intent, then make focused changes and validate as I go. When the work involves code or agents, run the relevant unit/agent tests; for the docs here, preview the rendered HTML/SVG and keep the field guide’s `.md` and `.html` in sync.
- Before anything reaches a customer, confirm packaging and the staging deployment process, and validate the result in staging — never straight to production.
- Keep guidance practical, explicit, and appropriate for builders with varied levels of experience.
- Use placeholders in every example (`CUSTOMER_1`, `client-dev`, `YOUR-ORG`). Never put real customer data, credentials, or org auth URLs in files or commands.
