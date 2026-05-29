"""
Private Equity as a Catalyst for Economic Diversification in MENA & the GCC
Interactive dashboard — Streamlit

Run locally:   streamlit run app.py
Deploy:        push this folder to GitHub, then deploy on https://streamlit.io
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# Page config + light theming
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="GCC Private Equity & Diversification",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#0B2138"; TEAL = "#2DD4BF"; GOLD = "#F5B841"; CORAL = "#F4796B"
PLOT_BG = "#14304E"; GRID = "#234566"; INK = "#C7D7E6"

st.markdown(f"""
<style>
    .stApp {{ background: {NAVY}; }}
    h1, h2, h3, h4 {{ color: #FFFFFF; font-family: Georgia, serif; }}
    p, label, .stMarkdown {{ color: {INK}; }}
    [data-testid="stMetricValue"] {{ color: {TEAL}; font-weight: 700; }}
    [data-testid="stMetricLabel"] {{ color: {INK}; }}
    [data-testid="stSidebar"] {{ background: {PLOT_BG}; }}
    .block-container {{ padding-top: 2rem; }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Load data (cached)
# ----------------------------------------------------------------------
@st.cache_data
def load_data():
    firms = pd.read_csv("pe_firms.csv")
    panel = pd.read_csv("pe_country_panel.csv")
    return firms, panel

firms, panel = load_data()

def style_fig(fig, height=380):
    fig.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=INK, family="Arial"),
        margin=dict(l=10, r=10, t=50, b=10), height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        title_font=dict(color="#FFFFFF", size=16),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID)
    return fig

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown("#### INTERNATIONAL BUSINESS RESEARCH  ·  MID-REVIEW")
st.title("Private Equity as a Catalyst for Economic Diversification")
st.markdown(
    f"<p style='color:{INK};font-size:1.05rem;'>MENA &amp; the GCC — a firm-level and panel "
    f"study of how private capital is rewiring the Gulf's non-oil economy. "
    f"<i>Kruthivas Mahesh Tambralli · MS25GF030 · S P Jain School of Global Management</i></p>",
    unsafe_allow_html=True,
)
st.divider()

# ----------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------
st.sidebar.header("Filters")
countries = sorted(firms["country"].unique())
sel_countries = st.sidebar.multiselect("Country", countries, default=countries)

ftypes = sorted(firms["firm_type"].unique())
sel_types = st.sidebar.multiselect("Firm type", ftypes, default=ftypes)

difc_opt = st.sidebar.radio("DIFC / ADGM domicile", ["All", "DIFC/ADGM only", "Non-DIFC only"])

exclude_swf = st.sidebar.checkbox("Exclude sovereign wealth funds (outliers)", value=False)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: 30 PE firms (cross-section) + 6-country panel (2015–2025). "
    "Figures reproduce the report's descriptive statistics and key relationships."
)

# apply filters
f = firms[firms["country"].isin(sel_countries) & firms["firm_type"].isin(sel_types)].copy()
if difc_opt == "DIFC/ADGM only":
    f = f[f["difc_adgm"] == 1]
elif difc_opt == "Non-DIFC only":
    f = f[f["difc_adgm"] == 0]
if exclude_swf:
    f = f[f["firm_type"] != "Sovereign Wealth Fund"]

if f.empty:
    st.warning("No firms match the current filters. Widen your selection in the sidebar.")
    st.stop()

# ----------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Firms in view", f"{len(f)}")
c2.metric("Avg non-oil deal share", f"{f['non_oil_deal_share_pct'].mean():.1f}%")
c3.metric("Total AUM", f"${f['aum_usd_m'].sum()/1000:,.0f}B")
c4.metric("Avg sectoral focus", f"{f['sectoral_focus_score'].mean():.2f} / 10")

st.divider()

# ----------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Market Trends", "🎯 The Decisive Lever (H5)", "🏦 Firm Explorer", "🔬 Correlations"]
)

# ---- TAB 1: country panel trends ----
with tab1:
    st.subheader("GCC private-equity deal value, 2015–2025")
    pv = panel[panel["country"].isin(sel_countries)]
    fig = px.area(
        pv, x="year", y="pe_deal_value_usd_m", color="country",
        labels={"pe_deal_value_usd_m": "PE deal value (USD M)", "year": "Year"},
        color_discrete_sequence=[TEAL, GOLD, "#7FB8D9", "#9D7FD9", "#5EEAD4", "#E89B7F"],
    )
    fig.add_vline(x=2015, line_dash="dot", line_color=GOLD,
                  annotation_text="Post-2015 reforms", annotation_font_color=GOLD)
    st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Non-oil GDP growth vs oil price**")
        fig2 = px.scatter(
            pv, x="oil_price_usd_bbl", y="non_oil_gdp_growth_pct",
            color="country", size="pe_deal_value_usd_m",
            labels={"oil_price_usd_bbl": "Oil price (USD/bbl)",
                    "non_oil_gdp_growth_pct": "Non-oil GDP growth (%)"},
            color_discrete_sequence=[TEAL, GOLD, "#7FB8D9", "#9D7FD9", "#5EEAD4", "#E89B7F"],
        )
        st.plotly_chart(style_fig(fig2), use_container_width=True)
    with colB:
        st.markdown("**Total deal value by country**")
        tot = pv.groupby("country", as_index=False)["pe_deal_value_usd_m"].sum().sort_values("pe_deal_value_usd_m")
        fig3 = px.bar(
            tot, x="pe_deal_value_usd_m", y="country", orientation="h",
            labels={"pe_deal_value_usd_m": "Cumulative deal value (USD M)", "country": ""},
            color_discrete_sequence=[TEAL],
        )
        st.plotly_chart(style_fig(fig3), use_container_width=True)

