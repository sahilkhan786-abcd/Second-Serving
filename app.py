"""
Second Serving — Reducing Food Waste Through Smart Food Donation
Investor-grade Streamlit prototype.

Design system: forced light theme (see .streamlit/config.toml) so contrast
never breaks on dark-mode devices, Inter/Poppins typography, a fixed
deep-green / charcoal / gold palette used consistently across every page.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

import database as db

# ------------------------------------------------------------------
# Page config & one-time DB init
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Second Serving | Food Rescue Platform",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()
db.seed_demo_data()

# ------------------------------------------------------------------
# Design tokens
# ------------------------------------------------------------------
INK = "#1A1D1B"
MUTED = "#5B6660"
GREEN = "#1B5E3A"
GREEN_DARK = "#123D26"
GREEN_LIGHT = "#E7F2EB"
GOLD = "#C7952A"
CARD_BG = "#FFFFFF"
PAGE_BG = "#FAFAF8"
BORDER = "#E4E7E2"
DANGER = "#B3441E"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
    color: {INK};
}}
h1, h2, h3, h4, .ss-brand {{
    font-family: 'Poppins', 'Inter', sans-serif !important;
}}

.stApp {{ background-color: {PAGE_BG}; }}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {GREEN_DARK} 0%, {GREEN} 100%);
}}
section[data-testid="stSidebar"] * {{
    color: #F2F6F3 !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
    font-size: 15px;
    padding: 2px 0;
}}
section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {{
    color: #FFFFFF !important;
    font-weight: 700;
}}
section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] {{
    color: #C9DED0 !important;
}}
section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15); }}

/* ---------- Hero ---------- */
.ss-hero {{
    background: linear-gradient(120deg, {GREEN_DARK} 0%, {GREEN} 55%, #2E7D4F 100%);
    border-radius: 20px;
    padding: 44px 46px;
    color: #FFFFFF;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(18,61,38,0.25);
}}
.ss-hero h1 {{
    font-size: 40px; font-weight: 800; margin: 0 0 8px 0; color: #FFFFFF;
}}
.ss-hero p {{
    font-size: 17px; color: #DCEDE1; max-width: 680px; margin: 0; line-height: 1.55;
}}
.ss-hero .ss-tag {{
    display:inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.35);
    color: #FFFFFF; padding: 5px 14px; border-radius: 30px;
    font-size: 12.5px; font-weight: 600; letter-spacing: 0.04em;
    text-transform: uppercase; margin-bottom: 16px;
}}

/* ---------- KPI cards ---------- */
.kpi {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 2px 12px rgba(20,30,25,0.05);
}}
.kpi .kpi-val {{
    font-family: 'Poppins', sans-serif;
    font-size: 30px; font-weight: 800; color: {GREEN_DARK}; line-height: 1.1;
}}
.kpi .kpi-label {{
    font-size: 13px; color: {MUTED}; font-weight: 600; margin-top: 6px;
    text-transform: uppercase; letter-spacing: 0.03em;
}}
.kpi .kpi-delta {{
    font-size: 12.5px; color: {GREEN}; font-weight: 600; margin-top: 4px;
}}

/* ---------- Generic content card ---------- */
.ss-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 10px rgba(20,30,25,0.05);
    margin-bottom: 14px;
}}
.ss-card.claimed {{ opacity: 0.72; border-left: 4px solid {MUTED}; }}
.ss-card.available {{ border-left: 4px solid {GREEN}; }}
.ss-card h4 {{ margin: 0 0 4px 0; font-size: 16.5px; color: {INK}; }}
.ss-card small {{ color: {MUTED}; font-size: 13px; }}

.ss-badge {{
    display:inline-block; padding: 3px 11px; border-radius: 20px;
    font-size: 11.5px; font-weight: 700; margin-right:6px; letter-spacing: 0.02em;
}}
.badge-available {{ background:{GREEN_LIGHT}; color:{GREEN_DARK}; }}
.badge-claimed {{ background:#FBEFDD; color:{GOLD}; }}
.badge-delivery {{ background:#E7EEF7; color:#2A5A9C; }}
.badge-danger {{ background:#F8E4DC; color:{DANGER}; }}

/* ---------- Section headers ---------- */
.ss-section-title {{
    font-size: 22px; font-weight: 800; color: {GREEN_DARK}; margin: 6px 0 4px 0;
}}
.ss-section-sub {{ color: {MUTED}; font-size: 14px; margin-bottom: 18px; }}

/* ---------- Buttons ---------- */
.stButton>button {{
    background: {GREEN}; color: white; border: none; border-radius: 10px;
    font-weight: 600; padding: 8px 18px; transition: all 0.15s ease;
}}
.stButton>button:hover {{ background: {GREEN_DARK}; color: white; }}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {{ font-weight: 600; color: {MUTED}; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {GREEN_DARK} !important; }}

/* ---------- Metrics on light bg always ---------- */
[data-testid="stMetric"] {{
    background: {CARD_BG}; border: 1px solid {BORDER}; border-radius: 12px;
    padding: 10px 14px;
}}

hr {{ border-color: {BORDER}; }}

.ss-quote {{
    background: {GREEN_LIGHT}; border-left: 4px solid {GREEN};
    padding: 14px 18px; border-radius: 10px; color: {GREEN_DARK};
    font-size: 14.5px; line-height: 1.6; margin: 10px 0;
}}
</style>
""", unsafe_allow_html=True)


