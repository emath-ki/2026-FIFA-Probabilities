import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="World Cup 2026: Match Odds & Competitive Balance",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS  — dark navy glass-morphism palette
# ══════════════════════════════════════════════════════════════════════════════
C_BG        = "#1a1540"                  # very deep navy — page background
C_NAVY      = "#2f2770"                  # primary navy — cards / sidebar
C_GREEN     = "#318546"                  # emerald green — home win / positive
C_TEAL      = "#6db1b3"                  # soft teal — draw / neutral
C_MINT      = "#c4e0da"                  # pale mint — body text / labels
C_RED       = "#c91a33"                  # crimson — away win / alert
C_WHITE     = "#ffffff"
C_TEXT      = "#e8f4f2"                  # near-white body text
C_SUBTEXT   = "#c4e0da"                  # mint for subtitles
C_GLASS_BG  = "rgba(47,39,112,0.55)"    # glassy navy card fill
C_GLASS_BD  = "rgba(109,177,179,0.25)"  # teal glass border
C_GLASS_SHA = "0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.07)"

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
PLOTLY_TEMPLATE = "plotly_dark"

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: {FONT};
    color: {C_TEXT};
}}
.stApp {{
    background: linear-gradient(135deg, {C_BG} 0%, #0f0d2e 60%, #1a1540 100%);
    min-height: 100vh;
}}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(47,39,112,0.95) 0%, rgba(26,21,64,0.98) 100%) !important;
    border-right: 1px solid {C_GLASS_BD};
    backdrop-filter: blur(20px);
}}
section[data-testid="stSidebar"] * {{
    color: {C_TEXT} !important;
    font-weight: 500;
}}
section[data-testid="stSidebar"] .stSelectbox label {{
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {C_MINT} !important;
}}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
    background: rgba(47,39,112,0.6);
    border: 1.5px solid {C_TEAL} !important;
    border-radius: 8px;
    color: {C_TEXT};
}}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:focus-within {{
    border-color: {C_MINT} !important;
    box-shadow: 0 0 0 2px rgba(196,224,218,0.3);
}}

/* ── Metric containers ────────────────────────────────────────────────────── */
[data-testid="metric-container"] {{
    background: {C_GLASS_BG} !important;
    border: 1px solid {C_GLASS_BD} !important;
    border-radius: 16px !important;
    padding: 20px 22px 16px 22px !important;
    box-shadow: {C_GLASS_SHA} !important;
    backdrop-filter: blur(12px) !important;
    overflow: visible !important;
}}
[data-testid="metric-container"] label {{
    color: {C_MINT} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1.4 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    display: block !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {C_WHITE} !important;
    font-size: 2.0rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    overflow: visible !important;
    word-break: break-word !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-size: 0.82rem !important;
    white-space: normal !important;
    color: {C_TEAL} !important;
    font-style: italic;
}}
[data-testid="metric-container"] > div {{ overflow: visible !important; }}

/* ── Headings ─────────────────────────────────────────────────────────────── */
h1 {{
    color: {C_WHITE} !important;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    letter-spacing: -0.02em;
}}
h2, h3 {{
    color: {C_MINT} !important;
    font-weight: 500 !important;
}}

/* ── Dataframe ────────────────────────────────────────────────────────────── */
.stDataFrame {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {C_GLASS_BD};
    background: {C_GLASS_BG};
}}

/* ── Dividers ─────────────────────────────────────────────────────────────── */
hr {{
    border-color: {C_GLASS_BD} !important;
    opacity: 0.6;
}}

/* ── Block container ─────────────────────────────────────────────────────── */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 4rem;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING & PREP
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data(path: str = "wc_2026_probabilities.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ `wc_2026_probabilities.csv` not found. Place it alongside `app.py` and rerun.")
    st.stop()

COLUMN_MAP = {
    "home_team":  "team1",
    "away_team":  "team2",
    "p_home_win": "home_win",
    "p_draw":     "draw",
    "p_away_win": "away_win",
}
df = df.rename(columns=COLUMN_MAP)