# ---- TAB 2: H5 sectoral focus ----
with tab2:
    st.subheader("H5 — Sectoral focus is the decisive diversification lever")
    corr_h5 = f["sectoral_focus_score"].corr(f["non_oil_deal_share_pct"])
    st.markdown(
        f"Correlation in current view: **r = {corr_h5:.3f}** "
        f"(report: r = 0.991 across all 30 firms)."
    )
    fig = px.scatter(
        f, x="sectoral_focus_score", y="non_oil_deal_share_pct",
        color="firm_type", size="aum_usd_m", hover_name="firm_name",
        trendline="ols", trendline_color_override=GOLD,
        labels={"sectoral_focus_score": "Sectoral focus score (0–10)",
                "non_oil_deal_share_pct": "Non-oil deal share (%)"},
        color_discrete_sequence=[TEAL, GOLD, CORAL, "#7FB8D9", "#9D7FD9", "#5EEAD4"],
    )
    st.plotly_chart(style_fig(fig, 470), use_container_width=True)
    st.info(
        "Funds that deliberately target non-oil sectors (tech, healthcare, education, "
        "renewables) post far higher non-oil deal shares — diversification quality is an "
        "allocation choice, not an accident of scale."
    )

# ---- TAB 3: firm explorer ----
with tab3:
    st.subheader("Firm explorer")
    colX, colY = st.columns([2, 1])
    with colY:
        x_var = st.selectbox("X axis", ["ln_aum", "aum_usd_m", "policy_reform_score",
                                        "active_non_oil_portfolio_cos", "cumulative_exits"], index=0)
        y_var = st.selectbox("Y axis", ["non_oil_gdp_contribution_usd_m", "non_oil_deal_share_pct",
                                        "cumulative_exits"], index=0)
        log_y = st.checkbox("Log scale (Y)", value=True)
    with colX:
        fig = px.scatter(
            f, x=x_var, y=y_var, color="country", size="aum_usd_m",
            hover_name="firm_name", log_y=log_y,
            color_discrete_sequence=[TEAL, GOLD, CORAL, "#7FB8D9", "#9D7FD9", "#5EEAD4"],
        )
        st.plotly_chart(style_fig(fig, 440), use_container_width=True)

    st.markdown("**Underlying data**")
    st.dataframe(
        f.sort_values("aum_usd_m", ascending=False).reset_index(drop=True),
        use_container_width=True, height=300,
    )
    st.download_button(
        "⬇️ Download filtered data (CSV)",
        f.to_csv(index=False).encode("utf-8"),
        "pe_firms_filtered.csv", "text/csv",
    )

# ---- TAB 4: correlation matrix ----
with tab4:
    st.subheader("Correlation matrix — firm-level variables")
    num_cols = ["ln_aum", "policy_reform_score", "sectoral_focus_score",
                "active_non_oil_portfolio_cos", "cumulative_exits",
                "non_oil_deal_share_pct", "non_oil_gdp_contribution_usd_m"]
    nice = {
        "ln_aum": "ln(AUM)", "policy_reform_score": "Policy",
        "sectoral_focus_score": "Sector focus", "active_non_oil_portfolio_cos": "Portfolio",
        "cumulative_exits": "Exits", "non_oil_deal_share_pct": "Deal share",
        "non_oil_gdp_contribution_usd_m": "Non-oil GDP",
    }
    cm = f[num_cols].copy()
    cm["non_oil_gdp_contribution_usd_m"] = np.log(cm["non_oil_gdp_contribution_usd_m"])
    corr = cm.corr().round(2)
    corr.index = [nice[c] for c in corr.index]
    corr.columns = [nice[c] for c in corr.columns]
    fig = px.imshow(
        corr, text_auto=True, aspect="auto",
        color_continuous_scale=[[0, CORAL], [0.5, PLOT_BG], [1, TEAL]],
        zmin=-1, zmax=1,
    )
    st.plotly_chart(style_fig(fig, 480), use_container_width=True)
    st.caption(
        "Note: non-oil GDP shown in log terms. Strongest links mirror the report — "
        "sector focus ↔ deal share, and ln(AUM) ↔ non-oil GDP contribution."
    )

st.divider()
st.caption(
    "Built with Streamlit · Plotly · pandas. Data derived from the IBR study "
    "datasets (30 PE firms + 6-country panel, 2015–2025)."
)
