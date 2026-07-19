"""
common.py
Modul bersama untuk aplikasi PulmoVision (multi-page Streamlit app).
Berisi: tema CSS "Clinical Tech", komponen UI (card, info-box, metric-card, dsb),
logo/icon (SVG, bukan emoji), dan navigasi sidebar yang dipakai di semua halaman.
"""

import streamlit as st

# ─────────────────────────────────────────────
# CSS TEMA — "Clinical Tech" (biru-teal)
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

:root {
    --blue-primary:  #2E86AB;
    --blue-dark:     #1B4F72;
    --blue-darker:   #112E40;
    --blue-light:    #8FC1DD;
    --blue-pale:     #E8F2F8;
    --blue-mist:     #F3F8FB;
    --cream:         #F7F8FA;
    --white:         #FFFFFF;
    --text-dark:     #16242B;
    --text-mid:      #3D5A66;
    --text-light:    #6B8694;
    --border:        rgba(46, 134, 171, 0.2);
    --border-strong: rgba(46, 134, 171, 0.35);
    --shadow-sm:      0 2px 12px rgba(27, 79, 114, 0.07);
    --shadow-md:      0 6px 24px rgba(27, 79, 114, 0.13);
    --shadow-lg:      0 16px 48px rgba(27, 79, 114, 0.18);
    --radius-sm:      10px;
    --radius-md:      16px;
    --radius-lg:      20px;
    --transition:     all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-testid="stAppViewContainer"]::-webkit-scrollbar,
[data-testid="stSidebar"]::-webkit-scrollbar,
::-webkit-scrollbar { width: 6px; height: 6px; }

[data-testid="stAppViewContainer"]::-webkit-scrollbar-track,
[data-testid="stSidebar"]::-webkit-scrollbar-track,
::-webkit-scrollbar-track { background: var(--blue-mist); }

[data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb,
[data-testid="stSidebar"]::-webkit-scrollbar-thumb,
::-webkit-scrollbar-thumb {
    background: var(--blue-light);
    border-radius: 99px;
    border: 2px solid var(--blue-mist);
}

[data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb:hover,
[data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover,
::-webkit-scrollbar-thumb:hover { background: var(--blue-primary); }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-dark);
}

.stApp {
    background-color: var(--cream);
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 200px 200px;
}

#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
[data-testid="stAppDeployButton"] { display: none !important; }

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, var(--blue-darker) 0%, var(--blue-dark) 55%, #1f5f86 100%);
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    position: relative;
    overflow: hidden;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(46,134,171,0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

[data-testid="stSidebar"] * { color: #D6E9F4 !important; }

[data-testid="stSidebar"] [data-testid="stImage"] {
    display: flex !important;
    justify-content: center !important;
    margin: 0 auto !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
    background-color: var(--blue-light) !important;
}

[data-testid="stSidebar"] .sidebar-section-title {
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    color: rgba(214, 233, 244, 0.55) !important;
    margin: 1.4rem 0 0.5rem !important;
}

.sidebar-logo-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 0.25rem;
}

.sidebar-logo-mark {
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
}

.sidebar-logo-title {
    text-align: center;
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #fff;
    margin-top: 0.55rem;
}

.sidebar-footer {
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
    padding: 0.85rem 1rem;
    background: rgba(0,0,0,0.2);
    border-radius: var(--radius-sm);
    border: 1px solid rgba(255,255,255,0.07);
}

.sidebar-footer p {
    font-size: 0.7rem !important;
    color: rgba(214,233,244,0.5) !important;
    margin: 0 !important;
    line-height: 1.6;
}

/* TYPOGRAPHY */
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 { color: var(--blue-dark) !important; }

/* SECTION TITLE WITH ICON */
.section-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin: 0 0 0.9rem !important;
}
.section-title .icon-chip {
    flex-shrink: 0;
    width: 30px; height: 30px;
    border-radius: 9px;
    background: var(--blue-pale);
    border: 1px solid var(--border-strong);
    display: flex; align-items: center; justify-content: center;
}
.section-title .icon-chip svg { width: 16px; height: 16px; }
.section-title h3 { margin: 0 !important; font-size: 1.15rem !important; }

/* PAGE HEADER */
.page-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.75rem;
    border-bottom: 1px solid var(--border);
    position: relative;
}

.page-header::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 72px; height: 2px;
    background: linear-gradient(to right, var(--blue-primary), var(--blue-light));
    border-radius: 99px;
}

.page-header .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--blue-pale);
    color: var(--blue-dark);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 99px;
    border: 1px solid var(--border-strong);
    margin-bottom: 0.85rem;
}

