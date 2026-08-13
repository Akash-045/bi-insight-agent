# Autonomous BI Insight Agent
### *"Metrics That Investigate Themselves"*

An agent that automates the root-cause investigation an analyst normally does by hand: when a KPI moves, it segments the data across multiple dimensions, tests each split for statistical significance, and reports back a ranked, plain-English explanation — showing its work along the way.

> **Status:** 🚧 In development. This README will evolve as the project is built.

---

## Why this project exists

Most BI dashboards tell you a number has moved. None of them tells you *why* — that's still manual work: slicing by channel, segment, geography, device, and time, testing each cut, and ruling out the noise. This agent automates that investigative process itself, instead of just visualising the result.

This project is a direct extension of my [Vanguard A/B Test analysis](#), where I manually found that a UI redesign *improved* completion rates but *introduced friction* in later steps — a finding hidden one layer beneath the headline metric. This agent is built to test whether an autonomous process can reach the same conclusion, and to see what it might surface that a first pass misses.

---

## What it does

1. **Monitors** a KPI (e.g. completion rate, revenue, conversion rate) for a significant change
2. **Segments** the data across available dimensions (e.g. age, tenure, channel, device, step)
3. **Tests** each segment split statistically (t-tests, z-tests, chi-square — not eyeballing)
4. **Explains** the finding in plain language, ranked by confidence
5. **Shows its work** — which segments were checked, which came back insignificant, so the conclusion can be verified, not just trusted

---

## Dataset

Built on the [Vanguard CX A/B Test dataset](#) — an A/B test comparing a traditional vs. redesigned digital process, with client demographics (age, tenure, gender, balance) and step-by-step funnel timestamps.

## Tech stack

- **Agent logic:** Claude API (tool use/function calling)
- **Stats:** Python, scipy / statsmodels
- **Data handling:** pandas
- **Interface:** Streamlit
- **Hosting:** Streamlit Community Cloud (free tier)
- **Storage:** Supabase (free tier)

## Roadmap

- [ ] Data prep and cleaning (reuse from original Vanguard analysis)
- [ ] Define KPI monitoring logic (detect the "significant change" trigger)
- [ ] Build segment-testing loop (agent decides which cuts to test)
- [ ] Structure Claude API calls for the investigation + explanation step
- [ ] Build Streamlit interface
- [ ] Validate agent's findings against my original manual analysis
- [ ] Deploy live demo

## Author

**Akash Samantray** — Data/BI Analyst focused on AI traceability and validation, not black-box automation.
[LinkedIn](https://linkedin.com/in/akash-samantray) · [GitHub](https://github.com/Akash-045)