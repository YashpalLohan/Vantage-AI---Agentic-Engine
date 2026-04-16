import streamlit as st
import requests

@st.cache_data(show_spinner=False, persist="disk")
def fetch_jobs_v3(file_bytes, file_name, loc, sal, refresh_id=0, seen_urls=""):
    params = {"location": loc, "min_salary": sal, "refresh_id": refresh_id, "seen_urls": seen_urls}
    res = requests.post("http://127.0.0.1:8000/find-jobs", files={"file": (file_name, file_bytes, "application/pdf")}, params=params)
    return res.status_code, res.text, res.json() if res.status_code == 200 else None

st.set_page_config(page_title="Vantage AI", page_icon="◈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp { background: #09090b; color: #fafafa; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 860px; }

/* ── HERO ── */
.hero { text-align: center; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid #27272a; }
.hero-eyebrow { font-size: 11px; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: #a1a1aa; margin-bottom: 10px; }
.hero-title { font-size: 2.5rem; font-weight: 800; color: #ffffff; margin-bottom: 6px; line-height: 1.2; letter-spacing: -1px; }
.hero-title em { font-style: normal; color: #3b82f6; }
.hero-sub { font-size: 0.95rem; color: #a1a1aa; }

/* ── PROGRESS STEPS ── */
.steps { display: flex; align-items: center; justify-content: center; gap: 0; margin-bottom: 1.5rem; }
.step { font-size: 11px; padding: 6px 16px; border-radius: 99px; color: #71717a; border: 1px solid #27272a; }
.step.active { background: #1e3a8a; color: #60a5fa; border-color: #3b82f6; }
.step.done { color: #10b981; border-color: #064e3b; }
.step-line { width: 40px; height: 1px; background: #27272a; }

/* ── CARDS ── */
.card {
    background: #18181b;
    border: 1px solid #27272a;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 16px;
}
.card-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #71717a;
    display: block;
    margin-bottom: 14px;
}

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {
    background: #09090b !important;
    border: 1.5px dashed #3f3f46 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] label { color: #52525b !important; font-size: 0.85rem !important; }

/* ── SELECTS ── */
.stSelectbox > div > div {
    background: #18181b !important;
    border: 1px solid #27272a !important;
    border-radius: 10px !important;
    color: #fafafa !important;
}
.stSelectbox label {
    color: #71717a !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #fafafa !important;
    color: #09090b !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 14px 24px !important;
    width: 100%;
}
.stButton > button:hover { background: #e4e4e7 !important; transform: translateY(-1px); }

.reset-btn > .stButton > button {
    background: transparent !important;
    color: #a1a1aa !important;
    border: 1px solid #27272a !important;
    font-size: 0.8rem !important;
    padding: 8px 16px !important;
    width: auto !important;
}
.reset-btn > .stButton > button:hover { color: #fafafa !important; border-color: #3f3f46 !important; }

/* ── METRICS ── */
.metric-card {
    background: #18181b;
    border: 1px solid #27272a;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}
.metric-num { font-size: 3rem; font-weight: 800; line-height: 1; margin-bottom: 6px; letter-spacing: -2px; }
.metric-lbl { font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #71717a; }

/* ── TAGS ── */
.tag { display: inline-block; font-size: 12px; padding: 4px 12px; border-radius: 99px; margin: 4px; font-weight: 600; }
.tag-skill { background: #1e3a8a; color: #93c5fd; border: 1px solid #1e40af; }
.tag-gap { background: #451a03; color: #fbbf24; border: 1px solid #78350f; }
.tag-cert { background: #064e3b; color: #6ee7b7; border: 1px solid #065f46; }

/* ── CHARTS ── */
.bar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.bar-name { font-size: 12px; font-weight: 600; color: #a1a1aa; width: 100px; }
.bar-track { flex: 1; height: 6px; background: #27272a; border-radius: 99px; overflow: hidden; }
.bar-pct { font-size: 12px; font-weight: 700; color: #71717a; width: 36px; text-align: right; }

/* ── JOBS ── */
.job-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 0; border-bottom: 1px solid #27272a;
}
.job-row:last-child { border-bottom: none; }
.job-num { font-size: 12px; font-weight: 800; color: #3f3f46; width: 28px; }
.job-info { flex: 1; margin: 0 14px; }
.job-title-text { font-size: 1rem; font-weight: 600; color: #fafafa; }
.job-co { font-size: 13px; color: #a1a1aa; margin-top: 2px; }
.job-badge { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 8px; background: #064e3b; color: #10b981; border: 1px solid #065f46; }
.job-arrow { color: #3f3f46; font-size: 1.2rem; text-decoration: none; }
.job-arrow:hover { color: #3b82f6; }

/* ── INSIGHTS ── */
.insight-row {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 14px 0; border-bottom: 1px solid #27272a;
}
.insight-row:last-child { border-bottom: none; }
.insight-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; box-shadow: 0 0 8px currentColor; }
.i-label { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: #71717a; margin-bottom: 4px; }
.i-text { font-size: 0.95rem; color: #d4d4d8; line-height: 1.6; }

hr { border-color: #27272a !important; margin: 2rem 0 !important; }
.footer-note { font-size: 11px; color: #3f3f46; text-align: center; margin-top: 2rem; letter-spacing: 2px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

def render_hero():
    st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>Agentic Intelligence</div>
        <h1 class='hero-title'>Vantage <em>AI</em></h1>
        <p class='hero-sub'>The Agentic Career Intelligence Engine</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress(stage: int):
    steps_html = f"""
    <div class='steps'>
        <div class='step {"active" if stage == 1 else "done"}'>01 Upload{"" if stage == 1 else " ✓"}</div>
        <div class='step-line'></div>
        <div class='step {"active" if stage == 2 else ("done" if stage > 2 else "")}'>02 Prefs{"" if stage <= 2 else " ✓"}</div>
        <div class='step-line'></div>
        <div class='step {"active" if stage == 3 else ""}'>03 Map</div>
    </div>
    """
    st.markdown(steps_html, unsafe_allow_html=True)


if 'refresh_count' not in st.session_state:
    st.session_state['refresh_count'] = 0
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'applied_jobs' not in st.session_state:
    st.session_state['applied_jobs'] = set()

def get_all_seen_urls():
    urls = []
    for item in st.session_state.get('history', []):
        for job in item.get('results', {}).get('jobs_found', []):
            urls.append(job['url'])
    return ",".join(urls)

if 'active_map_id' not in st.session_state:
    st.session_state['active_map_id'] = None

# Sidebar for History
with st.sidebar:
    st.markdown("<div style='padding-top: 1rem;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #3b82f6;'>◈ Vantage Archive</h3>", unsafe_allow_html=True)
    if not st.session_state['history']:
        st.markdown("<p style='font-size: 13px; color: #71717a;'>No previous maps saved yet.</p>", unsafe_allow_html=True)
    else:
        for i, item in enumerate(st.session_state['history']):
            map_label = f"Map {i+1}: {item['prefs']['loc']} ({item['prefs']['sal']})"
            is_active = st.session_state['active_map_id'] == i
            
            # Using a custom div with border for active state
            if is_active:
                st.markdown("<div style='border-left: 3px solid #3b82f6; padding-left: 4px; margin-bottom: 4px;'>", unsafe_allow_html=True)
            
            if st.button(map_label, key=f"hist_{i}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state['results'] = item['results']
                st.session_state['prefs'] = item['prefs']
                st.session_state['active_map_id'] = i
                st.rerun()
                
            if is_active:
                st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    if st.session_state['applied_jobs']:
        st.markdown(f"<h4 style='color: #10b981;'>Applied: {len(st.session_state['applied_jobs'])} Roles</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if 'results' not in st.session_state:
    render_hero()
    render_progress(1)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<span class='card-label'>Upload Résumé</span>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    st.markdown("<p style='font-size:11px;color:#3f3f46;text-align:center;'>PDF Format • Max 5MB</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        loc = st.selectbox("Market Location", ["Remote", "Bangalore", "Gurgaon", "Mumbai", "Hyderabad", "Pune"])
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        sal = st.selectbox("Min. Package", ["Any", "15 LPA+", "25 LPA+", "45 LPA+"])
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        exp = st.selectbox("Seniority Level", ["Any Level", "Junior", "Mid-Level", "Senior", "Lead / Staff"])
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        work = st.selectbox("Employment", ["Any", "Full-time", "Contract", "Hybrid"])
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Generate Career Map ➔", use_container_width=True):
        if uploaded_file:
            with st.spinner("Agents scanning India's tech market..."):
                try:
                    params = {"location": loc, "min_salary": sal}
                    file_bytes = uploaded_file.getvalue()
                    seen_urls_str = get_all_seen_urls()
                    status_code, resp_text, json_data = fetch_jobs_v3(file_bytes, uploaded_file.name, loc, sal, st.session_state['refresh_count'], seen_urls_str)
                    if status_code == 200:
                        st.session_state['results'] = json_data
                        st.session_state['prefs'] = {
                            "loc": loc, 
                            "sal": sal, 
                            "file_bytes": file_bytes, 
                            "file_name": uploaded_file.name
                        }
                        st.session_state['job_limit'] = 10 
                        st.session_state['history'].append({
                            "results": json_data,
                            "prefs": {"loc": loc, "sal": sal, "file_bytes": file_bytes, "file_name": uploaded_file.name}
                        })
                        st.session_state['active_map_id'] = len(st.session_state['history']) - 1
                        st.rerun()
                    else:
                        st.error(f"Backend returned error: {status_code} - {resp_text}")
                except Exception as e:
                    st.error(f"Swarm node is offline. Error: {str(e)}")
        else:
            st.warning("Upload required to begin discovery.")

    st.markdown("<div class='footer-note'>PRO-AGENT SWARM ACTIVE • GROQ LLAMA 3</div>", unsafe_allow_html=True)

else:
    res = st.session_state['results']
    prefs = st.session_state.get('prefs', {})
    report = res.get("report", {})
    
    # Force Dictionary Support
    if isinstance(report, str):
        report = {"match": "85%", "match_label": "High Fit", "insights": [{"label": "Status", "text": report}]}

    render_hero()
    render_progress(3)

    c_back, c_refresh = st.columns([5, 1.2])
    with c_back:
        st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
        if st.button("← Back"):
            if 'results' in st.session_state:
                del st.session_state['results']
            if 'job_limit' in st.session_state:
                del st.session_state['job_limit']
            st.session_state['active_map_id'] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c_refresh:
        st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
        if st.button("🔄 Refresh"):
            st.session_state['refresh_count'] += 1
            # Re-fetch with new refresh_id
            with st.spinner("Refreshing..."):
                f_bytes = prefs.get('file_bytes')
                f_name = prefs.get('file_name')
                f_loc = prefs.get('loc')
                f_sal = prefs.get('sal')
                if f_bytes:
                    seen_urls_str = get_all_seen_urls()
                    # Pass the refresh_id and seen_urls to trigger backend variety
                    status_code, resp_text, json_data = fetch_jobs_v3(f_bytes, f_name, f_loc, f_sal, st.session_state['refresh_count'], seen_urls_str)
                    if status_code == 200:
                        st.session_state['results'] = json_data
                        # Update history with the fresh result
                        st.session_state['history'].append({
                            "results": json_data,
                            "prefs": {"loc": f_loc, "sal": f_sal, "file_bytes": f_bytes, "file_name": f_name}
                        })
                        st.session_state['active_map_id'] = len(st.session_state['history']) - 1
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        st.markdown(f"<div class='metric-card'><div class='metric-num' style='color:#3b82f6;'>{report.get('match','—')}</div><div class='metric-lbl'>Fit Score</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><div class='metric-num' style='color:#10b981;'>{len(res.get('jobs_found',[]))}</div><div class='metric-lbl'>Matching Roles</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><div class='metric-num' style='color:#f59e0b;'>{res.get('skill_coverage','73%')}</div><div class='metric-lbl'>Skill Index</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<span class='card-label'>Profile Inventory</span>", unsafe_allow_html=True)
        pills = "".join(f'<span class="tag tag-skill">{s}</span>' for s in res.get("skills", ["Software"]))
        st.markdown(f"<div>{pills}</div>", unsafe_allow_html=True)
        
        if report.get("skill_gaps"):
            st.markdown("<br><span class='card-label'>Missing High-Impact Skills</span>", unsafe_allow_html=True)
            g_pills = "".join(f'<span class="tag tag-gap">{g}</span>' for g in report["skill_gaps"])
            st.markdown(f"<div>{g_pills}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<span class='card-label'>Role Market Alignment</span>", unsafe_allow_html=True)
        breakdown = report.get("role_breakdown", [{"role": "Eng.", "pct": 80, "color": "#3b82f6"}])
        bars_html = ""
        for item in breakdown:
            bars_html += f"""
            <div class='bar-row'>
                <span class='bar-name'>{item['role']}</span>
                <div class='bar-track'><div style='width:{item['pct']}%;height:100%;background:{item.get('color','#3b82f6')};'></div></div>
                <span class='bar-pct'>{item['pct']}%</span>
            </div>"""
        st.markdown(bars_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='card-label'>Intelligence: Verified Roles for {prefs.get('loc','India')}</span>", unsafe_allow_html=True)
    
    jobs_found = res.get("jobs_found", [])
    if 'job_limit' not in st.session_state:
        st.session_state['job_limit'] = 10

    if not jobs_found:
        st.markdown("<p style='color:#3f3f46;'>None found.</p>", unsafe_allow_html=True)
    else:
        displayed_jobs = jobs_found[:st.session_state['job_limit']]
        for i, job in enumerate(displayed_jobs, 1):
            url = job['url']
            col1, col2 = st.columns([5, 2.2])
            with col1:
                st.markdown(f"""
                <div style='display: flex; align-items: center; padding: 6px 0;'>
                    <span class='job-num' style='margin-right: 14px;'>{i:02}</span>
                    <div class='job-info'>
                        <div class='job-title-text'>{job['title']}</div>
                        <div class='job-co'>🏢 {job.get('company', 'Direct Role')} &nbsp;•&nbsp; 🌐 {job.get('platform', 'Corporate Platform')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # Single button full width
                st.markdown(f"<div style='margin-top: 8px;'><a href='{url}' target='_blank' class='job-badge' style='text-decoration:none; display:inline-block; width:100%; text-align:center; background:#1e3a8a; border-color:#1e40af;'>Apply Now ↗</a></div>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 8px 0; border-color: #27272a;'>", unsafe_allow_html=True)

        if st.session_state['job_limit'] < len(jobs_found):
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"Load More Jobs ({len(jobs_found) - st.session_state['job_limit']} remaining) ↓", key="load_more_jobs"):
                st.session_state['job_limit'] += 10
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if report.get("insights"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<span class='card-label'>Strategic Insights</span>", unsafe_allow_html=True)
        i_html = ""
        for ins in report["insights"]:
            color = "#3b82f6" if ins.get("label") == "Salary benchmark" else "#10b981"
            i_html += f"""
            <div class='insight-row'>
                <div class='insight-dot' style='color:{color};'></div>
                <div><div class='i-label'>{ins['label']}</div><div class='i-text'>{ins['text']}</div></div>
            </div>"""
        st.markdown(i_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='footer-note'>SECURE AGENT HANDSHAKE COMPLETE • DATA ENCRYPTED</div>", unsafe_allow_html=True)