.page-header h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: clamp(1.9rem, 4vw, 2.75rem) !important;
    font-weight: 400 !important;
    color: var(--blue-dark) !important;
    line-height: 1.15 !important;
    margin: 0 0 0.5rem !important;
    letter-spacing: -0.5px;
}

.page-header .subtitle {
    color: var(--text-light);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
    font-style: italic;
}

/* CARDS */
.card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(to right, var(--blue-primary), var(--blue-light));
    opacity: 0;
    transition: var(--transition);
}

.card:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); border-color: var(--border-strong); }
.card:hover::before { opacity: 1; }

.card h3 {
    font-family: 'DM Serif Display', serif;
    color: var(--blue-dark);
    font-size: 1.2rem;
    font-weight: 400;
    margin: 0 0 0.75rem;
}

.card p { color: var(--text-mid); font-size: 0.88rem; line-height: 1.75; margin: 0; }

/* METRIC CARDS */
.metric-card {
    background: linear-gradient(135deg, var(--blue-darker) 0%, var(--blue-dark) 60%, #2b7095 100%);
    border-radius: var(--radius-md);
    padding: 1.6rem 1.5rem;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    transition: var(--transition);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}

.metric-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }

.metric-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    font-weight: 400;
    color: #fff;
    line-height: 1;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.metric-card .label {
    font-size: 0.72rem;
    color: var(--blue-light);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    position: relative;
    z-index: 1;
}

.metric-card .delta {
    font-size: 0.78rem;
    color: rgba(214, 233, 244, 0.75);
    margin-top: 0.4rem;
    position: relative;
    z-index: 1;
}

/* INFO BOX */
.info-box {
    background: linear-gradient(to right, var(--blue-pale), var(--blue-mist));
    border: 1px solid rgba(46, 134, 171, 0.25);
    border-left: 4px solid var(--blue-primary);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 1.25rem 1.5rem;
    margin: 1.25rem 0;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
}
.info-box .icon-chip {
    flex-shrink: 0;
    width: 26px; height: 26px;
    margin-top: 1px;
    border-radius: 8px;
    background: rgba(46,134,171,0.14);
    display: flex; align-items: center; justify-content: center;
}
.info-box .icon-chip svg { width: 14px; height: 14px; }
.info-box p { margin: 0; color: var(--blue-darker); font-size: 0.88rem; line-height: 1.7; }

/* EXPANDER */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    background: var(--white) !important;
    margin-bottom: 0.75rem !important;
    box-shadow: var(--shadow-sm);
}

[data-testid="stExpander"] summary { padding: 1rem 1.25rem !important; font-weight: 500 !important; color: var(--text-dark) !important; font-size: 0.92rem !important; }
[data-testid="stExpander"] summary:hover { background: var(--blue-mist) !important; color: var(--blue-dark) !important; }
[data-testid="stExpander"] [data-testid="stExpanderDetails"] * { color: var(--text-dark) !important; }
[data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] td,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] th { color: var(--text-mid) !important; }
[data-testid="stExpander"] [data-testid="stExpanderDetails"] code { color: var(--blue-dark) !important; background: var(--blue-pale) !important; }

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--blue-primary) !important;
    border-radius: var(--radius-md) !important;
    background: var(--blue-mist) !important;
    padding: 1.5rem !important;
    transition: var(--transition);
}
[data-testid="stFileUploader"]:hover { background: var(--blue-pale) !important; border-color: var(--blue-dark) !important; }

/* BUTTONS */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--blue-primary) 0%, var(--blue-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.75rem !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.4px !important;
    transition: var(--transition) !important;
    box-shadow: 0 4px 14px rgba(27,79,114,0.28) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(27,79,114,0.38) !important;
    filter: brightness(1.05) !important;
}

/* ALERTS */
.stAlert { border-radius: var(--radius-sm) !important; border: 1px solid var(--border) !important; font-size: 0.875rem !important; }
.stSuccess { background: var(--blue-mist) !important; border-color: var(--blue-light) !important; color: var(--blue-darker) !important; }

/* DATAFRAME / TABLE */
[data-testid="stDataFrame"], [data-testid="stTable"] { border-radius: var(--radius-sm) !important; border: 1px solid var(--border) !important; overflow: hidden; }

/* DIVIDER */
hr.section-divider {
    height: 1px !important;
    background: linear-gradient(to right, var(--blue-primary), var(--blue-light), transparent) !important;
    margin: 2.25rem 0 !important;
    border: none !important;
    opacity: 0.8 !important;
}

