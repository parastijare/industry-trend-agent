import streamlit as st
import json
from agents import trend_researcher, signal_extractor, report_writer, llm_judge

st.set_page_config(page_title="TrendPulse AI", page_icon="📈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background-color: #020817;
    background-image:
        url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop'),
        linear-gradient(180deg, rgba(2,8,23,0.92) 0%, rgba(2,8,23,0.97) 100%);
    background-blend-mode: overlay;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 2rem;
    background: rgba(255,255,255,0.03);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0;
}
.nav-logo {
    font-size: 1.3rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.02em;
}
.nav-logo span { color: #0ea5e9; }
.nav-pills { display: flex; gap: 0.5rem; }
.nav-pill {
    background: rgba(14,165,233,0.1);
    border: 1px solid rgba(14,165,233,0.2);
    color: #7dd3fc;
    border-radius: 999px;
    padding: 0.25rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
}

.hero-section {
    text-align: center;
    padding: 5rem 2rem 3rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(14,165,233,0.08);
    border: 1px solid rgba(14,165,233,0.25);
    color: #38bdf8;
    border-radius: 999px;
    padding: 0.3rem 1.1rem;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 1rem;
}
.hero-title span {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #64748b;
    font-size: 1.1rem;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-top: 2rem;
}
.stat-item { text-align: center; }
.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #f8fafc;
}
.stat-label {
    color: #475569;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.input-section {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin: 1rem 0 2rem;
    backdrop-filter: blur(20px);
}
.input-label {
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.6rem;
}

.pipeline-header {
    color: #475569;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
}
.pipeline-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.4rem;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.pipeline-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0ea5e9, #6366f1);
    border-radius: 2px 2px 0 0;
}
.pipeline-card .step {
    font-size: 0.72rem;
    font-weight: 700;
    color: #0ea5e9;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
}
.pipeline-card .name {
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.3rem;
}
.pipeline-card .desc {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.5;
}
.pipeline-card .icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
}