REQUIRED = {"group", "team1", "team2", "home_win", "draw", "away_win"}
missing  = REQUIRED - set(df.columns)
if missing:
    st.error(f"❌ Missing columns: **{missing}**\n\nFound: `{list(df.columns)}`")
    st.stop()

PROB_COLS = ["home_win", "draw", "away_win"]

# ── Pre-compute aggregates ────────────────────────────────────────────────────
df["upset_score"] = 1 - df[["home_win", "draw", "away_win"]].max(axis=1)
group_upset       = df.groupby("group")["upset_score"].mean()
top_upset_group   = str(group_upset.idxmax())
top_upset_val     = float(group_upset.max())

_away_means    = df.groupby("group", sort=False)["away_win"].mean()
top_away_group = str(_away_means.idxmax())
top_away_val   = float(_away_means.max())

top_draw_idx   = int(df["draw"].idxmax())
top_draw_t1    = df.loc[top_draw_idx, "team1"]
top_draw_t2    = df.loc[top_draw_idx, "team2"]
top_draw_match = f"{top_draw_t1} vs {top_draw_t2}"
top_draw_val   = float(df.loc[top_draw_idx, "draw"])

_draw_means  = df.groupby("group", sort=False)["draw"].mean()
tight_group  = str(_draw_means.idxmax())
tight_pct    = f"{_draw_means.max() * 100:.1f}"

# ══════════════════════════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(47,39,112,0.3)",
    font          = dict(family=FONT, color=C_MINT),
    title_font    = dict(color=C_MINT, size=14, family=FONT),
    xaxis         = dict(
        gridcolor     = "rgba(109,177,179,0.2)",
        gridwidth     = 1,
        griddash      = "solid",
        tickfont      = dict(color=C_MINT, size=11),
        title_font    = dict(color=C_MINT),
    ),
    yaxis         = dict(
        gridcolor     = "rgba(109,177,179,0.2)",
        gridwidth     = 1,
        tickfont      = dict(color=C_MINT, size=11),
        title_font    = dict(color=C_MINT),
    ),
    margin        = dict(l=10, r=10, t=30, b=10),
)


def make_gauge(value: float, label: str, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode   = "gauge+number",
        value  = value,
        number = {"suffix": "%", "font": {"size": 34, "color": C_WHITE, "family": FONT}},
        title  = {"text": label, "font": {"size": 13, "color": C_MINT, "family": FONT}},
        gauge  = {
            "axis": {
                "range":     [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(109,177,179,0.4)",
                "tickfont":  {"color": C_MINT, "size": 9},
            },
            "bar":        {"color": color, "thickness": 0.28},
            "bgcolor":    "rgba(47,39,112,0.4)",
            "borderwidth": 1,
            "bordercolor": "rgba(109,177,179,0.3)",
            "steps": [
                {"range": [0,  33], "color": "rgba(49,133,70,0.15)"},
                {"range": [33, 66], "color": "rgba(109,177,179,0.15)"},
                {"range": [66, 100],"color": "rgba(201,26,51,0.15)"},
            ],
            "threshold": {
                "line":      {"color": color, "width": 3},
                "thickness": 0.75,
                "value":     value,
            },
        },
    ))
    fig.update_layout(
        height        = 240,
        margin        = dict(l=16, r=16, t=40, b=8),
        paper_bgcolor = "rgba(0,0,0,0)",
        font          = {"family": FONT},
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown(
        f"<h2 style='color:{C_WHITE};font-size:1.3rem;font-weight:700;"
        f"margin-bottom:2px;'>⚽ World Cup 2026</h2>"
        f"<p style='color:{C_TEAL};font-size:0.85rem;margin-top:0;'>"
        f"Match Odds &amp; Competitive Balance</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── MATCH INSPECTOR ──────────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_WHITE};font-size:0.82rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>"
        f"🔍 Match Inspector</p>",
        unsafe_allow_html=True,
    )

    # ALL matches (no group filtering here)
    match_labels = (df["team1"] + " vs " + df["team2"]).tolist()
    sel_match_label = st.selectbox("Pick a match", options=match_labels, index=0)

    st.divider()

    # ── UPSET POTENTIAL ──────────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_WHITE};font-size:0.82rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>"
        f"🎲 Expected Upset Rate</p>",
        unsafe_allow_html=True,
    )

    upset_ranking = (
        group_upset.sort_values(ascending=False)
        .reset_index()
        .rename(columns={"group": "Group", "upset_score": "Score"})
    )
    upset_ranking["Score"] = upset_ranking["Score"].map("{:.1%}".format)

    st.dataframe(upset_ranking, hide_index=True, use_container_width=True)

    st.divider()

    # ── GROUP PICKER (ONLY HERE) ─────────────────────────────────────────────
    groups    = sorted(df["group"].unique())
    sel_group = st.selectbox("Pick a group", options=groups, index=0)

    st.divider()

    # ── CONTEXT TEXT ─────────────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_MINT};font-size:0.72rem;font-style:italic;"
        f"line-height:1.5;margin-top:4px;'>"
        f"Probabilities are derived from a public Elo-based model. ",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='color:{C_TEAL};font-size:0.68rem;margin-top:6px;'>"
        f"Data: wc_2026_probabilities.csv &nbsp;·&nbsp; {len(df):,} rows</p>",
        unsafe_allow_html=True,
    )

    # ── SIGNATURE ────────────────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_WHITE};font-size:0.7rem;margin-top:10px;"
        f"opacity:0.7;'>By Eshwaree Mathanki</p>",
        unsafe_allow_html=True,
    )

    

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["Main Dashboard", "Data Guide"])

