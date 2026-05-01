import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="World Cup 2026: Win Probability & Competitive Balance",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS  — new brand palette
# ══════════════════════════════════════════════════════════════════════════════
C_BLUE      = "#304ffd"                  # primary blue — home win / positive
C_LIME      = "#afe906"                  # lime green — draws / neutral highlights
C_PURPLE    = "#7921a3"                  # purple — away win / alert
C_CRIMSON   = "#61120e"                  # deep crimson — accent / alert
C_BG        = "#0d0f1a"                  # very dark navy — page background
C_CARD      = "#12152b"                  # card background
C_WHITE     = "#ffffff"
C_TEXT      = "#e8eaf6"                  # near-white body text
C_SUBTEXT   = "#c5cae9"                  # muted body text / labels
C_GLASS_BG  = "rgba(48,79,253,0.12)"    # glassy blue card fill
C_GLASS_BD  = "rgba(175,233,6,0.20)"    # lime glass border
C_GLASS_SHA = "0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.06)"

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
    background: linear-gradient(135deg, {C_BG} 0%, #080a15 60%, #0d0f1a 100%);
    min-height: 100vh;
}}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(48,79,253,0.18) 0%, rgba(13,15,26,0.98) 100%) !important;
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
    color: {C_SUBTEXT} !important;
}}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
    background: rgba(48,79,253,0.15);
    border: 1.5px solid {C_LIME} !important;
    border-radius: 8px;
    color: {C_TEXT};
}}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:focus-within {{
    border-color: {C_LIME} !important;
    box-shadow: 0 0 0 2px rgba(175,233,6,0.25);
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
    color: {C_SUBTEXT} !important;
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
    color: {C_LIME} !important;
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
    color: {C_SUBTEXT} !important;
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

# ── Standardise column names to analytics convention ─────────────────────────
COLUMN_MAP = {
    "home_team":  "home_side",
    "away_team":  "away_side",
    "team1":      "home_side",
    "team2":      "away_side",
    "p_home_win": "home_win_prob",
    "p_draw":     "draw_prob",
    "p_away_win": "away_win_prob",
    "home_win":   "home_win_prob",
    "draw":       "draw_prob",
    "away_win":   "away_win_prob",
}
df = df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns})

REQUIRED = {"group", "home_side", "away_side", "home_win_prob", "draw_prob", "away_win_prob"}
missing  = REQUIRED - set(df.columns)
if missing:
    st.error(f"❌ Missing columns: **{missing}**\n\nFound: `{list(df.columns)}`")
    st.stop()

PROB_COLS = ["home_win_prob", "draw_prob", "away_win_prob"]

# ── Pre-compute aggregates ────────────────────────────────────────────────────
# Upset Index = 1 − max outcome probability (higher = less dominant favourite)
df["upset_index"] = 1 - df[PROB_COLS].max(axis=1)

group_upset_index   = df.groupby("group")["upset_index"].mean()
top_upset_group     = str(group_upset_index.idxmax())
top_upset_val       = float(group_upset_index.max())

# Away-win probability aggregated by group
_away_means         = df.groupby("group", sort=False)["away_win_prob"].mean()
top_away_group      = str(_away_means.idxmax())
top_away_val        = float(_away_means.max())

# Highest single-match draw probability
top_draw_idx        = int(df["draw_prob"].idxmax())
top_draw_home       = df.loc[top_draw_idx, "home_side"]
top_draw_away       = df.loc[top_draw_idx, "away_side"]
top_draw_match      = f"{top_draw_home} vs {top_draw_away}"
top_draw_val        = float(df.loc[top_draw_idx, "draw_prob"])

# Group with highest mean draw probability (most evenly contested group)
_draw_means         = df.groupby("group", sort=False)["draw_prob"].mean()
tight_group         = str(_draw_means.idxmax())
tight_pct           = f"{_draw_means.max() * 100:.1f}"