.signal-item {
    background: rgba(14,165,233,0.04);
    border: 1px solid rgba(14,165,233,0.12);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 0.8rem;
}
.signal-num {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: white;
    font-weight: 800;
    font-size: 0.85rem;
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
}
.signal-title {
    color: #f1f5f9;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
}
.signal-desc { color: #64748b; font-size: 0.85rem; line-height: 1.5; }
.signal-meta { margin-top: 0.4rem; display: flex; gap: 1rem; flex-wrap: wrap; }
.signal-impact { color: #94a3b8; font-size: 0.8rem; }
.conf-high   { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.2); border-radius: 999px; padding: 0.1rem 0.6rem; font-size: 0.72rem; font-weight: 700; }
.conf-medium { background: rgba(245,158,11,0.1);  color: #f59e0b; border: 1px solid rgba(245,158,11,0.2);  border-radius: 999px; padding: 0.1rem 0.6rem; font-size: 0.72rem; font-weight: 700; }
.conf-low    { background: rgba(239,68,68,0.1);   color: #ef4444; border: 1px solid rgba(239,68,68,0.2);   border-radius: 999px; padding: 0.1rem 0.6rem; font-size: 0.72rem; font-weight: 700; }

.report-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 2.5rem;
    color: #cbd5e1;
    line-height: 1.8;
    font-size: 0.95rem;
}
.report-container h1 { color: #f8fafc; font-size: 1.6rem; font-weight: 800; border-bottom: 1px solid rgba(255,255,255,0.07); padding-bottom: 0.8rem; }
.report-container h2 { color: #38bdf8; font-size: 1.15rem; font-weight: 700; margin-top: 1.8rem; }
.report-container ul { color: #94a3b8; }
.report-container strong { color: #e2e8f0; }

.overall-score {
    background: linear-gradient(135deg, rgba(14,165,233,0.1), rgba(99,102,241,0.1));
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.overall-number {
    font-size: 5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.overall-label {
    color: #475569;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.5rem;
}
.score-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    height: 100%;
}
.score-val {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0ea5e9;
}
.score-name {
    color: #475569;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.3rem 0;
    font-weight: 700;
}
.score-reason {
    color: #64748b;
    font-size: 0.78rem;
    line-height: 1.5;
    margin-top: 0.5rem;
}
.judge-summary {
    background: rgba(99,102,241,0.06);
    border-left: 3px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 1.1rem 1.4rem;
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.7;
    margin: 1.2rem 0;
}
.strength-card {
    background: rgba(16,185,129,0.06);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #10b981;
    font-size: 0.88rem;
    line-height: 1.6;
}
.improve-card {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #f59e0b;
    font-size: 0.88rem;
    line-height: 1.6;
}

.sec-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1rem;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    font-family: 'Manrope', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 2rem !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
.stExpander {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
    border-radius: 999px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Trend<span>Pulse</span> AI</div>
    <div class="nav-pills">
        <span class="nav-pill">Groq LLM</span>
        <span class="nav-pill">Tavily Search</span>
        <span class="nav-pill">4 Agents</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-eyebrow">⚡ Real-Time Industry Intelligence</div>
    <div class="hero-title">Know What's Happening<br>in Any <span>Industry</span></div>
    <div class="hero-sub">
        Four specialized AI agents research, extract, write, and evaluate
        a complete trend report on any sector in under 60 seconds.
    </div>
    <div class="hero-stats">
        <div class="stat-item">
            <div class="stat-number">4</div>
            <div class="stat-label">AI Agents</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">5</div>
            <div class="stat-label">Trend Signals</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">60s</div>
            <div class="stat-label">Avg Report Time</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">3</div>
            <div class="stat-label">Judge Criteria</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline Cards ────────────────────────────────────────────────
st.markdown("<div class='pipeline-header'>Agent Pipeline</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
cards = [
    ("🔍", "Step 01", "Trend Researcher",  "Searches the web via Tavily for latest news, funding and forecasts"),
    ("📡", "Step 02", "Signal Extractor",  "Identifies the top 5 most impactful trend signals as structured data"),
    ("✍️", "Step 03", "Report Writer",     "Synthesizes research into a professional executive-ready report"),
    ("⚖️", "Step 04", "LLM Judge",         "Scores the report on accuracy, relevance and analytical depth"),
]
for col, (icon, step, name, desc) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(f"""
        <div class="pipeline-card">
            <div class="icon">{icon}</div>
            <div class="step">{step}</div>
            <div class="name">{name}</div>
            <div class="desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("<div class='input-label'>Target Sector</div>", unsafe_allow_html=True)
col_in, col_btn = st.columns([4, 1])
with col_in:
    sector = st.text_input(
        "Sector",
        placeholder="e.g.  FinTech  ·  HealthTech  ·  EdTech  ·  CleanTech  ·  SpaceTech",
        label_visibility="collapsed"
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("Analyse →")
st.markdown("</div>", unsafe_allow_html=True)

# ── Run Pipeline ──────────────────────────────────────────────────
if run and sector:

    with st.status(f"Analysing {sector}...", expanded=True) as status:
        def log(msg): status.write(f"⏳ {msg}")
        research    = trend_researcher(sector, log)
        signals_raw = signal_extractor(sector, research, log)
        report      = report_writer(sector, research, signals_raw, log)
        judge       = llm_judge(sector, report, log)
        status.update(label=f"✅ {sector} report ready!", state="complete")

    # Agent 1
    with st.expander("🔍 Raw Research Data — Agent 1"):
        st.markdown(f"<div style='color:#64748b;font-size:0.88rem;line-height:1.8'>{research}</div>",
                    unsafe_allow_html=True)

    # Agent 2
    st.markdown("<div class='sec-title'>📡 Top 5 Trend Signals</div>", unsafe_allow_html=True)
    try:
        clean = signals_raw.strip().replace("```json", "").replace("```", "")
        data  = json.loads(clean)
        for s in data.get("signals", []):
            conf       = s.get("confidence", "Medium").lower()
            conf_class = f"conf-{conf}"
            st.markdown(f"""
            <div class="signal-item">
                <div class="signal-num">{s['rank']}</div>
                <div class="signal-content">
                    <div class="signal-title">{s['title']}</div>
                    <div class="signal-desc">{s['description']}</div>
                    <div class="signal-meta">
                        <span class="signal-impact">📌 {s['why_it_matters']}</span>
                        <span class="{conf_class}">{s['confidence']}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
    except Exception:
        st.write(signals_raw)

    # Agent 3
    st.markdown("<div class='sec-title'>📄 Full Trend Report</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='report-container'>{report}</div>", unsafe_allow_html=True)

    # Agent 4
    st.markdown("<div class='sec-title'>⚖️ Quality Evaluation — LLM Judge</div>", unsafe_allow_html=True)

    scores  = judge.get("scores", {})
    overall = judge.get("overall_score", 0)

    left, right = st.columns([1, 2])

    with left:
        st.markdown(f"""
        <div class="overall-score">
            <div class="overall-number">{overall}</div>
            <div style="color:#64748b;font-size:1rem;margin-top:0.2rem">out of 5</div>
            <div class="overall-label">Overall Score</div>
        </div>""", unsafe_allow_html=True)

    with right:
        sc1, sc2, sc3 = st.columns(3)
        for col, key, label in zip(
            [sc1, sc2, sc3],
            ["accuracy", "relevance", "analytical_depth"],
            ["Accuracy", "Relevance", "Depth"]
        ):
            d = scores.get(key, {})
            with col:
                st.markdown(f"""
                <div class="score-card">
                    <div class="score-val">{d.get('score', 0)}/5</div>
                    <div class="score-name">{label}</div>
                    <div class="score-reason">{d.get('reasoning', '')}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown(f"<div class='judge-summary'>{judge.get('summary', '')}</div>", unsafe_allow_html=True)

    fc, ic = st.columns(2)
    with fc:
        st.markdown(f"<div class='strength-card'><b>✦ Top Strength</b><br>{judge.get('top_strength', '')}</div>",
                    unsafe_allow_html=True)
    with ic:
        st.markdown(f"<div class='improve-card'><b>△ Key Improvement</b><br>{judge.get('top_improvement', '')}</div>",
                    unsafe_allow_html=True)

elif run and not sector:
    st.warning("Please enter a sector name to generate a report.")