/* TAG PILL */
.tag {
    display: inline-block;
    background: var(--blue-pale);
    color: var(--blue-dark);
    border: 1px solid var(--border-strong);
    border-radius: 99px;
    padding: 3px 13px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px;
    letter-spacing: 0.3px;
}

/* TIMELINE / STEP LIST */
.step-row {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    padding: 0.85rem 0;
    border-bottom: 1px dashed var(--border);
}
.step-row:last-child { border-bottom: none; }
.step-num {
    flex-shrink: 0;
    width: 28px; height: 28px;
    border-radius: 50%;
    background: var(--blue-pale);
    border: 1px solid var(--border-strong);
    color: var(--blue-dark);
    font-weight: 700;
    font-size: 0.8rem;
    display: flex; align-items: center; justify-content: center;
}
.step-text b { color: var(--text-dark); }
.step-text p { margin: 0.15rem 0 0; color: var(--text-mid); font-size: 0.85rem; line-height: 1.65; }

/* NATIVE METRICS */
[data-testid="metric-container"] {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1.25rem 1.5rem !important;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}
[data-testid="metric-container"]:hover { border-color: var(--border-strong); box-shadow: var(--shadow-md); transform: translateY(-2px); }
[data-testid="metric-container"] label { color: var(--text-light) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 1.1px; font-weight: 700 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { color: var(--blue-dark) !important; font-family: 'DM Serif Display', serif !important; }
[data-testid="stMetricDelta"], [data-testid="stMetricDelta"] * { color: var(--blue-primary) !important; }

[data-testid="collapsedControl"] {
    background-color: var(--blue-mist) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important;
    color: var(--blue-dark) !important;
}
[data-testid="collapsedControl"] svg { fill: var(--blue-dark) !important; }

.stSpinner > div { border-top-color: var(--blue-primary) !important; }

/* SIDEBAR NAV BUTTONS (st.page_link) */
[data-testid="stSidebar"] [data-testid="stPageLink"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 0.9rem !important;
    margin-bottom: 0.5rem !important;
    transition: var(--transition) !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
    background: rgba(255,255,255,0.14) !important;
    border-color: rgba(255,255,255,0.3) !important;
    transform: translateX(3px);
}
[data-testid="stSidebar"] [data-testid="stPageLink"] p {
    color: #D6E9F4 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] {
    background: rgba(255,255,255,0.18) !important;
    border-color: var(--blue-light) !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* HIGHLIGHT RESULT CARD */
.result-card {
    background: linear-gradient(135deg, var(--blue-darker) 0%, var(--blue-dark) 55%, #2b7095 100%);
    border-radius: var(--radius-lg);
    padding: 1.75rem 1.5rem;
    text-align: center;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: var(--shadow-md);
    transition: var(--transition);
    height: 100%;
}
.result-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.result-card .result-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 0.55rem;
    background: linear-gradient(90deg, #ffffff, var(--blue-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.result-card .result-label {
    font-size: 0.72rem;
    color: var(--blue-light);
    text-transform: uppercase;
    letter-spacing: 1.3px;
    font-weight: 700;
}

@media (max-width: 768px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .page-header h1 { font-size: 1.75rem !important; }
    .metric-card .value { font-size: 1.8rem; }
    .card { padding: 1.25rem !important; }
}
</style>
"""


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ICON SET — SVG murni, tanpa emoji/emoticon
# ─────────────────────────────────────────────
ICONS = {
    "logo": """<svg viewBox="0 0 24 24" fill="none" stroke="#D6E9F4" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 3c-1.7 0-3 2.5-3 6v6c0 3 1.3 6 3.3 6 1.4 0 1.7-1.3 1.7-3V6c0-1.7-.6-3-2-3Z"/>
        <path d="M15 3c1.7 0 3 2.5 3 6v6c0 3-1.3 6-3.3 6-1.4 0-1.7-1.3-1.7-3V6c0-1.7.6-3 2-3Z"/>
        <path d="M12 3v6"/>
    </svg>""",
    "book": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5A2.5 2.5 0 0 0 4 22.5"/>
        <path d="M4 4.5v16A2.5 2.5 0 0 1 6.5 18H20"/>
    </svg>""",
    "flask": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 2v6.5L4 18a2 2 0 0 0 1.8 3h12.4a2 2 0 0 0 1.8-3l-5-9.5V2"/>
        <path d="M8 2h8"/>
        <path d="M7 15h10"/>
    </svg>""",
    "trophy": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M8 4h8v5a4 4 0 0 1-8 0V4Z"/>
        <path d="M8 5H5a3 3 0 0 0 3 5"/>
        <path d="M16 5h3a3 3 0 0 1-3 5"/>
        <path d="M12 13v3"/>
        <path d="M9 20h6"/>
        <path d="M10 16.5h4l.5 3.5h-5l.5-3.5Z"/>
    </svg>""",
    "wrench": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14.7 6.3a4 4 0 0 0-5.4 4.6L3 17.2V21h3.8l6.3-6.3a4 4 0 0 0 4.6-5.4l-2.6 2.6-2-2 2.6-2.6Z"/>
    </svg>""",
    "layers": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="m12 2 9 5-9 5-9-5 9-5Z"/>
        <path d="m3 12 9 5 9-5"/>
        <path d="m3 17 9 5 9-5"/>
    </svg>""",
    "database": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <ellipse cx="12" cy="5" rx="8" ry="3"/>
        <path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/>
        <path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>
    </svg>""",
    "scale": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3v18"/>
        <path d="M6 7h12"/>
        <path d="M3 15l3-8 3 8a3 3 0 0 1-6 0Z"/>
        <path d="M15 15l3-8 3 8a3 3 0 0 1-6 0Z"/>
    </svg>""",
    "sliders": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 6h16"/><circle cx="9" cy="6" r="2"/>
        <path d="M4 12h16"/><circle cx="16" cy="12" r="2"/>
        <path d="M4 18h16"/><circle cx="10" cy="18" r="2"/>
    </svg>""",
    "info": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <path d="M12 11v6"/>
        <path d="M12 7.5h.01"/>
    </svg>""",
    "camera": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 8h3l1.5-2h7L17 8h3v11H4V8Z"/>
        <circle cx="12" cy="13.5" r="3.2"/>
    </svg>""",
    "target": """<svg viewBox="0 0 24 24" fill="none" stroke="#1B4F72" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <circle cx="12" cy="12" r="5"/>
        <circle cx="12" cy="12" r="1"/>
    </svg>""",
    "download": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3v12"/>
        <path d="m7 11 5 5 5-5"/>
        <path d="M4 20h16"/>
    </svg>""",
    "warning": """<svg viewBox="0 0 24 24" fill="none" stroke="#B45309" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3 2 20h20L12 3Z"/>
        <path d="M12 10v4"/>
        <path d="M12 17h.01"/>
    </svg>""",
}


def icon(name, size=16):
    """Kembalikan markup SVG untuk sebuah icon."""
    svg = ICONS.get(name, "")
    return svg


def section_title(title, icon_name=None):
    icon_html = f'<div class="icon-chip">{icon(icon_name)}</div>' if icon_name else ""
    st.markdown(
        f'<div class="section-title">{icon_html}<h3>{title}</h3></div>',
        unsafe_allow_html=True,
    )


def page_header(badge, title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
        <div class="badge">{badge}</div>
        <h1>{title}</h1>
        {'<p class="subtitle">' + subtitle + '</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def card(title, body):
    st.markdown(f"""
    <div class="card"><h3>{title}</h3><p>{body}</p></div>
    """, unsafe_allow_html=True)


def info_box(text, icon_name="info"):
    st.markdown(
        f'<div class="info-box"><div class="icon-chip">{icon(icon_name)}</div><p>{text}</p></div>',
        unsafe_allow_html=True,
    )


def divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


def metric_card(value, label, delta=""):
    delta_html = f'<div class="delta">{delta}</div>' if delta else ''
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{value}</div>
        <div class="label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def result_card(value, label):
    st.markdown(f"""
    <div class="result-card">
        <div class="result-value">{value}</div>
        <div class="result-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR — logo, judul, navigasi antar halaman, footer
# Dipanggil di setiap halaman agar konsisten.
# ─────────────────────────────────────────────
def sidebar_nav(extra_controls=None):
    """
    extra_controls: fungsi opsional (callable) yang dipanggil di dalam sidebar
    untuk merender kontrol tambahan khusus suatu halaman (mis. slider threshold).
    """
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-logo-wrap">
                <div class="sidebar-logo-mark">{icon('logo')}</div>
                <div class="sidebar-logo-title">PulmoVision</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if extra_controls is not None:
            extra_controls()

        st.markdown("""
        <div class="sidebar-footer">
            <p>PulmoVision<br>YOLOv8 + Triplet Attention<br>Deteksi &amp; Klasifikasi Tumor Paru</p>
        </div>
        """, unsafe_allow_html=True)