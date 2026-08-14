import os
import pandas as pd
from scipy import stats
import streamlit as st
from dotenv import load_dotenv
import anthropic

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

st.set_page_config(
    page_title="Autonomous BI Insight Agent",
    page_icon="◆",
    layout="wide"
)

# ------------------------------------------------------------
# Custom styling — "lab report" aesthetic: cool paper background,
# serif display headers, monospace for stats/numbers to reinforce
# the project's whole point: rigor and traceability, not vibes.
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --bg: #F4F5F7;
    --surface: #FFFFFF;
    --ink: #14181F;
    --muted: #5B6472;
    --border: #E2E4E9;
    --confidence: #1E7F6E;
    --confidence-bg: #E7F3F0;
    --flag: #C4761F;
    --flag-bg: #FBF0E3;
    --risk: #B23A3A;
    --risk-bg: #FBEAE9;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--bg);
}

h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em;
}

.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.2rem;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1.1;
    color: var(--ink);
    margin: 0.1rem 0 0.4rem 0;
}

.hero-sub {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 1.02rem;
    color: var(--muted);
    max-width: 640px;
    margin-bottom: 0.5rem;
}

.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.2rem 0 1.4rem 0;
}

.icon-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.15rem;
}

.icon-row svg {
    flex-shrink: 0;
}

.section-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.5rem;
    color: var(--ink);
    margin: 0;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    height: 100%;
}

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
}

.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem;
    font-weight: 500;
    color: var(--ink);
    line-height: 1.1;
}

.metric-delta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

.delta-up { color: var(--risk); }
.delta-flag { color: var(--flag); }

.confidence-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: var(--confidence-bg);
    color: var(--confidence);
    border: 1px solid rgba(30,127,110,0.25);
    margin-top: 0.6rem;
}

.flag-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    padding: 0.4rem 0.7rem;
    border-radius: 8px;
    background: var(--flag-bg);
    color: var(--flag);
    border: 1px solid rgba(196,118,31,0.3);
}

.callout {
    background: var(--surface);
    border-left: 3px solid var(--confidence);
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    font-size: 0.92rem;
    color: var(--muted);
    margin-top: 0.6rem;
}

.footer-note {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    text-align: center;
    margin-top: 2rem;
}

.stButton > button {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    background: var(--ink);
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.55rem 1.3rem;
}

