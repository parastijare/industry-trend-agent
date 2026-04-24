import streamlit as st
import json
from agents import trend_researcher, signal_extractor, report_writer, llm_judge

st.set_page_config(page_title="TrendPulse AI", page_icon="📈", layout="wide")

# Sidebar state
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background-color: #020817;
}

/* Sidebar */
.sidebar {
    position: fixed;
    top: 70px;
    left: 0;
    width: 260px;
    height: calc(100% - 70px);
    background: rgba(2,8,23,0.95);
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 1.5rem 1rem;
    transition: all 0.3s ease;
    z-index: 100;
}

.sidebar.closed {
    left: -240px;
}

/* Toggle button */
.toggle-btn {
    position: fixed;
    top: 90px;
    left: 260px;
    background: #0ea5e9;
    color: white;
    border-radius: 50%;
    width: 34px;
    height: 34px;
    border: none;
    cursor: pointer;
    z-index: 200;
}

.toggle-btn.closed {
    left: 10px;
}

/* Main content */
.main-content {
    margin-left: 280px;
    transition: all 0.3s ease;
}

.main-content.full {
    margin-left: 20px;
}

/* Cards */
.pipeline-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}

.pipeline-card .name {
    color: white;
    font-weight: 700;
}

.pipeline-card .desc {
    color: #64748b;
    font-size: 0.85rem;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    padding: 1rem 2rem;
    background: rgba(255,255,255,0.05);
}

.nav-logo {
    color: white;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
    <div class="nav-logo">TrendPulse AI</div>
</div>
""", unsafe_allow_html=True)

# Toggle logic
if st.button("⬅" if st.session_state.sidebar_open else "➡"):
    st.session_state.sidebar_open = not st.session_state.sidebar_open

# Sidebar
sidebar_class = "sidebar" if st.session_state.sidebar_open else "sidebar closed"

st.markdown(f"""
<div class="{sidebar_class}">
    <h4 style="color:white;">Agent Pipeline</h4>

    <div class="pipeline-card">
        🔍 <div class="name">Trend Researcher</div>
        <div class="desc">Fetches industry insights</div>
    </div>

    <div class="pipeline-card">
        📡 <div class="name">Signal Extractor</div>
        <div class="desc">Finds key signals</div>
    </div>

    <div class="pipeline-card">
        ✍️ <div class="name">Report Writer</div>
        <div class="desc">Builds report</div>
    </div>

    <div class="pipeline-card">
        ⚖️ <div class="name">LLM Judge</div>
        <div class="desc">Evaluates output</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main wrapper
main_class = "main-content" if st.session_state.sidebar_open else "main-content full"
st.markdown(f'<div class="{main_class}">', unsafe_allow_html=True)

# App UI
st.title("📈 TrendPulse AI")
st.write("AI-powered industry trend analysis using multi-agent pipeline.")

sector = st.text_input("Enter Industry (e.g. AI, FinTech, HealthTech)")
run = st.button("Analyse")

if run and sector:

    with st.spinner("Running agents..."):
        research = trend_researcher(sector, print)
        signals_raw = signal_extractor(sector, research, print)
        report = report_writer(sector, research, signals_raw, print)
        judge = llm_judge(sector, report, print)

    st.subheader("📡 Trend Signals")
    try:
        clean = signals_raw.strip().replace("```json", "").replace("```", "")
        data = json.loads(clean)

        for s in data.get("signals", []):
            st.markdown(f"**{s['title']}**")
            st.write(s["description"])
            st.caption(f"Impact: {s['why_it_matters']} | Confidence: {s['confidence']}")

    except:
        st.write(signals_raw)

    st.subheader("📄 Report")
    st.write(report)

    st.subheader("⚖️ Evaluation")
    st.write(judge)

elif run:
    st.warning("Please enter a sector.")

st.markdown("</div>", unsafe_allow_html=True)