with tab1:


    # ── Header: title/narrative (left) + image (right) ───────────────────────
    import os
    from pathlib import Path

    _header_left, _header_right = st.columns([3, 1], gap="large")

    with _header_left:
        st.markdown(
            f"<h1 style='color:{C_WHITE};font-weight:700;font-size:2.5rem;"
            f"letter-spacing:-0.02em;margin-bottom:4px;'>World Cup 2026</h1>"
            f"<p style='color:{C_TEAL};font-size:1.1rem;font-style:italic;"
            f"font-weight:400;margin-top:0;margin-bottom:28px;'>"
            f"Explore every group's match odds &amp; more in one living view</p>",
            unsafe_allow_html=True,
        )
        # Narrative summary block
        st.markdown(
            f"""
            <div style="
                margin: 0 0 36px 0;
                padding: 20px 24px;
                border-left: 4px solid {C_TEAL};
                background: {C_GLASS_BG};
                border-radius: 0 12px 12px 0;
                box-shadow: {C_GLASS_SHA};
                backdrop-filter: blur(12px);
                line-height: 1.6;
                font-family: {FONT};
                font-size: 1.0rem;
                color: {C_TEXT};
            ">
                The 2026 World Cup group stage features
                <strong style="color:{C_WHITE}">{len(df)} matches</strong>
                across <strong style="color:{C_WHITE}">{df["group"].nunique()} groups</strong>.
                Group&nbsp;<span style="color:{C_TEAL};font-weight:600;">{top_away_group}</span>
                carries the highest away-win probability:
                <span style="color:{C_TEAL};font-weight:600;">{top_away_val*100:.1f}%</span> on average.
                Group&nbsp;<span style="color:{C_GREEN};font-weight:600;">{tight_group}</span>
                is the most tightly contested, with
                <span style="color:{C_GREEN};font-weight:600;">{tight_pct}%</span>
                of its matches likely to end level.
                The match with the slimmest margins?
                <span style="font-weight:600;color:{C_WHITE}">{top_draw_t1} vs {top_draw_t2}</span>;
                where even a draw sits at
                <span style="color:{C_RED};font-weight:600;">{top_draw_val*100:.1f}%</span>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with _header_right:
        # Resolve image relative to this script's directory so any absolute
        # path in the working folder works regardless of where the user is.
        _img_name = "e97b939610c0b9fbd9d1b2bbcebdd2a2.jpg"
        _img_path = Path(__file__).parent / _img_name
        if _img_path.exists():
            st.image(
                str(_img_path),
                use_container_width=True,
            )
        else:
            # Fallback: try the bare filename (works when CWD == app dir)
            if os.path.exists(_img_name):
                st.image(_img_name, use_container_width=True)
            else:
                st.markdown(
                    f"<p style='color:{C_TEAL};font-size:0.75rem;font-style:italic;"
                    f"text-align:center;padding-top:60px;'>"
                    f"Image not found.<br>{_img_name}</p>",
                    unsafe_allow_html=True,
                )

    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 0 — KPI METRIC TILES
    # ══════════════════════════════════════════════════════════════════════════════
    st.divider()
    st.markdown(
        f"<h3 style='color:{C_WHITE};font-size:1.1rem;font-weight:600;margin-bottom:12px;'>"
        f"📈 Tournament Overview</h3>",
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Group Stage Matches",
        f"{len(df)}",
        delta=f"across {df['group'].nunique()} groups",
    )

    with m2:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_RED};">
                <p style="color:{C_MINT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Away-Favoured Group</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">Group {top_away_group}</p>
                <p style="color:{C_RED};font-size:0.88rem;font-style:italic;margin:0;">
                    {top_away_val*100:.1f}% avg away-win probability</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_RED};">
                <p style="color:{C_MINT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Most Unpredictable Group</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">Group {top_upset_group}</p>
                <p style="color:{C_RED};font-size:0.88rem;font-style:italic;margin:0;">
                    {top_upset_val*100:.1f}% avg upset score</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)

    with n1:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_GREEN};">
                <p style="color:{C_MINT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Most Draw-Likely Group</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">Group {tight_group}</p>
                <p style="color:{C_GREEN};font-size:0.88rem;font-style:italic;margin:0;">
                    {tight_pct}% avg draw probability</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with n2:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_TEAL};">
                <p style="color:{C_MINT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Highest Draw Match</p>
                <p style="color:{C_WHITE};font-size:1.15rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.3;">{top_draw_t1}<br>vs {top_draw_t2}</p>
                <p style="color:{C_TEAL};font-size:0.88rem;font-style:italic;margin:0;">
                    {top_draw_val*100:.1f}% draw probability</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with n3:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_TEAL};">
                <p style="color:{C_MINT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Total Groups</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">{df["group"].nunique()}</p>
                <p style="color:{C_TEAL};font-size:0.88rem;font-style:italic;margin:0;">
                    Groups A – {sorted(df["group"].unique())[-1]} · 6 matches each</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 1 — MATCH INSPECTOR  (tiles first, speedometers directly below)
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<h2 style='color:{C_WHITE};font-size:1.5rem;font-weight:600;margin-bottom:4px;'>"
        f"🔍 Match Inspector — {sel_match_label}</h2>",
        unsafe_allow_html=True,
    )

    _t1, _t2  = sel_match_label.split(" vs ", 1)
    match_row = df[(df["team1"] == _t1) & (df["team2"] == _t2)].iloc[0]

    _home_val = float(match_row["home_win"]) * 100
    _draw_val = float(match_row["draw"])     * 100
    _away_val = float(match_row["away_win"]) * 100


    # ── Probability tiles ─────────────────────────────────────────────────────────
    def prob_card(team_label: str, outcome: str, pct: float, color: str) -> str:
        bar_w = f"{pct:.1f}%"
        return f"""
        <div style="
            background: {C_GLASS_BG};
            border: 1px solid {C_GLASS_BD};
            border-radius: 16px;
            padding: 22px 24px;
            box-shadow: {C_GLASS_SHA};
            backdrop-filter: blur(16px);
            border-top: 4px solid {color};
        ">
            <p style="color:{C_MINT};font-size:0.72rem;font-weight:600;text-transform:uppercase;
                      letter-spacing:0.6px;margin:0 0 4px 0;">{team_label}</p>
            <p style="color:{C_WHITE};font-size:2.2rem;font-weight:700;margin:0 0 8px 0;
                      line-height:1;">{pct:.1f}<span style="font-size:1rem;font-weight:400;">%</span></p>
            <p style="color:{C_SUBTEXT};font-size:0.8rem;margin:0 0 10px 0;">{outcome}</p>
            <div style="background:rgba(255,255,255,0.1);border-radius:99px;height:6px;overflow:hidden;">
                <div style="width:{bar_w};height:100%;background:{color};border-radius:99px;"></div>
            </div>
        </div>"""

    # — Speedometer gauges (directly below the tiles) —
    st.markdown(
        f"<p style='color:{C_MINT};font-size:0.82rem;font-weight:600;"
        f"text-transform:uppercase;letter-spacing:0.05em;margin:18px 0 0 0;'>"
        f"</p>",
        unsafe_allow_html=True,
    )
    sp1, sp2, sp3 = st.columns(3)
    with sp1:
        st.plotly_chart(
            make_gauge(_home_val, f"🏠Home Win : {_t1}", C_GREEN),
            use_container_width=True, config={"displayModeBar": False},
        )
    with sp2:
        st.plotly_chart(
            make_gauge(_draw_val, "🤝 Draw", C_TEAL),
            use_container_width=True, config={"displayModeBar": False},
        )
    with sp3:
        st.plotly_chart(
            make_gauge(_away_val, f"✈️Away Win : {_t2} ", C_RED),
            use_container_width=True, config={"displayModeBar": False},
        )



    # — Tiles row —
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown(prob_card(f"🏠 {_t1}", "Home Win", _home_val, C_GREEN), unsafe_allow_html=True)
    with g2:
        st.markdown(prob_card("🤝 Draw", "Neither side wins", _draw_val, C_TEAL), unsafe_allow_html=True)
    with g3:
        st.markdown(prob_card(f"✈️ {_t2}", "Away Win", _away_val, C_RED), unsafe_allow_html=True)

    # Dominant outcome banner
    _outcome_map = {"Home Win": (_home_val, C_GREEN), "Draw": (_draw_val, C_TEAL), "Away Win": (_away_val, C_RED)}
    _dom         = max(_outcome_map, key=lambda k: _outcome_map[k][0])
    _dom_val, _dom_color = _outcome_map[_dom]
    _icons       = {"Home Win": "🏠", "Draw": "🤝", "Away Win": "✈️"}
    st.markdown(
        f"""
        <div style="
            background: {C_GLASS_BG};
            border: 1px solid {C_GLASS_BD};
            border-left: 4px solid {_dom_color};
            border-radius: 12px;
            padding: 14px 24px;
            text-align: left;
            margin: 16px 0 4px 0;
            max-width: 480px;
            backdrop-filter: blur(12px);
            box-shadow: {C_GLASS_SHA};
        ">
            <span style="color:{C_MINT};font-size:0.7rem;text-transform:uppercase;
                         letter-spacing:0.6px;font-weight:600;">Most likely outcome</span><br>
            <span style="color:{_dom_color};font-size:1.3rem;font-weight:700;">
                {_icons[_dom]}&nbsp;{_dom} &mdash; {_dom_val:.1f}%
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )



    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 2 — CHARTS
    # ══════════════════════════════════════════════════════════════════════════════
    chart_col1, chart_col2 = st.columns([3, 2], gap="large")
    with chart_col1:
        st.divider()
        st.markdown(
            f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:2px;'>"
            f"The Favourites, the Draws, and the Long Shots</h3>"
            f"<p style='color:{C_TEAL};font-size:0.8rem;margin-top:0;margin-bottom:8px;'>"
            f"Average outcome probability per group</p>",
            unsafe_allow_html=True,
        )
        group_avg = (
            df.groupby("group")[PROB_COLS]
            .mean()
            .reset_index()
            .melt(id_vars="group", var_name="Outcome", value_name="Probability")
        )
        group_avg["Outcome"] = group_avg["Outcome"].map(
            {"home_win": "Home Win", "draw": "Draw", "away_win": "Away Win"}
        )
        fig_bar = px.bar(
            group_avg, x="Probability", y="group", color="Outcome",
            orientation="h", barmode="group",
            color_discrete_map={"Home Win": C_GREEN, "Draw": C_TEAL, "Away Win": C_RED},
            template=PLOTLY_TEMPLATE,
            labels={"group": "Group", "Probability": "Avg Probability"},
            text_auto=".1%",
        )
        fig_bar.update_layout(
            height=440,
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1,
                        font=dict(color=C_MINT, size=11)),
            xaxis_tickformat=".0%",
            **CHART_LAYOUT,
        )
        fig_bar.update_traces(textfont_size=10, textfont_color=C_TEXT)
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.divider()
        st.markdown(
            f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:2px;'>"
            f"Where the Uncertainty Lives</h3>"
            f"<p style='color:{C_TEAL};font-size:0.8rem;margin-top:0;margin-bottom:8px;'>"
            f"Within-Group Competitive Parity Score · colour = avg away-win</p>",
            unsafe_allow_html=True,
        )
        bal_df = (
            df.groupby("group")
            .agg(balance=("home_win", lambda x: 1 - x.std()), avg_away=("away_win", "mean"))
            .reset_index()
            .sort_values("balance", ascending=True)
        )
        fig_bal = px.bar(
            bal_df, x="balance", y="group", orientation="h",
            color="avg_away",
            color_continuous_scale=[C_GREEN, C_TEAL, C_RED],
            template=PLOTLY_TEMPLATE,
            labels={
                "balance":  "Balance (higher = more competitive)",
                "group":    "Group",
                "avg_away": "Avg Away-Win",
            },
            text_auto=".2f",
        )
        fig_bal.update_layout(
            height=440,
            coloraxis_colorbar=dict(
                title="Avg<br>Away-Win", tickformat=".0%", thickness=10, len=0.65,
                title_font=dict(color=C_MINT, size=11),
                tickfont=dict(color=C_MINT),
            ),
            **CHART_LAYOUT,
        )
        fig_bal.update_traces(textfont_size=11, textfont_color=C_TEXT)
        st.plotly_chart(fig_bal, use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 3 — Expected Upset Rate (by group)
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:2px;'>"
        f"🎲 Expected Upset Rate (by group)</h3>"
        f"<p style='color:{C_TEAL};font-size:0.8rem;margin-top:0;margin-bottom:8px;'>"
        f"Upset score = 1 − max(home_win, draw, away_win) · higher = no outcome dominates</p>",
        unsafe_allow_html=True,
    )
    upset_chart_df = (
        group_upset.reset_index()
        .rename(columns={"group": "Group", "upset_score": "Upset Score"})
        .sort_values("Upset Score", ascending=True)
    )
    fig_upset = px.bar(
        upset_chart_df, x="Upset Score", y="Group", orientation="h",
        template=PLOTLY_TEMPLATE, color="Upset Score",
        color_continuous_scale=[C_GREEN, C_TEAL, C_RED],
        text_auto=".1%",
    )
    fig_upset.update_layout(
        height=340,
        xaxis_tickformat=".0%",
        coloraxis_showscale=False,
        **CHART_LAYOUT,
    )
    fig_upset.update_traces(textfont_size=11, textfont_color=C_TEXT)
    st.plotly_chart(fig_upset, use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 4 — GROUP DETAIL TABLE
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:4px;'>"
        f"📋 Group {sel_group} — All Matches</h3>",
        unsafe_allow_html=True,
    )

    filtered     = df[df["group"] == sel_group].copy()
    extra_cols   = [c for c in ["date", "tournament", "elo_diff", "home_injury_flag", "away_injury_flag"]
                    if c in filtered.columns]
    display_cols = ["team1", "team2"] + extra_cols + PROB_COLS + ["upset_score"]

    display_df = filtered[display_cols].copy()
    for col in PROB_COLS + ["upset_score"]:
        display_df[col] = display_df[col].map("{:.1%}".format)

    display_df.columns = [c.replace("_", " ").title() for c in display_df.columns]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.markdown(
        f"<p style='color:{C_TEAL};font-size:0.78rem;margin-top:4px;'>"
        f"{len(filtered)} match(es) in Group {sel_group}</p>",
        unsafe_allow_html=True,
    )

    # ── PAGE FOOTER ───────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="margin-top:48px;padding-top:16px;
                    border-top:1px solid {C_GLASS_BD};text-align:center;">
            <p style="color:{C_TEAL};font-size:0.75rem;margin:0;">
                Built with public data &nbsp;·&nbsp; &nbsp;·&nbsp; Just probabilities
                by Eshwaree Mathanki
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


