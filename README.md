# Autonomous BI Insight Agent
### *"Metrics that investigate themselves"*

**Live app:** [akash-045-bi-insight-agent-app-mdxxjj.streamlit.app](https://akash-045-bi-insight-agent-app-mdxxjj.streamlit.app/)

An agent that automates the root-cause investigation an analyst normally does by hand: when a KPI moves, it segments the data across multiple dimensions, tests each split for statistical significance, and reports back a plain-English explanation — while checking its own work for small-sample errors before it reports anything.

---

## Why this project exists

Most BI dashboards tell you a number moved. They don't tell you *why* — that's still manual work: slicing by segment, testing each cut, ruling out noise. This project automates that investigative process, and — just as importantly — validates whether an AI agent doing this automatically can be trusted, or whether it needs guardrails to stop it from reporting false findings.

This is a direct extension of my [Vanguard CX A/B Test analysis](https://github.com/Akash-045/customer-experience-project), where I manually found that a UI redesign *improved* completion rates but *introduced friction* in later steps — a finding hidden one layer beneath the headline metric. This project asks: can an autonomous agent rediscover that same finding on its own?

**Short answer: yes — after two rounds of fixing its mistakes.** That process is the actual point of this project.

---

## What it does

1. **Loads** cleaned client and funnel data from the Vanguard CX experiment
2. **Tests** each segment (age, tenure, gender, number of accounts) against three metrics — completion rate, process duration, and backward navigation — using proper statistical tests (chi-square, t-test)
3. **Checks its own reliability** — any segment with a group smaller than 30 people is automatically skipped, rather than reported as a real finding
4. **Explains** the results in plain English via the Claude API, under explicit rules: no demographic-targeting recommendations, no guessed motivations — facts only
5. **Displays** everything in an interactive Streamlit app, including which findings were trusted and which were flagged

---

## Key finding

| Metric | Control | Test | Statistically significant? |
|---|---|---|---|
| Completion rate | 65.58% | 69.29% | ✅ Yes |
| Avg. process duration | 293.8s | 328.4s (+12%) | ✅ Yes |
| Backward navigation rate | 26.09% | 33.41% (+7.3pp) | ✅ Yes |

**The redesign works — but it isn't free.** Test group users complete the process more often, but take longer and backtrack more, indicating friction that a completion-rate-only dashboard would completely miss. This pattern held consistently across all reliable age and tenure segments, and was concentrated most heavily among older and longer-tenured clients.

The agent independently rediscovered this exact finding — without being told the answer — once its guardrails were correctly implemented.

---

## Two real bugs caught during development (the actual story of this project)

**Bug 1 — Agent confidently reported findings from near-empty groups.**
On the first run, the agent ranked a segment with 100% completion as its *top finding*, even though that "group" contained only 1–2 people. It looked statistically valid (p < 0.05) but was pure noise. Fixed by adding a minimum sample-size check (30+ per group) before any segment is allowed into the agent's analysis.

**Bug 2 — The sample-size guardrail itself was broken.**
After adding the fix, *every* segment started getting skipped — the check was accidentally counting raw individual values (e.g. each exact age) instead of the actual High/Low groups being compared. Fixed by moving the check to run after grouping, not before.

**Why this matters for the project's thesis:** an AI agent doing statistical analysis will confidently report wrong conclusions if it isn't explicitly told to check its own sample sizes. This project doesn't just automate analysis — it demonstrates *why* that automation needs a human-designed validation layer to be trustworthy.

---

## Tech stack

- **Agent logic:** Claude API (Anthropic)
- **Stats:** Python, scipy
- **Data handling:** pandas
- **Interface:** Streamlit
- **Hosting:** Streamlit Community Cloud (free tier)
- **Secrets management:** python-dotenv (local), Streamlit Secrets (deployed)

---

## Project structure

```
├── app.py                                  # Streamlit interface
├── requirements.txt
├── 01_data_exploration_and_cleaning.ipynb  # Load, clean, merge raw data
├── 02_manual_segment_analysis.ipynb        # Baseline hypothesis testing (ground truth)
├── 03_agent_investigation_pipeline.ipynb   # Autonomous agent investigation
├── 04_validation_and_comparison.ipynb      # Agent findings vs manual baseline
├── client_table_clean.csv                  # Cleaned client-level data
├── web_events_clean.csv                    # Cleaned funnel event data
└── agent_findings.txt                      # Saved agent output
```

---

## Dataset

[Vanguard CX A/B Test dataset](https://github.com/Akash-045/customer-experience-project) — an A/B test comparing a traditional vs. redesigned digital process, with client demographics (age, tenure, gender, balance) and step-by-step funnel timestamps for 50,487 experiment clients across 317,235 funnel events.

---

## Author

**Akash Samantray** — Data/BI Analyst focused on AI traceability and validation, not black-box automation.
[LinkedIn](https://linkedin.com/in/akash-samantray) · [GitHub](https://github.com/Akash-045)