"""
Second Serving — Reducing Food Waste Through Smart Food Donation
Investor-ready dark-theme Streamlit prototype.
Palette: charcoal-navy base, amber primary accent, teal secondary accent.
Icons: inline SVG (no emoji) for consistent rendering across all devices.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

import database as db

st.set_page_config(
    page_title="Second Serving | Food Rescue Platform",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()
db.seed_demo_data()

# ------------------------------------------------------------------
# Design tokens — charcoal-navy base, amber primary, teal secondary
# ------------------------------------------------------------------
BG          = "#0B0D12"
BG_ELEV     = "#12151C"
CARD        = "#171B24"
CARD_HOVER  = "#1E232E"
BORDER      = "#2A303B"
TEXT        = "#EDEFF3"
TEXT_MUTED  = "#9096A3"
ACCENT      = "#FF8A3D"     # amber — primary
ACCENT_DARK = "#E06B1F"
TEAL        = "#2DD4BF"     # secondary data color
BLUE        = "#5B9BD8"
GOLD        = "#E8C468"
DANGER      = "#E5674E"
INPUT_BG    = "#0F1218"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
[data-testid="stMain"], .main, .block-container {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}}
[data-testid="stHeader"] {{ background-color: {BG} !important; }}
h1, h2, h3, h4, h5, p, span, label, div {{ color: {TEXT}; }}
h1, h2, h3, h4, .ss-brand {{ font-family: 'Poppins', 'Inter', sans-serif !important; }}
.block-container {{ padding-top: 2rem !important; }}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #08090D 0%, {BG_ELEV} 100%) !important;
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
section[data-testid="stSidebar"] .stRadio label {{ font-size: 15px; padding: 4px 0; }}
section[data-testid="stSidebar"] [data-testid="stMetric"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px;
    padding: 10px 12px !important;
}}
section[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
    color: {ACCENT} !important; font-weight: 800 !important; font-size: 22px !important;
}}
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED} !important; font-size: 12px !important;
}}
section[data-testid="stSidebar"] hr {{ border-color: {BORDER} !important; }}

/* ---------- Hero ---------- */
.ss-hero {{
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at 15% 20%, rgba(255,138,61,0.14) 0%, transparent 45%),
                radial-gradient(circle at 85% 80%, rgba(45,212,191,0.10) 0%, transparent 45%),
                linear-gradient(135deg, #10131A 0%, #171B24 100%);
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 48px 48px;
    margin-bottom: 26px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
}}
.ss-hero h1 {{ font-size: 42px; font-weight: 800; margin: 0 0 10px 0; color: {TEXT} !important; letter-spacing: -0.5px; }}
.ss-hero p {{ font-size: 17px; color: {TEXT_MUTED} !important; max-width: 660px; margin: 0; line-height: 1.6; }}
.ss-hero .ss-tag {{
    display:inline-block; background: rgba(255,138,61,0.12);
    border: 1px solid rgba(255,138,61,0.4);
    color: {ACCENT} !important; padding: 6px 15px; border-radius: 30px;
    font-size: 12.5px; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; margin-bottom: 18px;
}}

/* ---------- KPI cards ---------- */
.kpi {{
    background: {CARD} !important;
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px 22px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}}
.kpi:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(255,138,61,0.18);
    border-color: {ACCENT};
}}
.kpi .kpi-icon {{ margin-bottom: 10px; opacity: 0.95; }}
.kpi .kpi-icon svg {{ display: block; }}
.kpi .kpi-val {{
    font-family: 'Poppins', sans-serif;
    font-size: 32px; font-weight: 800; color: {ACCENT} !important; line-height: 1.1;
}}
.kpi .kpi-label {{
    font-size: 12.5px; color: {TEXT_MUTED} !important; font-weight: 600; margin-top: 7px;
    text-transform: uppercase; letter-spacing: 0.04em;
}}
.kpi .kpi-delta {{ font-size: 12.5px; color: {TEAL} !important; font-weight: 600; margin-top: 4px; }}

/* ---------- Generic content card ---------- */
.ss-card {{
    background: {CARD} !important;
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.32);
    margin-bottom: 14px;
}}
.ss-card, .ss-card * {{ color: {TEXT} !important; }}
.ss-card.claimed {{ opacity: 0.6; border-left: 4px solid {TEXT_MUTED}; }}
.ss-card.available {{ border-left: 4px solid {ACCENT}; }}
.ss-card h4 {{ margin: 0 0 4px 0; font-size: 16.5px; }}
.ss-card small {{ color: {TEXT_MUTED} !important; font-size: 13px; }}

.ss-badge {{
    display:inline-block; padding: 3px 11px; border-radius: 20px;
    font-size: 11.5px; font-weight: 700; margin-right:6px; letter-spacing: 0.02em;
}}
.badge-available {{ background:rgba(255,138,61,0.15) !important; color:{ACCENT} !important; }}
.badge-claimed   {{ background:rgba(232,196,104,0.15) !important; color:{GOLD} !important; }}
.badge-delivery  {{ background:rgba(45,212,191,0.15) !important; color:{TEAL} !important; }}
.badge-danger    {{ background:rgba(229,103,78,0.15) !important; color:{DANGER} !important; }}

/* ---------- Section headers ---------- */
.ss-section-title {{ font-size: 23px; font-weight: 800; color: {TEXT} !important; margin: 8px 0 4px 0; }}
.ss-section-title .accent {{ color: {ACCENT} !important; }}
.ss-section-sub {{ color: {TEXT_MUTED} !important; font-size: 14px; margin-bottom: 20px; }}

/* ---------- How it works steps ---------- */
.ss-step {{
    background: {CARD} !important;
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 24px 20px;
    height: 100%;
    transition: transform 0.18s ease, border-color 0.18s ease;
}}
.ss-step:hover {{ transform: translateY(-3px); border-color: {TEAL}; }}
.ss-step .step-num {{
    display:inline-flex; align-items:center; justify-content:center;
    width: 34px; height: 34px; border-radius: 50%;
    background: rgba(255,138,61,0.15); color: {ACCENT} !important;
    font-weight: 800; font-size: 15px; margin-bottom: 12px;
}}
.ss-step h4 {{ font-size: 16px; margin: 4px 0 6px 0; color: {TEXT} !important; display: flex; align-items: center; gap: 6px; }}
.ss-step h4 svg {{ flex-shrink: 0; }}
.ss-step p {{ font-size: 13.5px; color: {TEXT_MUTED} !important; line-height: 1.5; margin:0; }}

/* ---------- Buttons ---------- */
.stButton>button {{
    background: {ACCENT} !important; color: #100A05 !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important; padding: 9px 20px !important;
    transition: all 0.15s ease !important;
}}
.stButton>button:hover {{
    background: {ACCENT_DARK} !important; color: #100A05 !important;
    box-shadow: 0 4px 14px rgba(255,138,61,0.3) !important;
}}
.stButton>button p {{ color: #100A05 !important; }}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {{ font-weight: 600; color: {TEXT_MUTED} !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {ACCENT} !important; }}
[data-baseweb="tab-highlight"] {{ background-color: {ACCENT} !important; }}

/* ---------- Metrics (non-sidebar) ---------- */
[data-testid="stMetric"] {{
    background: {CARD} !important; border: 1px solid {BORDER}; border-radius: 12px;
    padding: 10px 14px;
}}
[data-testid="stMetricValue"] {{ color: {ACCENT} !important; }}
[data-testid="stMetricLabel"] {{ color: {TEXT_MUTED} !important; }}

/* ---------- Form inputs ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input,
.stDateInput input, .stTimeInput input {{
    background-color: {INPUT_BG} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 9px !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {{
    border-color: {ACCENT} !important; box-shadow: 0 0 0 1px {ACCENT} !important;
}}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {{
    color: {TEXT_MUTED} !important; opacity: 1 !important;
}}
.stSelectbox div[data-baseweb="select"] > div {{
    background-color: {INPUT_BG} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 9px !important;
}}
.stSelectbox svg {{ fill: {TEXT} !important; }}
div[data-baseweb="popover"] ul, div[data-baseweb="menu"] {{ background-color: {CARD} !important; }}
div[data-baseweb="popover"] li, div[data-baseweb="menu"] li {{
    color: {TEXT} !important; background-color: {CARD} !important;
}}
div[data-baseweb="popover"] li:hover {{ background-color: {CARD_HOVER} !important; }}
.stCheckbox label p {{ color: {TEXT} !important; }}

/* Expander */
[data-testid="stExpander"] {{
    background-color: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
[data-testid="stExpander"] p, [data-testid="stExpander"] span, [data-testid="stExpander"] label {{
    color: {TEXT} !important;
}}

/* Form container */
[data-testid="stForm"] {{
    background-color: {BG_ELEV} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 14px !important;
    padding: 18px !important;
}}

/* Dataframe */
[data-testid="stDataFrame"] {{ background-color: {CARD} !important; border-radius: 10px; }}

label p, .stMarkdown p {{ color: {TEXT} !important; }}
hr {{ border-color: {BORDER} !important; }}

.ss-quote {{
    background: rgba(255,138,61,0.06) !important; border-left: 4px solid {ACCENT};
    padding: 16px 20px; border-radius: 12px; color: {TEXT} !important;
    font-size: 14.5px; line-height: 1.65; margin: 10px 0; font-style: italic;
}}
.ss-quote * {{ color: {TEXT} !important; }}

.ss-divider {{
    height: 1px; background: linear-gradient(90deg, transparent, {BORDER}, transparent);
    margin: 30px 0;
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SVG icon library (no emoji — renders identically on every device)
# ------------------------------------------------------------------
ICONS = {
    "box": '<path d="M21 8L12 3 3 8l9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "meal": '<path d="M7 3v7a2 2 0 002 2h0a2 2 0 002-2V3"/><path d="M9 12v9"/><path d="M17 3c-1.5 0-3 1.5-3 4s1.5 4 3 4v9"/>',
    "store": '<path d="M3 9l1-5h16l1 5"/><path d="M4 9v10a1 1 0 001 1h14a1 1 0 001-1V9"/><path d="M9 20v-6h6v6"/>',
    "bell": '<path d="M18 8a6 6 0 00-12 0c0 5-2 6-2 6h16s-2-1-2-6"/><path d="M10 20a2 2 0 004 0"/>',
    "truck": '<rect x="1" y="6" width="14" height="11" rx="1"/><path d="M15 10h4l3 3v4h-7"/><circle cx="6" cy="19" r="2"/><circle cx="17" cy="19" r="2"/>',
    "receipt": '<path d="M6 2h12v20l-3-2-3 2-3-2-3 2V2z"/><path d="M9 7h6M9 11h6M9 15h4"/>',
    "money": '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.5c0-1.2 1.1-2 2.5-2s2.5.8 2.5 2-1.1 1.6-2.5 2-2.5.8-2.5 2 1.1 2 2.5 2 2.5-.8 2.5-2"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M15 20c0-2.5 1-4.5 2.5-5.5"/>',
    "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
    "home": '<path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/>',
}


def icon_svg(name, size=22, color="currentColor"):
    path = ICONS.get(name, "")
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"
    stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'''


def kpi_card(value, label, icon=None, delta=None, icon_color=None):
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    icon_html = f'<div class="kpi-icon">{icon_svg(icon, 24, icon_color or ACCENT)}</div>' if icon else ""
    return f"""
    <div class="kpi">
        {icon_html}
        <div class="kpi-val">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """


def step_card(num, icon, title, text):
    return f"""
    <div class="ss-step">
        <div class="step-num">{num}</div>
        <h4>{icon_svg(icon, 18, ACCENT)} {title}</h4>
        <p>{text}</p>
    </div>
    """


PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=TEXT, size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title_font=dict(family="Poppins, sans-serif", size=16, color=TEXT),
    legend=dict(font=dict(color=TEXT)),
    colorway=[ACCENT, TEAL, GOLD, BLUE, TEXT_MUTED],
    xaxis=dict(gridcolor=BORDER, color=TEXT, linecolor=BORDER, tickfont=dict(color=TEXT, size=12)),
    yaxis=dict(gridcolor=BORDER, color=TEXT, linecolor=BORDER, tickfont=dict(color=TEXT, size=12)),
    margin=dict(l=40, r=20, t=50, b=70),
)

# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
st.sidebar.markdown(
    f"<div class='ss-brand' style='font-size:22px;font-weight:800;color:{ACCENT};'>🥖 Second Serving</div>",
    unsafe_allow_html=True,
)
st.sidebar.caption("Food Rescue & Redistribution Platform")
page = st.sidebar.radio(
    "Navigate",
    ["Overview & Impact", "Donor Portal", "Recipient Portal",
     "Logistics Board", "Trust & Safety", "Investor Summary"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
stats = db.get_stats()
c1, c2 = st.sidebar.columns(2)
c1.metric("Meals rescued", stats["total_meals"])
c2.metric("Donors", stats["active_donors"])
c3, c4 = st.sidebar.columns(2)
c3.metric("Recipients", stats["active_recipients"])
c4.metric("Live posts", stats["total_donations"] - stats["total_claimed"])
st.sidebar.markdown("---")
st.sidebar.caption("Built for SBS 210 · Second Serving Team\nKing's College / Westcliff University")

# ------------------------------------------------------------------
# OVERVIEW & IMPACT
# ------------------------------------------------------------------
if page == "Overview & Impact":
    st.markdown("""
    <div class="ss-hero">
        <div class="ss-tag">Food Rescue Platform · Live Prototype</div>
        <h1>Second Serving</h1>
        <p>We connect restaurants and cafeterias with surplus, unsold food to nearby
        shelters and food banks — in under 30 seconds. No more good food in landfills
        while people go hungry three kilometers away.</p>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card(stats["total_donations"], "Donations Posted", "box"), unsafe_allow_html=True)
    k2.markdown(kpi_card(stats["total_claimed"], "Donations Claimed", "check"), unsafe_allow_html=True)
    k3.markdown(kpi_card(stats["total_meals"], "Est. Meals Rescued", "meal"), unsafe_allow_html=True)
    k4.markdown(kpi_card(stats["active_donors"], "Partner Businesses", "store"), unsafe_allow_html=True)

    st.markdown('<div class="ss-divider"></div>', unsafe_allow_html=True)

    # ---------- How it works ----------
    st.markdown('<div class="ss-section-title">How <span class="accent">Second Serving</span> Works</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-section-sub">Four steps, from surplus food to a delivered meal.</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(step_card(1, "store", "Post", "A restaurant logs surplus food — type, quantity, allergens, pickup window — in under 30 seconds."), unsafe_allow_html=True)
    with s2:
        st.markdown(step_card(2, "bell", "Match", "Nearby shelters and food banks see it appear live and claim what they need."), unsafe_allow_html=True)
    with s3:
        st.markdown(step_card(3, "truck", "Deliver", "If the donor can't drop it off, a volunteer picks it up from the Logistics Board."), unsafe_allow_html=True)
    with s4:
        st.markdown(step_card(4, "receipt", "Verify", "A receipt and safety record are generated automatically, building trust on both sides."), unsafe_allow_html=True)

    st.markdown('<div class="ss-divider"></div>', unsafe_allow_html=True)

    donations = db.get_all_donations()
    if donations:
        df = pd.DataFrame([dict(r) for r in donations])
        colA, colB = st.columns(2)

        with colA:
            st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig = px.pie(status_counts, names="Status", values="Count", hole=0.55, title="Donation Status")
            fig.update_layout(**PLOTLY_LAYOUT)
            fig.update_traces(textfont=dict(color=TEXT, size=13), marker=dict(line=dict(color=CARD, width=2)))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            donor_counts = df["donor_name"].value_counts().reset_index()
            donor_counts.columns = ["Donor", "Donations"]
            fig2 = px.bar(donor_counts, x="Donor", y="Donations", title="Donations by Business")
            fig2.update_layout(**PLOTLY_LAYOUT)
            fig2.update_traces(marker_color=ACCENT, marker_line_width=0)
            fig2.update_xaxes(tickangle=-20)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No donations yet — post the first one from the Donor Portal.")

    st.markdown('<div class="ss-section-title">Why This Matters</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ss-quote">
    "Sita runs a shift at a buffet and has to throw away leftover food at closing —
    purely due to health regulation and no reliable channel to give it away safely.
    Three kilometers away, Ram runs a shelter with an almost-empty food bank.
    They're solving the same problem from opposite ends, and have never met."
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# DONOR PORTAL
# ------------------------------------------------------------------
elif page == "Donor Portal":
    st.markdown('<div class="ss-section-title">🏪 Donor Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-section-sub">Publish excess food in under 30 seconds.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Post Surplus Food", "My Donations"])
    donors = db.get_donors()
    donor_names = {d["name"]: d["id"] for d in donors}

    with tab1:
        with st.expander("➕ Register a new business (first-time donors)"):
            with st.form("new_donor_form"):
                nd_name = st.text_input("Business name")
                nd_type = st.selectbox("Business type", ["Bakery", "Restaurant", "Cafe", "Cafeteria", "Other"])
                nd_loc = st.text_input("Location")
                if st.form_submit_button("Register business"):
                    if nd_name:
                        db.add_donor(nd_name, nd_type, nd_loc)
                        st.success(f"{nd_name} registered! Select it below.")
                        st.rerun()

        st.markdown("#### Post a new surplus food item")
        with st.form("post_food_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                donor_choice = st.selectbox("Your business", list(donor_names.keys()) if donor_names else ["No donors registered"])
                food_type = st.text_input("Food type", placeholder="e.g. Assorted bagels & pastries")
                quantity = st.text_input("Quantity", placeholder="e.g. 25 pieces / 10 kg")
                allergens = st.text_input("Allergens (comma separated)", placeholder="Gluten, Dairy, Nuts")
            with col2:
                pickup_start = st.time_input("Pickup window start", value=datetime.now().time())
                pickup_end = st.time_input("Pickup window end", value=(datetime.now() + timedelta(hours=2)).time())
                needs_delivery = st.checkbox("We need delivery help (can't drop it off)")
                safety_checked = st.checkbox("Food meets safety checklist (stored properly, within safe time window)", value=True)
                photo_note = st.text_area("Notes / photo description", placeholder="e.g. Boxed, still warm, individually wrapped")

            submitted = st.form_submit_button("🚀 Publish Donation", use_container_width=True)
            if submitted:
                if not donor_names:
                    st.error("Please register your business first.")
                elif not food_type or not quantity:
                    st.error("Food type and quantity are required.")
                else:
                    today = datetime.now().strftime("%Y-%m-%d")
                    db.create_donation(
                        donor_id=donor_names[donor_choice],
                        food_type=food_type,
                        quantity=quantity,
                        allergens=allergens,
                        pickup_start=f"{today} {pickup_start.strftime('%H:%M')}",
                        pickup_end=f"{today} {pickup_end.strftime('%H:%M')}",
                        needs_delivery=needs_delivery,
                        photo_note=photo_note,
                        safety_checked=safety_checked,
                    )
                    st.success("✅ Donation published! Nearby recipients have been notified.")
                    st.balloons()

    with tab2:
        st.markdown("#### All donations across the network")
        all_donations = db.get_all_donations()
        if all_donations:
            for d in all_donations:
                badge = {
                    "Available": '<span class="ss-badge badge-available">Available</span>',
                    "Claimed": '<span class="ss-badge badge-claimed">Claimed</span>',
                    "Picked Up": '<span class="ss-badge badge-claimed">Picked Up</span>',
                }.get(d["status"], "")
                delivery_badge = '<span class="ss-badge badge-delivery">Needs Delivery</span>' if d["needs_delivery"] else ""
                card_class = "available" if d["status"] == "Available" else "claimed"
                st.markdown(f"""
                <div class="ss-card {card_class}">
                    <h4>{d['food_type']} — {d['quantity']}</h4>
                    {badge}{delivery_badge}<br><br>
                    <small>🏪 {d['donor_name']} &nbsp;|&nbsp; Pickup: {d['pickup_start']} → {d['pickup_end']}</small><br>
                    <small>Allergens: {d['allergens'] or 'None listed'}</small>
                    {f"<br><small>Claimed by: {d['recipient_name']}</small>" if d['recipient_name'] else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No donations posted yet.")

# ------------------------------------------------------------------
# RECIPIENT PORTAL
# ------------------------------------------------------------------
elif page == "Recipient Portal":
    st.markdown('<div class="ss-section-title">🤝 Recipient Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-section-sub">Browse available surplus food and claim what your organization needs.</div>', unsafe_allow_html=True)

    recipients = db.get_recipients()
    recipient_names = {r["name"]: r["id"] for r in recipients}

    with st.expander("➕ Register a new shelter / food bank"):
        with st.form("new_recipient_form"):
            rn_name = st.text_input("Organization name")
            rn_type = st.selectbox("Type", ["Shelter", "Food Bank", "Orphanage", "Community Kitchen", "Other"])
            rn_loc = st.text_input("Location")
            rn_capacity = st.number_input("Meals served per day (capacity)", min_value=0, step=10)
            if st.form_submit_button("Register organization"):
                if rn_name:
                    db.add_recipient(rn_name, rn_type, rn_loc, rn_capacity)
                    st.success(f"{rn_name} registered!")
                    st.rerun()

    st.markdown("#### Acting as")
    active_recipient = st.selectbox("Select your organization", list(recipient_names.keys()) if recipient_names else ["No recipients registered"], label_visibility="collapsed")

    st.markdown('<div class="ss-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-section-title" style="font-size:19px;">📦 Available Donations Near You</div>', unsafe_allow_html=True)

    available = db.get_available_donations()
    if not available:
        st.info("No surplus food available right now — check back soon!")
    else:
        for d in available:
            col1, col2 = st.columns([4, 1])
            with col1:
                delivery_badge = '<span class="ss-badge badge-delivery">Needs Delivery Volunteer</span>' if d["needs_delivery"] else ""
                safety_badge = '<span class="ss-badge badge-available">✅ Safety Checked</span>' if d["safety_checked"] else ""
                st.markdown(f"""
                <div class="ss-card available">
                    <h4>{d['food_type']} — {d['quantity']}</h4>
                    {delivery_badge} {safety_badge}<br><br>
                    <small>🏪 <b>{d['donor_name']}</b> (⭐ {d['donor_rating']}) — {d['donor_location']}</small><br>
                    <small>🕒 Pickup window: {d['pickup_start']} → {d['pickup_end']}</small><br>
                    <small>⚠️ Allergens: {d['allergens'] or 'None listed'}</small><br>
                    <small>📝 {d['photo_note'] or ''}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if recipient_names and st.button("Claim", key=f"claim_{d['id']}", use_container_width=True):
                    db.claim_donation(d["id"], recipient_names[active_recipient])
                    st.success(f"Claimed {d['food_type']}! A receipt has been generated.")
                    st.rerun()

# ------------------------------------------------------------------
# LOGISTICS BOARD
# ------------------------------------------------------------------
elif page == "Logistics Board":
    st.markdown('<div class="ss-section-title">🚚 Logistics Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-section-sub">Donations that need volunteer driver / rideshare support to reach recipients.</div>', unsafe_allow_html=True)

    all_donations = db.get_all_donations()
    need_delivery = [d for d in all_donations if d["needs_delivery"] and d["status"] != "Picked Up"]

    if not need_delivery:
        st.info("No active delivery requests right now.")
    else:
        for d in need_delivery:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="ss-card available">
                    <h4>{d['food_type']} — {d['quantity']}</h4>
                    <small>From: {d['donor_name']} &nbsp;→&nbsp; To: {d['recipient_name'] or 'Unclaimed'}</small><br>
                    <small>🕒 Pickup by: {d['pickup_end']}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if d["status"] == "Claimed":
                    if st.button("Mark Delivered", key=f"deliver_{d['id']}", use_container_width=True):
                        db.mark_picked_up(d["id"])
                        st.success("Marked as delivered!")
                        st.rerun()

    st.markdown('<div class="ss-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### Volunteer Sign-up")
    with st.form("volunteer_form"):
        v_name = st.text_input("Your name")
        v_phone = st.text_input("Phone number")
        v_vehicle = st.selectbox("Vehicle type", ["Motorbike", "Car", "Van", "On foot"])
        if st.form_submit_button("Sign up as delivery volunteer"):
            st.success(f"Thanks {v_name}! You'll be notified of nearby delivery requests.")

# ------------------------------------------------------------------
# TRUST & SAFETY / RECEIPTS
# ------------------------------------------------------------------
elif page == "Trust & Safety":
    st.markdown('<div class="ss-section-title">🧾 Trust & Safety Layer</div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-section-sub">Automatic tax-deduction receipts and safety tracking for every completed donation.</div>', unsafe_allow_html=True)

    receipts = db.get_receipts()
    if receipts:
        df = pd.DataFrame([dict(r) for r in receipts])
        k1, k2 = st.columns(2)
        k1.markdown(kpi_card(len(df), "Receipts Issued", "receipt"), unsafe_allow_html=True)
        k2.markdown(kpi_card(int(df["estimated_meals"].sum()), "Meals Documented", "meal"), unsafe_allow_html=True)
        st.markdown('<div class="ss-divider"></div>', unsafe_allow_html=True)

        st.dataframe(
            df[["issued_at", "donor_name", "recipient_name", "food_type", "quantity", "estimated_meals"]]
            .rename(columns={
                "issued_at": "Issued At", "donor_name": "Donor", "recipient_name": "Recipient",
                "food_type": "Food Type", "quantity": "Quantity", "estimated_meals": "Est. Meals"
            }),
            use_container_width=True, hide_index=True,
        )

        st.download_button(
            "⬇️ Download receipts as CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="second_serving_receipts.csv",
            mime="text/csv",
        )
    else:
        st.info("No receipts generated yet — receipts are auto-created when a recipient claims a donation.")

    st.markdown('<div class="ss-section-title" style="font-size:19px;">Donor Trust Ratings</div>', unsafe_allow_html=True)
    donors = db.get_donors()
    if donors:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        ddf = pd.DataFrame([dict(d) for d in donors])
        fig = px.bar(ddf, x="name", y="rating", range_y=[0, 5], title="")
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_traces(marker_color=TEAL, marker_line_width=0)
        fig.update_xaxes(tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# INVESTOR SUMMARY
# ------------------------------------------------------------------
elif page == "Investor Summary":
    st.markdown("""
    <div class="ss-hero">
        <div class="ss-tag">For Investors & Partners</div>
        <h1>The Opportunity</h1>
        <p>Food waste isn't a supply problem — it's a coordination problem. Second Serving
        is the missing link between edible surplus food and the people who need it,
        built as a lean, low-cost, high-trust platform.</p>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    k1.markdown(kpi_card("$381B", "Food wasted annually in the US (ReFED)", "money"), unsafe_allow_html=True)
    k2.markdown(kpi_card("33.8M", "People in food-insecure households (USDA)", "users"), unsafe_allow_html=True)
    k3.markdown(kpi_card("22–33B lbs", "Restaurant food waste per year (Move For Hunger)", "trash"), unsafe_allow_html=True)

    st.markdown('<div class="ss-divider"></div>', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 💵 The Ask")
        st.write("**NPR 40,00,000** in seed funding for a 6-month pilot covering "
                  "platform development, donor/recipient onboarding, and logistics coordination.")
        st.markdown('</div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### ⏱️ Why Now")
        st.write("Comparable platforms (Too Good To Go, Food Cowboy, Transfernation) prove "
                  "the model works — Transfernation alone redirects **~1.8–2.26 metric tons "
                  "of food per week** in NYC. Second Serving adapts this proven model to "
                  "underserved local markets, starting with Kathmandu.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ss-section-title" style="font-size:19px;">Validated Through Field Interviews</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ss-card">
    We interviewed four food businesses (Bagels & Co, Krishna Bakery, PIE, Wellbeing Bakery)
    before building this platform. Two blockers came up consistently — <b>food-safety liability</b>
    and <b>who handles delivery</b> — which is why Trust & Safety and Logistics are first-class
    features here, not afterthoughts. Businesses also confirmed they only know their exact
    surplus <b>near closing time</b>, which is why the platform is built for fast, last-minute
    posting rather than advance scheduling.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ss-section-title" style="font-size:19px;">Live Platform Metrics</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card(stats["total_donations"], "Donations Posted", "box"), unsafe_allow_html=True)
    k2.markdown(kpi_card(stats["total_claimed"], "Donations Claimed", "check"), unsafe_allow_html=True)
    k3.markdown(kpi_card(stats["active_donors"], "Partner Businesses", "store"), unsafe_allow_html=True)
    k4.markdown(kpi_card(stats["active_recipients"], "Partner Recipients", "home"), unsafe_allow_html=True)