with tab2:
    # ══════════════════════════════════════════════════════════════════════════
    #  DATA GUIDE
    # ══════════════════════════════════════════════════════════════════════════

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="text-align:center;padding:40px 0 8px 0;">
            <p style="color:{C_MINT};font-size:0.78rem;font-weight:600;
                      text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">
                Reference
            </p>
            <h2 style="color:{C_WHITE};font-size:2rem;font-weight:700;
                       letter-spacing:-0.02em;margin:0 0 10px 0;">
                How to Read This Dashboard
            </h2>
            <p style="color:{C_TEAL};font-size:1.05rem;font-weight:400;
                      max-width:560px;margin:0 auto 32px auto;line-height:1.55;">
                A quick guide to the five metrics that power every chart,
                number, and story you see.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Intro paragraph ───────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            max-width:680px;margin:0 auto 36px auto;
            padding:20px 26px;
            background:{C_GLASS_BG};
            border-left:4px solid {C_TEAL};
            border-radius:0 12px 12px 0;
            box-shadow:{C_GLASS_SHA};
            backdrop-filter:blur(12px);
            font-size:0.97rem;color:{C_TEXT};line-height:1.65;
        ">
            This dashboard doesn't just show raw odds — it layers Elo‑based
            probabilities into three ideas: who's the favourite, how tight the
            match is, and where surprises are most likely. Below, each term is
            explained in plain language, with a note on where to spot it on the
            main dashboard.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 5 Core Terms — 2-column progressive-disclosure cards ─────────────────
    TERMS = [
        {
            "icon":     "📊",
            "term":     "Elo Rating & Elo Diff",
            "snapshot": "The strength score behind every team, and the gap between two opponents.",
            "detail":   (
                "An Elo-based probability, also known as the expected score, is the statistical likelihood that one competitor will defeat another based on the difference between their ratings."
                "An Elo rating goes up when a team wins and down when they lose. "
                "The Elo Diff is simply the home team's rating minus the away team's rating. "
                "A large positive diff means a clear favourite; a diff near zero means the model "
                "sees two equals. On the dashboard, this isn't shown directly — but it's the "
                "invisible engine that generates all the win/draw/loss probabilities you see in "
                "the match detail table."
            ),
            "where":    "You'll find the raw Elo Diff column in the Group Match Table at the bottom of the main dashboard.",
            "accent":   C_TEAL,
        },
        {
            "icon":     "🎯",
            "term":     "Win, Draw & Away Probabilities",
            "snapshot": "The model's best guess at how a match will end — always adding to 100%.",
            "detail":   (
                "These three numbers are the building blocks of the entire tournament forecast. "
                "A high Draw probability flags a group where points are constantly shared. "
                "A high Away Win probability signals matches where the underdog has a real chance. "
                "You can explore them for every single match using the sidebar selectors on the main dashboard."
            ),
            "where":    "Visible in the Match Inspector gauges and progress bars, and in the Group Match Table.",
            "accent":   C_GREEN,
        },
        {
            "icon":     "🎲",
            "term":     "Expected Upset Rate",
            "snapshot": "How evenly the odds are split. A high score means no single outcome dominates.",
            "detail":   (
                "Expected Upset Rate = 1 – the single most likely result. "
                "If the favourite is a 60% lock, the upset potential is 40%. "
                "The match with the highest upset potential is the one where the model is basically shrugging. "
                "On the main dashboard, this is the core story of the 'Upset Potential by Group' bar chart — "
                "the group with the tallest bar is where chaos is most likely to strike."
            ),
            "where":    "See the 'Upset Potential by Group' bar chart and the 'Most Unpredictable Group' KPI card.",
            "accent":   C_RED,
        },
        {
            "icon":     "🔄",
            "term":     "Within-Group Competitive Parity",
            "snapshot": "How evenly matched a whole group is — a low score means no easy games.",
            "detail":   (
                "This is calculated as 1 minus the standard deviation of home-win probabilities inside a group. "
                "The lower the standard deviation, the more level the playing field. "
                "The 'Where the Uncertainty Lives' chart on the main dashboard ranks every group from most "
                "to least balanced. The group at the top is the statistical 'High Average Strength Group' — where every "
                "match could genuinely go either way."
            ),
            "where":    "See the 'Where the Uncertainty Lives' horizontal bar chart on the main dashboard.",
            "accent":   C_GREEN,
        },
        {
            "icon":     "🐶",
            "term":     "Lower-Tier Win Probability Share",
            "snapshot": "A group where the away team (the underdog)wins more often than expected",
            "detail":   (
                "This highlights the group with the highest average Away Win probability — a direct signal "
                "that favourites don't have it easy. It's a simple but telling number: if away sides are "
                "winning at an elevated rate, the traditional home advantage is being overridden by talent gaps. "
                "Or, more interestingly, by the absence of them."
            ),
            "where":    "The 'Away-Favoured Group' KPI card and the narrative summary at the top of the main dashboard both surface this group directly.",
            "accent":   C_TEAL,
        },
    ]

    # Render in a 2-column grid
    col_a, col_b = st.columns(2, gap="large")
    columns_cycle = [col_a, col_b, col_a, col_b, col_a]   # 5 cards, last in left col

    for idx, term in enumerate(TERMS):
        with columns_cycle[idx]:
            # Card shell
            st.markdown(
                f"""
                <div style="
                    background:{C_GLASS_BG};
                    border:1px solid {C_GLASS_BD};
                    border-top:4px solid {term['accent']};
                    border-radius:14px;
                    padding:20px 22px 6px 22px;
                    box-shadow:{C_GLASS_SHA};
                    backdrop-filter:blur(12px);
                    margin-bottom:4px;
                ">
                    <p style="font-size:1.6rem;margin:0 0 6px 0;">{term['icon']}</p>
                    <p style="color:{C_WHITE};font-size:1.0rem;font-weight:700;
                              margin:0 0 6px 0;">{term['term']}</p>
                    <p style="color:{C_TEAL};font-size:0.88rem;font-style:italic;
                              margin:0 0 10px 0;line-height:1.45;">{term['snapshot']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Expander (sits outside card div, directly below)
            with st.expander("Learn more →"):
                st.markdown(
                    f"<p style='color:{C_TEXT};font-size:0.9rem;line-height:1.65;'>"
                    f"{term['detail']}</p>"
                    f"<p style='color:{term['accent']};font-size:0.82rem;font-weight:600;"
                    f"margin-top:10px;'>📍 Where to find it: {term['where']}</p>",
                    unsafe_allow_html=True,
                )
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.divider()

    # ── Section 2 — Limitations note ─────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            max-width:680px;
            margin:8px auto 24px auto;
            padding:22px 26px;
            background:{C_GLASS_BG};
            border:1px solid {C_GLASS_BD};
            border-left:4px solid {C_MINT};
            border-radius:0 14px 14px 0;
            box-shadow:{C_GLASS_SHA};
            backdrop-filter:blur(12px);
        ">
            <p style="color:{C_WHITE};font-size:0.95rem;font-weight:700;margin:0 0 8px 0;">
                Where the model stops, and the real world begins.
            </p>
            <p style="color:{C_TEXT};font-size:0.9rem;line-height:1.65;margin:0;">
                These probabilities are built from a pure Elo‑based model — they don't yet factor
                in squad form, injuries, tactical match‑ups, or travel demands across three host nations.
                Think of this dashboard as the structural layer of tournament uncertainty.
                The real world always adds its own chaos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Footer note ───────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="text-align:center;padding-top:8px;">
            <p style="color:{C_TEAL};font-size:0.78rem;font-style:italic;margin:0;">
                Probabilities are derived from a public Elo-based model.
                They represent likelihoods and probabilities by emath.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