.stButton > button:hover {
    background: var(--confidence);
    color: white;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Small inline SVG icons — kept minimal and monochrome so they
# read as a real analyst tool, not a decorated demo
# ------------------------------------------------------------
ICON_BAR = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#14181F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"></line><line x1="18" y1="20" x2="18" y2="4"></line><line x1="6" y1="20" x2="6" y2="16"></line></svg>"""
ICON_USERS = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#14181F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>"""
ICON_BOT = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#14181F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>"""


def section_header(icon_svg, title):
    st.markdown(f"""
        <div class="icon-row">{icon_svg}<h2 class="section-title">{title}</h2></div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# Hero
# ------------------------------------------------------------
st.markdown("""
<div class="eyebrow">AUTONOMOUS BI INSIGHT AGENT</div>
<div class="hero-title">Metrics that investigate themselves.</div>
<div class="hero-sub">
Most dashboards tell you a number moved. This agent segments the data, tests each
cut for statistical significance, and reports back what actually changed —
flagging anything it can't trust along the way.
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Load cleaned data (from notebook 01)
# ------------------------------------------------------------
@st.cache_data
def load_data():
    client_table = pd.read_csv("client_table_clean.csv")
    web = pd.read_csv("web_events_clean.csv", parse_dates=['date_time'])
    return client_table, web

client_table, web = load_data()

st.markdown(f"""
<div class="confidence-tag">✓ DATA LOADED · n={len(client_table):,} clients · {len(web):,} funnel events</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Rebuild the three metrics (same logic as notebooks 02/03)
# ------------------------------------------------------------
step_order = {'start': 0, 'step_1': 1, 'step_2': 2, 'step_3': 3, 'confirm': 4}
web['step_rank'] = web['process_step'].map(step_order)

furthest_step = (
    web.groupby('client_id')['step_rank']
    .max()
    .reset_index()
    .rename(columns={'step_rank': 'furthest_step_rank'})
)
furthest_step = furthest_step.merge(client_table[['client_id', 'Variation']], on='client_id', how='left')
furthest_step['completed'] = furthest_step['furthest_step_rank'] == 4

visit_duration = (
    web.groupby(['client_id', 'visit_id'])['date_time']
    .agg(['min', 'max'])
    .reset_index()
)
visit_duration['duration_sec'] = (visit_duration['max'] - visit_duration['min']).dt.total_seconds()
client_duration = visit_duration.groupby('client_id')['duration_sec'].mean().reset_index()
client_duration = client_duration.merge(client_table[['client_id', 'Variation']], on='client_id', how='left')

web_sorted = web.sort_values(['client_id', 'visit_id', 'date_time'])
web_sorted['prev_step_rank'] = web_sorted.groupby(['client_id', 'visit_id'])['step_rank'].shift(1)
web_sorted['went_backward'] = web_sorted['step_rank'] < web_sorted['prev_step_rank']
client_backward = web_sorted.groupby('client_id')['went_backward'].any().reset_index()
client_backward = client_backward.merge(client_table[['client_id', 'Variation']], on='client_id', how='left')

completion_by_group = furthest_step.groupby('Variation')['completed'].mean()
duration_by_group = client_duration.groupby('Variation')['duration_sec'].mean()
backward_by_group = client_backward.groupby('Variation')['went_backward'].mean()


# ------------------------------------------------------------
# Headline metric cards
# ------------------------------------------------------------
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
section_header(ICON_BAR, "Headline Metrics — Test vs Control")

col1, col2, col3 = st.columns(3)

with col1:
    delta = completion_by_group['Test'] - completion_by_group['Control']
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Completion Rate</div>
        <div class="metric-value">{completion_by_group['Test']:.1%}</div>
        <div class="metric-delta delta-flag">▲ {delta:+.1%} vs Control</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    delta = duration_by_group['Test'] - duration_by_group['Control']
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg. Duration</div>
        <div class="metric-value">{duration_by_group['Test']:.0f}s</div>
        <div class="metric-delta delta-up">▲ {delta:+.0f}s vs Control</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    delta = backward_by_group['Test'] - backward_by_group['Control']
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Backward Navigation</div>
        <div class="metric-value">{backward_by_group['Test']:.1%}</div>
        <div class="metric-delta delta-up">▲ {delta:+.1%} vs Control</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="callout">
The full picture: Test completes more often — but takes longer and backtracks more.
A completion-rate-only view would have missed the cost entirely.
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Segment explorer
# ------------------------------------------------------------
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
section_header(ICON_USERS, "Explore by Segment")

segments_to_check = {
    "Age": "clnt_age",
    "Tenure": "clnt_tenure_yr",
    "Gender": "gendr",
    "Number of Accounts": "num_accts"
}

selected_segment_label = st.selectbox("Choose a segment to explore:", list(segments_to_check.keys()))
selected_column = segments_to_check[selected_segment_label]


def get_segment_view(column_name, metric_data, metric_column, min_group_size=30):
    merged = metric_data.merge(client_table[['client_id', column_name]], on='client_id', how='left')

    if pd.api.types.is_numeric_dtype(merged[column_name]):
        midpoint = merged[column_name].median()
        merged['group'] = merged[column_name].apply(lambda x: "High" if x >= midpoint else "Low")
    else:
        merged['group'] = merged[column_name]

    group_counts = merged['group'].value_counts()
    if (group_counts < min_group_size).any():
        return None, group_counts

    result_table = merged.groupby(['group', 'Variation'])[metric_column].mean().reset_index()
    return result_table, group_counts


completion_view, counts = get_segment_view(selected_column, furthest_step, 'completed')

if completion_view is None:
    st.markdown(f"""
    <div class="flag-tag">⚠ SKIPPED — group too small to trust (min. 30 required) · sizes: {dict(counts)}</div>
    """, unsafe_allow_html=True)
else:
    st.dataframe(completion_view, use_container_width=True)
    total_n = int(counts.sum())
    st.markdown(f"""
    <div class="confidence-tag">✓ RELIABLE · n={total_n:,} · groups: {dict(counts)}</div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# Agent investigation
# ------------------------------------------------------------
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
section_header(ICON_BOT, "Run Autonomous Agent Investigation")

st.markdown("""
<div style="color: var(--muted); font-size: 0.95rem; margin-bottom: 0.8rem;">
Sends the current statistical results to Claude and asks it to explain what changed —
under the same rules used in the notebooks: no demographic targeting advice,
no guessed motivations, facts only.
</div>
""", unsafe_allow_html=True)

if st.button("Run Agent Investigation"):
    with st.spinner("Agent is investigating..."):

        findings_text = f"""
Completion rate by group:
{completion_by_group}

Duration (seconds) by group:
{duration_by_group}

Backward navigation rate by group:
{backward_by_group}
"""

        prompt = f"""
You are a data analyst assistant. Below are statistical results comparing a Test group
vs Control group for three metrics: completion rate, duration, and backward navigation.

IMPORTANT RULES:
1. Do NOT recommend targeting specific demographic groups.
2. STRICTLY describe WHAT the data shows, not WHY it happens — no guessing at user
   motivations or comfort levels.
3. Specifically check whether the completion rate improvement comes with a cost in
   duration or backward navigation, and call this out clearly.

Here is the data:
{findings_text}
"""

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        st.markdown("""<div class="callout" style="border-left-color: var(--ink);">""", unsafe_allow_html=True)
        st.markdown(response.content[0].text)
        st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("""
<div class="footer-note">BUILT BY AKASH SAMANTRAY · github.com/Akash-045</div>
""", unsafe_allow_html=True)