def kpi_card(value, label, delta=None):
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi">
        <div class="kpi-val">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """


PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=INK, size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title_font=dict(family="Poppins, sans-serif", size=16, color=GREEN_DARK),
    colorway=[GREEN, GOLD, "#2A5A9C", MUTED, "#8FBFA0"],
)

# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
st.sidebar.markdown(
    "<div class='ss-brand' style='font-size:22px;font-weight:800;color:white;'>🥖 Second Serving</div>",
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
    k1.markdown(kpi_card(stats["total_donations"], "Donations Posted"), unsafe_allow_html=True)
    k2.markdown(kpi_card(stats["total_claimed"], "Donations Claimed"), unsafe_allow_html=True)
    k3.markdown(kpi_card(stats["total_meals"], "Est. Meals Rescued"), unsafe_allow_html=True)
    k4.markdown(kpi_card(stats["active_donors"], "Partner Businesses"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    donations = db.get_all_donations()
    if donations:
        df = pd.DataFrame([dict(r) for r in donations])
        colA, colB = st.columns(2)

        with colA:
            st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig = px.pie(status_counts, names="Status", values="Count", hole=0.55,
                         title="Donation Status")
            fig.update_layout(**PLOTLY_LAYOUT)
            fig.update_traces(textfont=dict(color="white", size=13))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            donor_counts = df["donor_name"].value_counts().reset_index()
            donor_counts.columns = ["Donor", "Donations"]
            fig2 = px.bar(donor_counts, x="Donor", y="Donations", title="Donations by Business")
            fig2.update_layout(**PLOTLY_LAYOUT)
            fig2.update_traces(marker_color=GREEN)
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

    st.markdown("---")
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

    st.markdown("---")
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
        k1.markdown(kpi_card(len(df), "Receipts Issued"), unsafe_allow_html=True)
        k2.markdown(kpi_card(int(df["estimated_meals"].sum()), "Meals Documented"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

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
        fig.update_traces(marker_color=GOLD)
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
    k1.markdown(kpi_card("$381B", "Food wasted annually in the US (ReFED)"), unsafe_allow_html=True)
    k2.markdown(kpi_card("33.8M", "People in food-insecure households (USDA)"), unsafe_allow_html=True)
    k3.markdown(kpi_card("22–33B lbs", "Restaurant food waste per year (Move For Hunger)"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### The Ask")
        st.write("**NPR 40,00,000** in seed funding for a 6-month pilot covering "
                  "platform development, donor/recipient onboarding, and logistics coordination.")
        st.markdown('</div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### Why Now")
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
    k1.markdown(kpi_card(stats["total_donations"], "Donations Posted"), unsafe_allow_html=True)
    k2.markdown(kpi_card(stats["total_claimed"], "Donations Claimed"), unsafe_allow_html=True)
    k3.markdown(kpi_card(stats["active_donors"], "Partner Businesses"), unsafe_allow_html=True)
    k4.markdown(kpi_card(stats["active_recipients"], "Partner Recipients"), unsafe_allow_html=True)
