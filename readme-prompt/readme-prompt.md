Act as a senior frontend engineer and SVG graphic designer. 

Write the complete, self-contained SVG code for a trending GitHub Profile README card with terminal glassmorphism, animated ASCII art, typing effects, and dual dark/light theme support.

### 1. File Structure & Canvas
- Format: Single SVG file containing a github friendly format.
- Dimensions: viewBox="0 0 850 440", width="100%", height="440".
- Compatibility: All styles must be fully encapsulated in an internal <style> block. Do not import external fonts or scripts (must work under GitHub's Camo caching proxy).

### 2. Design System & Glassmorphism Aesthetics
- Outer Container: Deep modern developer dark background with subtle ambient radial gradients (cyan/blue on the upper-left, magenta/purple on the bottom-right).
- Main Window/Card:
  - Rounded corners (border-radius: 18px).
  - Background: Semi-transparent dark glass fill (rgba(18, 22, 34, 0.75)) with backdrop-filter: blur(20px) and a subtle 1px border (rgba(255, 255, 255, 0.12)).
  - macOS Terminal Controls: Red (#ff5f56), yellow (#ffbd2e), and green (#27c93f) traffic-light dots aligned horizontally, followed by user label: "guest@user-terminal:~".
- Layout: Split into a two-column layout:
  - Left panel: Dedicated container with a darker inset background for the ASCII graphic.
  - Right panel: Typography, role bullets, and pill tags.

### 3. Light / Dark Mode Support
- Default theme: Modern Dark mode.
- Use an inline @media (prefers-color-scheme: light) block to switch:
  - Card background to frosted light glass (rgba(255, 255, 255, 0.8)).
  - Border to translucent gray.
  - Primary text to #1f2328, muted text to #57606a, and accent glow/ASCII colors to deep cyan/blue (#0969da).

### 4. Left Panel: ASCII Art
- Content: use my profile svg "images/profile.jpeg" to cnvert it to an ASCII Art
- Dimensions: Monospace text, roughly 32–36 characters wide, 14–16 lines tall.
- Typography: font-family: monospace, font-size: 11px, line-height: 1.15.
- Color & FX: Cyan/neon-blue text (#38bdf8) with an active CSS pulsing glow animation:
  @keyframes glow { 0%, 100% { filter: drop-shadow(0 0 2px rgba(56,189,248,0.3)); } 50% { filter: drop-shadow(0 0 8px rgba(56,189,248,0.7)); } }
- Safety: Ensure all XML-conflicting characters (< and >) are either avoided or written as HTML entities (&lt; &gt;).

### 5. Right Panel: Content & Animations
- Header / Typing Effect:
  - Text: "> Hello, World! I build enterprise AI, and sharing it on every stage."
  - Animation: CSS typing animation with a continuous blinking vertical cursor bar (|).
- Bullets / Experience (Light dot prefix):
  - "Role: Forward Deployed Engineering Lead & a Salesforce CTA"
  - "Focus: I design and deliver enterprise-grade AI and customer-experience solutions on Salesforce — and I love turning what I learn into talks for teams, communities and conference stages."  
  - Primary keys in bold/white, descriptions in subtle muted gray (#94a3b8).
- Tech Badges (Footer):
  - Pill badges for: Agentforce, Data 360, React, Python, TypeScript.
  - Styled with rounded pill borders (border-radius: 9999px), dark translucent background, and matching monospace/sans-serif font.

Output only valid, raw, fully working SVG code without skipping any parts or using placeholders. And update the README.md file to contain the generated SVG and a bit of the description of this project.