# ══════════════════════════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(48,79,253,0.08)",
    font          = dict(family=FONT, color=C_SUBTEXT),
    title_font    = dict(color=C_SUBTEXT, size=14, family=FONT),
    xaxis         = dict(
        gridcolor     = "rgba(175,233,6,0.15)",
        gridwidth     = 1,
        griddash      = "solid",
        tickfont      = dict(color=C_SUBTEXT, size=11),
        title_font    = dict(color=C_SUBTEXT),
    ),
    yaxis         = dict(
        gridcolor     = "rgba(175,233,6,0.15)",
        gridwidth     = 1,
        tickfont      = dict(color=C_SUBTEXT, size=11),
        title_font    = dict(color=C_SUBTEXT),
    ),
    margin        = dict(l=10, r=10, t=30, b=10),
)


def make_gauge(value: float, label: str, color: str) -> go.Figure:
    """Render a win-probability speedometer gauge."""
    fig = go.Figure(go.Indicator(
        mode   = "gauge+number",
        value  = value,
        number = {"suffix": "%", "font": {"size": 34, "color": C_WHITE, "family": FONT}},
        title  = {"text": label, "font": {"size": 13, "color": C_SUBTEXT, "family": FONT}},
        gauge  = {
            "axis": {
                "range":     [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(175,233,6,0.35)",
                "tickfont":  {"color": C_SUBTEXT, "size": 9},
            },
            "bar":        {"color": color, "thickness": 0.28},
            "bgcolor":    "rgba(48,79,253,0.2)",
            "borderwidth": 1,
            "bordercolor": "rgba(175,233,6,0.25)",
            "steps": [
                {"range": [0,  33], "color": "rgba(48,79,253,0.12)"},
                {"range": [33, 66], "color": "rgba(175,233,6,0.10)"},
                {"range": [66, 100],"color": "rgba(121,33,163,0.12)"},
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
        f"<p style='color:{C_LIME};font-size:0.85rem;margin-top:0;'>"
        f"Win Probability &amp; Competitive Balance</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── MATCH SELECTOR ───────────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_WHITE};font-size:0.82rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>"
        f"🔍 Match Selector</p>",
        unsafe_allow_html=True,
    )

    match_labels     = (df["home_side"] + " vs " + df["away_side"]).tolist()
    sel_match_label  = st.selectbox("Pick a match", options=match_labels, index=0)

    st.divider()

    # ── UPSET INDEX RANKING ──────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_WHITE};font-size:0.82rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>"
        f"🎲 Upset Index by Group</p>",
        unsafe_allow_html=True,
    )

    upset_ranking = (
        group_upset_index.sort_values(ascending=False)
        .reset_index()
        .rename(columns={"group": "Group", "upset_index": "Upset Index"})
    )
    upset_ranking["Upset Index"] = upset_ranking["Upset Index"].map("{:.1%}".format)

    st.dataframe(upset_ranking, hide_index=True, use_container_width=True)

    st.divider()

    # ── GROUP FILTER ─────────────────────────────────────────────────────────
    groups    = sorted(df["group"].unique())
    sel_group = st.selectbox("Pick a group", options=groups, index=0)

    st.divider()

    # ── CONTEXT TEXT ─────────────────────────────────────────────────────────
    st.markdown(
        f"<p style='color:{C_SUBTEXT};font-size:0.72rem;font-style:italic;"
        f"line-height:1.5;margin-top:4px;'>"
        f"Win probabilities derived from a public Elo-based model.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='color:{C_LIME};font-size:0.68rem;margin-top:6px;'>"
        f"Data: wc_2026_probabilities.csv &nbsp;·&nbsp; {len(df):,} fixtures</p>",
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
            f"<p style='color:{C_LIME};font-size:1.1rem;font-style:italic;"
            f"font-weight:400;margin-top:0;margin-bottom:28px;'>"
            f"Win probability &amp; competitive balance across every group fixture</p>",
            unsafe_allow_html=True,
        )
        # Narrative summary block
        st.markdown(
            f"""
            <div style="
                margin: 0 0 36px 0;
                padding: 20px 24px;
                border-left: 4px solid {C_LIME};
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
                <strong style="color:{C_WHITE}">{len(df)} fixtures</strong>
                across <strong style="color:{C_WHITE}">{df["group"].nunique()} groups</strong>.
                Group&nbsp;<span style="color:{C_LIME};font-weight:600;">{top_away_group}</span>
                carries the highest away-win probability:
                <span style="color:{C_LIME};font-weight:600;">{top_away_val*100:.1f}%</span> on average.
                Group&nbsp;<span style="color:{C_BLUE};font-weight:600;">{tight_group}</span>
                is the most evenly contested, with
                <span style="color:{C_BLUE};font-weight:600;">{tight_pct}%</span>
                of its fixtures projected to end level.
                The match with the narrowest probability margin?
                <span style="font-weight:600;color:{C_WHITE}">{top_draw_home} vs {top_draw_away}</span>;
                draw probability sits at
                <span style="color:{C_PURPLE};font-weight:600;">{top_draw_val*100:.1f}%</span>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with _header_right:
        _img_name = "e97b939610c0b9fbd9d1b2bbcebdd2a2.jpg"
        _img_path = Path(__file__).parent / _img_name
        if _img_path.exists():
            st.image(str(_img_path), use_container_width=True)
        else:
            if os.path.exists(_img_name):
                st.image(_img_name, use_container_width=True)
            else:
                st.markdown(
                    f"<p style='color:{C_LIME};font-size:0.75rem;font-style:italic;"
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
        "Group Stage Fixtures",
        f"{len(df)}",
        delta=f"across {df['group'].nunique()} groups",
    )

    with m2:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_PURPLE};">
                <p style="color:{C_SUBTEXT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Away-Favoured Group</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">Group {top_away_group}</p>
                <p style="color:{C_PURPLE};font-size:0.88rem;font-style:italic;margin:0;">
                    {top_away_val*100:.1f}% mean away-win probability</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_CRIMSON};">
                <p style="color:{C_SUBTEXT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Highest Upset Index Group</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">Group {top_upset_group}</p>
                <p style="color:{C_CRIMSON};font-size:0.88rem;font-style:italic;margin:0;">
                    {top_upset_val*100:.1f}% mean upset index</p>
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
                border-left:4px solid {C_BLUE};">
                <p style="color:{C_SUBTEXT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Highest Draw-Probability Group</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">Group {tight_group}</p>
                <p style="color:{C_BLUE};font-size:0.88rem;font-style:italic;margin:0;">
                    {tight_pct}% mean draw probability</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with n2:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_LIME};">
                <p style="color:{C_SUBTEXT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Highest Single-Fixture Draw Prob.</p>
                <p style="color:{C_WHITE};font-size:1.15rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.3;">{top_draw_home}<br>vs {top_draw_away}</p>
                <p style="color:{C_LIME};font-size:0.88rem;font-style:italic;margin:0;">
                    {top_draw_val*100:.1f}% draw probability</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with n3:
        st.markdown(
            f"""<div style="background:{C_GLASS_BG};border:1px solid {C_GLASS_BD};
                border-radius:16px;padding:20px 22px 16px 22px;
                box-shadow:{C_GLASS_SHA};backdrop-filter:blur(12px);
                border-left:4px solid {C_LIME};">
                <p style="color:{C_SUBTEXT};font-size:0.75rem;font-weight:600;text-transform:uppercase;
                          letter-spacing:0.5px;margin:0 0 6px 0;">Total Groups</p>
                <p style="color:{C_WHITE};font-size:2.0rem;font-weight:700;margin:0 0 4px 0;
                          line-height:1.1;">{df["group"].nunique()}</p>
                <p style="color:{C_LIME};font-size:0.88rem;font-style:italic;margin:0;">
                    Groups A – {sorted(df["group"].unique())[-1]} · 6 fixtures each</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 1 — MATCH INSPECTOR (gauges first, probability bars below)
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<h2 style='color:{C_WHITE};font-size:1.5rem;font-weight:600;margin-bottom:4px;'>"
        f"🔍 Match Probability Breakdown — {sel_match_label}</h2>",
        unsafe_allow_html=True,
    )

    _home, _away  = sel_match_label.split(" vs ", 1)
    match_row     = df[(df["home_side"] == _home) & (df["away_side"] == _away)].iloc[0]

    _home_prob = float(match_row["home_win_prob"]) * 100
    _draw_prob = float(match_row["draw_prob"])     * 100
    _away_prob = float(match_row["away_win_prob"]) * 100

    # — Probability gauges —
    sp1, sp2, sp3 = st.columns(3)
    with sp1:
        st.plotly_chart(
            make_gauge(_home_prob, f"🏠 Home Win — {_home}", C_BLUE),
            use_container_width=True, config={"displayModeBar": False},
        )
    with sp2:
        st.plotly_chart(
            make_gauge(_draw_prob, "🤝 Draw Probability", C_LIME),
            use_container_width=True, config={"displayModeBar": False},
        )
    with sp3:
        st.plotly_chart(
            make_gauge(_away_prob, f"✈️ Away Win — {_away}", C_PURPLE),
            use_container_width=True, config={"displayModeBar": False},
        )

    # — Probability bar tiles —
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
            <p style="color:{C_SUBTEXT};font-size:0.72rem;font-weight:600;text-transform:uppercase;
                      letter-spacing:0.6px;margin:0 0 4px 0;">{team_label}</p>
            <p style="color:{C_WHITE};font-size:2.2rem;font-weight:700;margin:0 0 8px 0;
                      line-height:1;">{pct:.1f}<span style="font-size:1rem;font-weight:400;">%</span></p>
            <p style="color:{C_SUBTEXT};font-size:0.8rem;margin:0 0 10px 0;">{outcome}</p>
            <div style="background:rgba(255,255,255,0.08);border-radius:99px;height:6px;overflow:hidden;">
                <div style="width:{bar_w};height:100%;background:{color};border-radius:99px;"></div>
            </div>
        </div>"""

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown(prob_card(f"🏠 {_home}", "Home Win Probability", _home_prob, C_BLUE), unsafe_allow_html=True)
    with g2:
        st.markdown(prob_card("🤝 Draw", "Neither side wins", _draw_prob, C_LIME), unsafe_allow_html=True)
    with g3:
        st.markdown(prob_card(f"✈️ {_away}", "Away Win Probability", _away_prob, C_PURPLE), unsafe_allow_html=True)

    # — Most probable outcome banner —
    _outcome_map = {
        "Home Win": (_home_prob, C_BLUE),
        "Draw":     (_draw_prob, C_LIME),
        "Away Win": (_away_prob, C_PURPLE),
    }
    _dom           = max(_outcome_map, key=lambda k: _outcome_map[k][0])
    _dom_val, _dom_color = _outcome_map[_dom]
    _icons         = {"Home Win": "🏠", "Draw": "🤝", "Away Win": "✈️"}
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
            <span style="color:{C_SUBTEXT};font-size:0.7rem;text-transform:uppercase;
                         letter-spacing:0.6px;font-weight:600;">Most probable outcome</span><br>
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
            f"Win Probability Distribution by Group</h3>"
            f"<p style='color:{C_LIME};font-size:0.8rem;margin-top:0;margin-bottom:8px;'>"
            f"Mean outcome probability per group — home win · draw · away win</p>",
            unsafe_allow_html=True,
        )
        group_avg = (
            df.groupby("group")[PROB_COLS]
            .mean()
            .reset_index()
            .melt(id_vars="group", var_name="Outcome", value_name="Probability")
        )
        group_avg["Outcome"] = group_avg["Outcome"].map({
            "home_win_prob": "Home Win",
            "draw_prob":     "Draw",
            "away_win_prob": "Away Win",
        })
        fig_bar = px.bar(
            group_avg, x="Probability", y="group", color="Outcome",
            orientation="h", barmode="group",
            color_discrete_map={"Home Win": C_BLUE, "Draw": C_LIME, "Away Win": C_PURPLE},
            template=PLOTLY_TEMPLATE,
            labels={"group": "Group", "Probability": "Mean Probability"},
            text_auto=".1%",
        )
        fig_bar.update_layout(
            height=440,
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1,
                        font=dict(color=C_SUBTEXT, size=11)),
            xaxis_tickformat=".0%",
            **CHART_LAYOUT,
        )
        fig_bar.update_traces(textfont_size=10, textfont_color=C_TEXT)
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.divider()
        st.markdown(
            f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:2px;'>"
            f"Competitive Balance Index by Group</h3>"
            f"<p style='color:{C_LIME};font-size:0.8rem;margin-top:0;margin-bottom:8px;'>"
            f"Balance score · colour = mean away-win probability</p>",
            unsafe_allow_html=True,
        )
        # Competitive Balance Index = 1 − σ(home_win_prob) within group
        # Higher score → more equal home/away strength → more competitive group
        bal_df = (
            df.groupby("group")
            .agg(
                competitive_balance=("home_win_prob", lambda x: 1 - x.std()),
                mean_away_win_prob=("away_win_prob", "mean"),
            )
            .reset_index()
            .sort_values("competitive_balance", ascending=True)
        )
        fig_bal = px.bar(
            bal_df, x="competitive_balance", y="group", orientation="h",
            color="mean_away_win_prob",
            color_continuous_scale=[C_BLUE, C_LIME, C_PURPLE],
            template=PLOTLY_TEMPLATE,
            labels={
                "competitive_balance":  "Competitive Balance Index (higher = more equal)",
                "group":                "Group",
                "mean_away_win_prob":   "Mean Away-Win Prob.",
            },
            text_auto=".2f",
        )
        fig_bal.update_layout(
            height=440,
            coloraxis_colorbar=dict(
                title="Mean<br>Away-Win", tickformat=".0%", thickness=10, len=0.65,
                title_font=dict(color=C_SUBTEXT, size=11),
                tickfont=dict(color=C_SUBTEXT),
            ),
            **CHART_LAYOUT,
        )
        fig_bal.update_traces(textfont_size=11, textfont_color=C_TEXT)
        st.plotly_chart(fig_bal, use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════════
    #  SECTION 3 — UPSET INDEX
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:2px;'>"
        f"🎲 Upset Index by Group</h3>"
        f"<p style='color:{C_LIME};font-size:0.8rem;margin-top:0;margin-bottom:8px;'>"
        f"Upset Index = 1 − max(home_win_prob, draw_prob, away_win_prob) &nbsp;·&nbsp; higher = no dominant outcome</p>",
        unsafe_allow_html=True,
    )
    upset_chart_df = (
        group_upset_index.reset_index()
        .rename(columns={"group": "Group", "upset_index": "Upset Index"})
        .sort_values("Upset Index", ascending=True)
    )
    fig_upset = px.bar(
        upset_chart_df, x="Upset Index", y="Group", orientation="h",
        template=PLOTLY_TEMPLATE, color="Upset Index",
        color_continuous_scale=[C_BLUE, C_LIME, C_PURPLE],
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
    #  SECTION 4 — GROUP FIXTURE TABLE
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<h3 style='color:{C_WHITE};font-size:1.05rem;font-weight:600;margin-bottom:4px;'>"
        f"📋 Group {sel_group} — All Fixtures</h3>",
        unsafe_allow_html=True,
    )

    filtered   = df[df["group"] == sel_group].copy()
    extra_cols = [c for c in ["date", "tournament", "elo_diff", "home_injury_flag", "away_injury_flag"]
                  if c in filtered.columns]
    display_cols = ["home_side", "away_side"] + extra_cols + PROB_COLS + ["upset_index"]

    display_df = filtered[display_cols].copy()
    for col in PROB_COLS + ["upset_index"]:
        display_df[col] = display_df[col].map("{:.1%}".format)

    # Human-readable column headers
    display_df = display_df.rename(columns={
        "home_side":      "Home Side",
        "away_side":      "Away Side",
        "home_win_prob":  "Home Win Prob.",
        "draw_prob":      "Draw Prob.",
        "away_win_prob":  "Away Win Prob.",
        "upset_index":    "Upset Index",
        "elo_diff":       "Elo Differential",
    })
    display_df.columns = [c.replace("_", " ").title() if c not in display_df.columns else c
                          for c in display_df.columns]

    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.markdown(
        f"<p style='color:{C_LIME};font-size:0.78rem;margin-top:4px;'>"
        f"{len(filtered)} fixture(s) in Group {sel_group}</p>",
        unsafe_allow_html=True,
    )

    # ── PAGE FOOTER ───────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="margin-top:48px;padding-top:16px;
                    border-top:1px solid {C_GLASS_BD};text-align:center;">
            <p style="color:{C_LIME};font-size:0.75rem;margin:0;">
                Built with public data &nbsp;·&nbsp; Elo-based win probabilities
                &nbsp;·&nbsp; by Eshwaree Mathanki
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — DATA GUIDE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="text-align:center;padding:40px 0 8px 0;">
            <p style="color:{C_SUBTEXT};font-size:0.78rem;font-weight:600;
                      text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">
                Reference
            </p>
            <h2 style="color:{C_WHITE};font-size:2rem;font-weight:700;
                       letter-spacing:-0.02em;margin:0 0 10px 0;">
                How to Read This Dashboard
            </h2>
            <p style="color:{C_LIME};font-size:1.05rem;font-weight:400;
                      max-width:560px;margin:0 auto 32px auto;line-height:1.55;">
                Plain-language definitions for every metric — with formulae where they help.
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
            border-left:4px solid {C_LIME};
            border-radius:0 12px 12px 0;
            box-shadow:{C_GLASS_SHA};
            backdrop-filter:blur(12px);
            font-size:0.97rem;color:{C_TEXT};line-height:1.65;
        ">
            This dashboard converts Elo ratings into match probabilities and layers them
            into three analytical questions: <em>Who is the favourite?</em>
            <em>How open is the contest?</em> <em>Where are upsets most likely?</em>
            Each term below is defined in plain language, with a formula and a pointer
            to where you'll find it on the main dashboard.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 5 Core Terms ─────────────────────────────────────────────────────────
    TERMS = [
        {
            "icon":     "📊",
            "term":     "Elo Rating & Elo Differential",
            "snapshot": "A team's strength score, and the gap between two opponents.",
            "detail":   (
                "<strong>Elo Rating</strong> is a numerical measure of team strength. "
                "It rises after a win and falls after a loss, scaled by the quality of the opponent. "
                "<br><br>"
                "<strong>Elo Differential</strong> = Home team Elo − Away team Elo. "
                "A large positive differential signals a clear favourite; a value near zero means "
                "the model rates both sides roughly equal. "
                "The differential is the input used to calculate all three outcome probabilities. "
                "<br><br>"
                "📐 <em>Formula (expected score / home-win probability):</em><br>"
                "<code>P(home win) = 1 / (1 + 10^(−ΔElo / 400))</code>"
            ),
            "where":    "The raw Elo Differential column appears in the Group Fixture Table at the bottom of the main dashboard.",
            "accent":   C_LIME,
        },
        {
            "icon":     "🎯",
            "term":     "Win, Draw & Away-Win Probability",
            "snapshot": "The model's estimated likelihood for each of the three possible match outcomes — always summing to 100%.",
            "detail":   (
                "These three probabilities are derived from the Elo differential using a logistic transformation. "
                "Together they always sum to 1 (100%). "
                "<br><br>"
                "• <strong>Home Win Prob.</strong> — likelihood the home side wins in 90 minutes.<br>"
                "• <strong>Draw Prob.</strong> — likelihood neither side wins.<br>"
                "• <strong>Away Win Prob.</strong> — likelihood the away side wins.<br><br>"
                "A high draw probability flags a group where points are frequently shared. "
                "A high away-win probability signals fixtures where the road side has a genuine chance, "
                "often because the talent gap overrides home advantage."
            ),
            "where":    "Visible in the Match Probability Breakdown gauges and bars, and in the Group Fixture Table.",
            "accent":   C_BLUE,
        },
        {
            "icon":     "🎲",
            "term":     "Upset Index",
            "snapshot": "How evenly spread the odds are. A higher score means no single outcome dominates.",
            "detail":   (
                "The Upset Index measures outcome uncertainty for a single fixture or a group average. "
                "<br><br>"
                "📐 <em>Formula:</em><br>"
                "<code>Upset Index = 1 − max(home_win_prob, draw_prob, away_win_prob)</code><br><br>"
                "If the favourite carries a 70% win probability, the Upset Index is 30%. "
                "If no outcome exceeds 40%, the index climbs above 60% — signalling maximum unpredictability. "
                "The group with the highest <em>mean</em> Upset Index is statistically the hardest to forecast."
            ),
            "where":    "See the 'Upset Index by Group' bar chart and the 'Highest Upset Index Group' KPI card.",
            "accent":   C_CRIMSON,
        },
        {
            "icon":     "🔄",
            "term":     "Competitive Balance Index",
            "snapshot": "How evenly matched a whole group is — a higher score means fewer easy games.",
            "detail":   (
                "The Competitive Balance Index captures the spread of home-win probabilities within a group. "
                "If all fixtures in a group have similar home-win probabilities, the standard deviation is low "
                "and the balance score is high — meaning no team is a runaway favourite. "
                "<br><br>"
                "📐 <em>Formula:</em><br>"
                "<code>Competitive Balance Index = 1 − σ(home_win_prob)</code><br>"
                "where σ is the standard deviation of home-win probabilities across all fixtures in the group.<br><br>"
                "The group with the highest index is the statistical 'Group of Death' — every fixture is genuinely open."
            ),
            "where":    "See the 'Competitive Balance Index by Group' horizontal bar chart on the main dashboard.",
            "accent":   C_BLUE,
        },
        {
            "icon":     "🐶",
            "term":     "Away-Favoured Group",
            "snapshot": "The group where away sides win more often than the tournament average.",
            "detail":   (
                "This metric highlights the group with the highest <strong>mean away-win probability</strong> "
                "across all its fixtures. "
                "<br><br>"
                "📐 <em>Formula:</em><br>"
                "<code>Away-Win Mean (group) = Σ away_win_prob / n</code><br>"
                "where n = number of fixtures in the group.<br><br>"
                "When away sides carry elevated win probabilities, it typically means the talent differential "
                "between teams in that group overrides any home-advantage effect — or simply that the "
                "group contains few dominant home favourites."
            ),
            "where":    "The 'Away-Favoured Group' KPI card and the narrative summary at the top of the main dashboard.",
            "accent":   C_LIME,
        },
    ]

    col_a, col_b = st.columns(2, gap="large")
    columns_cycle = [col_a, col_b, col_a, col_b, col_a]

    for idx, term in enumerate(TERMS):
        with columns_cycle[idx]:
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
                    <p style="color:{C_LIME};font-size:0.88rem;font-style:italic;
                              margin:0 0 10px 0;line-height:1.45;">{term['snapshot']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
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

    # ── Model Limitations note ────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            max-width:680px;
            margin:8px auto 24px auto;
            padding:22px 26px;
            background:{C_GLASS_BG};
            border:1px solid {C_GLASS_BD};
            border-left:4px solid {C_SUBTEXT};
            border-radius:0 14px 14px 0;
            box-shadow:{C_GLASS_SHA};
            backdrop-filter:blur(12px);
        ">
            <p style="color:{C_WHITE};font-size:0.95rem;font-weight:700;margin:0 0 8px 0;">
                Model scope and limitations.
            </p>
            <p style="color:{C_TEXT};font-size:0.9rem;line-height:1.65;margin:0;">
                These probabilities are generated by a pure Elo-based model. The model does not
                incorporate in-tournament form, squad injuries, tactical matchups, or the logistical
                demands of a three-host-nation tournament. Treat this dashboard as a structural
                baseline for tournament uncertainty — contextual factors will always introduce
                variance that a rating-only model cannot anticipate.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="text-align:center;padding-top:8px;">
            <p style="color:{C_LIME};font-size:0.78rem;font-style:italic;margin:0;">
                Win probabilities derived from a public Elo-based model (emath).
                All figures represent statistical likelihoods, not guarantees.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
