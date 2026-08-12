import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from textwrap import dedent


# ============================================================
# FORECASTOPTI
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

FORECAST_DIR = PROJECT_DIR / "outputs" / "forecasts"
EVALUATION_DIR = PROJECT_DIR / "outputs" / "evaluation"
OPTIMIZATION_DIR = PROJECT_DIR / "outputs" / "optimization"
CLUSTERING_DIR = PROJECT_DIR / "outputs" / "clustering"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ForecastOpti",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL HTML
# ============================================================

def html(markup):

    cleaned = dedent(markup).strip()

    cleaned = "\n".join(
        line.strip()
        for line in cleaned.splitlines()
        if line.strip()
    )

    st.markdown(
        cleaned,
        unsafe_allow_html=True
    )


# ============================================================
# SAFE DATAFRAME
# ============================================================

def safe_dataframe(df):

    if df is None:
        return pd.DataFrame()

    result = df.copy()

    for column in result.columns:

        if pd.api.types.is_object_dtype(
            result[column]
        ):

            result[column] = (
                result[column]
                .fillna("")
                .astype(str)
            )

    return result


def display_dataframe(
    df,
    height=None
):

    safe_df = safe_dataframe(df)

    kwargs = {
        "hide_index": True,
        "width": "stretch",
    }

    if height is not None:
        kwargs["height"] = height

    st.dataframe(
        safe_df,
        **kwargs
    )


# ============================================================
# VALUE HELPERS
# ============================================================

def safe_float(
    value,
    default=0
):

    try:

        if pd.isna(value):
            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def safe_int(
    value,
    default=0
):

    try:

        if pd.isna(value):
            return default

        return int(
            float(value)
        )

    except (
        TypeError,
        ValueError
    ):

        return default


def safe_text(
    value,
    default="-"
):

    if value is None:
        return default

    try:

        if pd.isna(value):
            return default

    except TypeError:
        pass

    return str(value)


def number(value):

    return f"{safe_float(value):,.2f}"


def integer(value):

    return f"{safe_float(value):,.0f}"


def percentage(value):

    return f"{safe_float(value):.2f}%"


# ============================================================
# CSV
# ============================================================

def load_csv(
    directory,
    filename
):

    path = directory / filename

    if not path.exists():
        return None

    try:

        return pd.read_csv(path)

    except Exception:

        return None


# ============================================================
# CUSTOM CSS
# ============================================================

html(
"""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

:root {

    --bg: #f6f7fb;

    --surface: #ffffff;

    --surface-soft: #f9fafb;

    --border: #e7e9ee;

    --text: #1f2937;

    --muted: #8a93a3;

    --blue: #2563eb;

    --blue-soft: #eef4ff;

    --green: #18a66a;

    --green-soft: #eaf8f1;

    --orange: #e89b25;

    --orange-soft: #fff6e8;

    --red: #df5757;

    --red-soft: #fff0f0;

    --dark: #151923;
}


.stApp {

    background:
        var(--bg) !important;

    color:
        var(--text) !important;
}


.block-container {

    max-width:
        1500px !important;

    padding-top:
        1.1rem !important;

    padding-bottom:
        3rem !important;

    padding-left:
        2rem !important;

    padding-right:
        2rem !important;
}


/* ============================================================
   REMOVE DEFAULT STREAMLIT ELEMENTS
   ============================================================ */

#MainMenu {

    visibility:
        hidden;
}


footer {

    visibility:
        hidden;
}


header {

    background:
        transparent !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {

    background:
        #ffffff !important;

    border-right:
        1px solid #e7e9ee !important;
}


[data-testid="stSidebar"] > div:first-child {

    background:
        #ffffff !important;

    padding:
        1.2rem 0.8rem !important;
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.brand {

    padding:
        0.4rem 0.65rem 1.5rem 0.65rem;
}


.brand-name {

    color:
        #172033 !important;

    font-size:
        20px !important;

    font-weight:
        800 !important;

    letter-spacing:
        -0.03em !important;
}


.brand-subtitle {

    color:
        #9aa2b1 !important;

    font-size:
        10px !important;

    margin-top:
        4px !important;
}


/* ============================================================
   SIDEBAR LABEL
   ============================================================ */

.sidebar-label {

    color:
        #a0a7b4 !important;

    font-size:
        9px !important;

    font-weight:
        800 !important;

    text-transform:
        uppercase !important;

    letter-spacing:
        .14em !important;

    padding:
        0.2rem 0.65rem 0.5rem 0.65rem !important;
}


/* ============================================================
   NAVIGATION BUTTON
   ============================================================ */

[data-testid="stSidebar"]
.stButton {

    margin:
        0 !important;

    padding:
        0 !important;
}


[data-testid="stSidebar"]
.stButton > button {

    width:
        100% !important;

    min-height:
        42px !important;

    border:
        1px solid transparent !important;

    border-radius:
        10px !important;

    background:
        transparent !important;

    color:
        #667085 !important;

    text-align:
        left !important;

    font-size:
        12px !important;

    font-weight:
        600 !important;

    margin:
        2px 0 !important;

    padding:
        8px 11px !important;

    box-shadow:
        none !important;
}


[data-testid="stSidebar"]
.stButton > button:hover {

    background:
        #f5f7fa !important;

    color:
        #172033 !important;

    border-color:
        #edf0f4 !important;
}


[data-testid="stSidebar"]
.stButton > button p {

    color:
        inherit !important;

    font-size:
        12px !important;

    font-weight:
        600 !important;
}


/* ============================================================
   ACTIVE NAV
   ============================================================ */

[data-testid="stSidebar"]
.nav-active {

    background:
        #edf4ff !important;

    color:
        #2563eb !important;

    border:
        1px solid #dce9ff !important;

    box-shadow:
        inset 3px 0 0 #2563eb !important;
}


[data-testid="stSidebar"]
.nav-active p {

    color:
        #2563eb !important;
}


/* ============================================================
   SIDEBAR FOOTER
   ============================================================ */

.sidebar-footer {

    border-top:
        1px solid #edf0f3;

    margin-top:
        1.5rem;

    padding:
        1rem 0.65rem;

    color:
        #a0a7b4;

    font-size:
        9px;

    line-height:
        1.6;
}


/* ============================================================
   TOP HEADER
   ============================================================ */

.topbar {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    margin-bottom:
        1.2rem;
}


.page-title {

    color:
        #172033 !important;

    font-size:
        24px !important;

    font-weight:
        800 !important;

    letter-spacing:
        -0.03em !important;

    margin:
        0 !important;
}


.page-subtitle {

    color:
        #9aa2b1 !important;

    font-size:
        11px !important;

    margin-top:
        4px !important;
}


.status-pill {

    display:
        inline-flex;

    align-items:
        center;

    gap:
        6px;

    background:
        #ecfdf3;

    color:
        #168653;

    border:
        1px solid #d7f5e4;

    border-radius:
        999px;

    padding:
        6px 10px;

    font-size:
        10px;

    font-weight:
        800;
}


.status-dot {

    width:
        6px;

    height:
        6px;

    background:
        #20b875;

    border-radius:
        50%;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    background:
        linear-gradient(
            135deg,
            #172033 0%,
            #263e6e 60%,
            #2563eb 100%
        );

    border-radius:
        18px;

    padding:
        26px 30px;

    margin-bottom:
        22px;

    box-shadow:
        0 14px 35px
        rgba(31, 41, 55, .10);
}


.hero-label {

    color:
        #a9c8ff;

    font-size:
        9px;

    font-weight:
        800;

    letter-spacing:
        .18em;
}


.hero-title {

    color:
        #ffffff;

    font-size:
        29px;

    font-weight:
        800;

    margin-top:
        6px;
}


.hero-description {

    color:
        #d9e5f7;

    font-size:
        12px;

    line-height:
        1.6;

    max-width:
        700px;

    margin-top:
        7px;
}


/* ============================================================
   KPI CARD
   ============================================================ */

.kpi {

    background:
        #ffffff;

    border:
        1px solid #e8ebef;

    border-radius:
        14px;

    padding:
        15px 17px;

    min-height:
        105px;

    box-shadow:
        0 5px 18px
        rgba(16, 24, 40, .035);
}


.kpi-label {

    color:
        #98a2b3;

    font-size:
        10px;

    font-weight:
        600;
}


.kpi-value {

    color:
        #172033;

    font-size:
        25px;

    font-weight:
        800;

    margin-top:
        8px;

    letter-spacing:
        -0.03em;
}


.kpi-description {

    color:
        #98a2b3;

    font-size:
        9px;

    margin-top:
        4px;
}


.kpi-blue {

    border-top:
        3px solid #2563eb;
}


.kpi-green {

    border-top:
        3px solid #18a66a;
}


.kpi-orange {

    border-top:
        3px solid #e89b25;
}


.kpi-red {

    border-top:
        3px solid #df5757;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-head {

    display:
        flex;

    align-items:
        flex-end;

    justify-content:
        space-between;

    margin-top:
        24px;

    margin-bottom:
        10px;
}


.section-title {

    color:
        #172033;

    font-size:
        16px;

    font-weight:
        800;
}


.section-description {

    color:
        #9aa2b1;

    font-size:
        10px;

    margin-top:
        3px;
}


/* ============================================================
   CARD
   ============================================================ */

.dashboard-card {

    background:
        #ffffff;

    border:
        1px solid #e8ebef;

    border-radius:
        15px;

    padding:
        17px;

    box-shadow:
        0 5px 18px
        rgba(16, 24, 40, .035);

    margin-bottom:
        16px;
}


.card-title {

    color:
        #252d3d;

    font-size:
        13px;

    font-weight:
        800;
}


.card-subtitle {

    color:
        #9aa2b1;

    font-size:
        9px;

    margin-top:
        3px;

    margin-bottom:
        10px;
}


/* ============================================================
   RISK
   ============================================================ */

.risk-card {

    background:
        #ffffff;

    border:
        1px solid #e8ebef;

    border-radius:
        15px;

    padding:
        18px;

    height:
        100%;

    box-shadow:
        0 5px 18px
        rgba(16, 24, 40, .035);
}


.risk-item {

    padding:
        13px 0;

    border-bottom:
        1px solid #f0f1f4;
}


.risk-item:last-child {

    border-bottom:
        none;
}


.risk-row {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;
}


.risk-name {

    color:
        #667085;

    font-size:
        11px;

    font-weight:
        600;
}


.risk-number {

    color:
        #172033;

    font-size:
        20px;

    font-weight:
        800;
}


.risk-badge {

    display:
        inline-block;

    padding:
        4px 8px;

    border-radius:
        999px;

    font-size:
        8px;

    font-weight:
        800;

    margin-top:
        4px;
}


.risk-high {

    background:
        #fff0f0;

    color:
        #c43d3d;
}


.risk-medium {

    background:
        #fff6e8;

    color:
        #b87913;
}


.risk-low {

    background:
        #eaf8f1;

    color:
        #168653;
}


/* ============================================================
   FILTER
   ============================================================ */

.filter-card {

    background:
        #ffffff;

    border:
        1px solid #e8ebef;

    border-radius:
        13px;

    padding:
        10px 13px;

    margin-bottom:
        15px;
}


/* ============================================================
   STREAMLIT METRICS
   ============================================================ */

div[data-testid="stMetric"] {

    background:
        #ffffff !important;

    border:
        1px solid #e8ebef !important;

    border-radius:
        14px !important;

    padding:
        14px !important;

    box-shadow:
        0 5px 18px
        rgba(16, 24, 40, .035) !important;
}


div[data-testid="stMetricLabel"] {

    color:
        #98a2b3 !important;
}


div[data-testid="stMetricValue"] {

    color:
        #172033 !important;

    font-weight:
        800 !important;
}


/* ============================================================
   INPUT
   ============================================================ */

.stSelectbox label,
.stTextInput label {

    color:
        #667085 !important;

    font-size:
        10px !important;

    font-weight:
        700 !important;
}


.stSelectbox > div > div,
.stTextInput > div > div {

    background:
        #ffffff !important;

    border-color:
        #e4e7ec !important;

    border-radius:
        9px !important;

    color:
        #344054 !important;
}


.stSelectbox *,
.stTextInput * {

    color:
        #344054 !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {

    border-radius:
        9px !important;

    font-weight:
        700 !important;

    border:
        1px solid #e4e7ec !important;

    background:
        #ffffff !important;

    color:
        #344054 !important;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {

    border-radius:
        12px !important;

    overflow:
        hidden !important;
}


/* ============================================================
   ALERT
   ============================================================ */

[data-testid="stAlert"] {

    border-radius:
        10px !important;
}


/* ============================================================
   DARK MODE PROTECTION
   ============================================================ */

@media (prefers-color-scheme: dark) {

    .stApp {

        background:
            #f6f7fb !important;

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"] {

        background:
            #ffffff !important;

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"] * {

        color:
            inherit;
    }


    [data-testid="stSidebar"]
    .stButton > button {

        background:
            #ffffff !important;

        color:
            #667085 !important;
    }


    [data-testid="stSidebar"]
    .stButton > button p {

        color:
            #667085 !important;
    }


    .page-title,
    .section-title,
    .card-title,
    .kpi-value {

        color:
            #172033 !important;
    }


    .page-subtitle,
    .section-description,
    .card-subtitle,
    .kpi-label,
    .kpi-description {

        color:
            #8a93a3 !important;
    }


    .dashboard-card,
    .risk-card,
    .kpi,
    .filter-card {

        background:
            #ffffff !important;

        color:
            #344054 !important;
    }


    .stSelectbox > div > div,
    .stTextInput > div > div {

        background:
            #ffffff !important;

        color:
            #344054 !important;
    }
}

</style>
"""
)


# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_data():

    forecast = load_csv(
        FORECAST_DIR,
        "test_forecast.csv"
    )

    evaluation = load_csv(
        EVALUATION_DIR,
        "test_evaluation.csv"
    )

    improvement = load_csv(
        EVALUATION_DIR,
        "model_improvement_comparison.csv"
    )

    optimization = load_csv(
        OPTIMIZATION_DIR,
        "inventory_recommendations.csv"
    )

    segments = load_csv(
        CLUSTERING_DIR,
        "store_item_demand_segments.csv"
    )

    segment_summary = load_csv(
        CLUSTERING_DIR,
        "demand_segment_summary.csv"
    )

    if (
        forecast is not None
        and "date" in forecast.columns
    ):

        forecast["date"] = pd.to_datetime(
            forecast["date"],
            errors="coerce"
        )

    return (
        forecast,
        evaluation,
        improvement,
        optimization,
        segments,
        segment_summary
    )


try:

    (
        forecast,
        evaluation,
        improvement,
        optimization,
        segments,
        segment_summary
    ) = load_data()

except Exception as error:

    st.error(
        "Gagal memuat data ForecastOpti."
    )

    st.exception(error)

    st.stop()


# ============================================================
# VALIDATION
# ============================================================

if forecast is None:

    st.error(
        "outputs/forecasts/test_forecast.csv tidak ditemukan."
    )

    st.stop()


if optimization is None:

    st.error(
        "outputs/optimization/inventory_recommendations.csv tidak ditemukan."
    )

    st.stop()


if segments is None:

    segments = pd.DataFrame()


if segment_summary is None:

    segment_summary = pd.DataFrame()


# ============================================================
# MODEL PERFORMANCE
# ============================================================

if (
    improvement is not None
    and len(improvement) > 1
):

    final_model = improvement.iloc[1]

elif (
    improvement is not None
    and len(improvement) > 0
):

    final_model = improvement.iloc[-1]

else:

    final_model = {}


test_mae = safe_float(
    final_model.get(
        "test_mae",
        0
    )
)

test_rmse = safe_float(
    final_model.get(
        "test_rmse",
        0
    )
)

test_wape = safe_float(
    final_model.get(
        "test_wape",
        0
    )
)

model_name = safe_text(
    final_model.get(
        "model",
        "HistGradientBoosting + Lag Features"
    )
)


# ============================================================
# GLOBAL DATA METRICS
# ============================================================

if "actual_sales" in forecast.columns:

    total_actual = safe_float(
        forecast[
            "actual_sales"
        ].sum()
    )

else:

    total_actual = 0


if "predicted_sales" in forecast.columns:

    total_forecast = safe_float(
        forecast[
            "predicted_sales"
        ].sum()
    )

else:

    total_forecast = 0


if (
    "store_id" in optimization.columns
    and
    "item_id" in optimization.columns
):

    total_store_items = (
        optimization[
            [
                "store_id",
                "item_id"
            ]
        ]
        .drop_duplicates()
        .shape[0]
    )

else:

    total_store_items = 0


if "recommended_stock" in optimization.columns:

    total_recommended_stock = safe_float(
        optimization[
            "recommended_stock"
        ].sum()
    )

else:

    total_recommended_stock = 0


# ============================================================
# NAVIGATION
# ============================================================

PAGES = [

    ("⌂", "Overview"),

    ("↗", "Forecast"),

    ("▣", "Inventory Analysis"),

    ("◈", "Demand Segmentation"),

    ("✓", "Recommendations"),

    ("✦", "AI Analysis"),

    ("◉", "System Health")
]


if "forecastopti_page" not in st.session_state:

    st.session_state.forecastopti_page = "Overview"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html(
        """
<div class="brand">

<div class="brand-name">
ForecastOpti
</div>

<div class="brand-subtitle">
Demand & Inventory Intelligence
</div>

</div>
"""
    )


    html(
        """
<div class="sidebar-label">
Workspace
</div>
"""
    )


    for icon, page_name in PAGES:

        active = (
            st.session_state.forecastopti_page
            == page_name
        )

        if active:

            st.markdown(
                f"""
<div class="nav-active">
""",
                unsafe_allow_html=True
            )

        clicked = st.button(
            f"{icon}   {page_name}",
            key=f"nav_{page_name}",
            width="stretch"
        )

        if active:

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        if clicked:

            st.session_state.forecastopti_page = page_name

            st.rerun()


    st.write("")


    if st.button(
        "Clear cached data",
        key="clear_cache",
        width="stretch"
    ):

        st.cache_data.clear()

        st.rerun()


    html(
        """
<div class="sidebar-footer">

ForecastOpti<br>
Business Intelligence Dashboard<br>
Forecasting · Inventory · Segmentation

</div>
"""
    )


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.forecastopti_page


# ============================================================
# TOP BAR
# ============================================================

html(
    f"""
<div class="topbar">

<div>

<div class="page-title">
{page}
</div>

<div class="page-subtitle">
Forecasting & Inventory Intelligence
</div>

</div>

<div class="status-pill">

<span class="status-dot"></span>

System Online

</div>

</div>
"""
)


# ============================================================
# HERO
# ============================================================

html(
    f"""
<div class="hero">

<div class="hero-label">
BUSINESS INTELLIGENCE
</div>

<div class="hero-title">
{page}
</div>

<div class="hero-description">
Forecast demand, understand demand behavior,
identify inventory risk, and generate
inventory recommendations from one dashboard.
</div>

</div>
"""
)


# ============================================================
# CHART HELPERS
# ============================================================

def chart_layout(
    fig,
    height=320
):

    fig.update_layout(

        height=height,

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Inter, Arial, sans-serif",
            color="#667085",
            size=10
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),

        hoverlabel=dict(
            bgcolor="#172033",
            font_color="#ffffff"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#edf0f4",
        tickfont=dict(
            color="#98a2b3",
            size=9
        )
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#f0f2f5",
        zeroline=False,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(
            color="#98a2b3",
            size=9
        )
    )

    return fig


def forecast_chart(data):

    if data.empty:
        return None

    fig = go.Figure()

    if "actual_sales" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["actual_sales"],
                mode="lines",
                name="Actual",
                line=dict(
                    color="#172033",
                    width=2.4
                ),
                hovertemplate=
                    "<b>Actual</b><br>"
                    "%{y:,.0f}<extra></extra>"
            )
        )

    if "predicted_sales" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["predicted_sales"],
                mode="lines",
                name="Forecast",
                line=dict(
                    color="#2563eb",
                    width=2.8
                ),
                hovertemplate=
                    "<b>Forecast</b><br>"
                    "%{y:,.0f}<extra></extra>"
            )
        )

    return chart_layout(
        fig,
        height=330
    )


def category_chart(
    categories,
    values
):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=[
                    "#172033",
                    "#667085",
                    "#2563eb"
                ][:len(categories)]
            ),
            text=[
                f"{int(v):,}"
                for v in values
            ],
            textposition="outside",
            textfont=dict(
                color="#344054",
                size=10
            ),
            hovertemplate=
                "%{x}<br>"
                "Store-Items: %{y:,}"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        showlegend=False
    )

    return chart_layout(
        fig,
        height=300
    )


def risk_chart(
    high,
    medium,
    low
):

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=[
                "High Risk",
                "Medium Risk",
                "Low Risk"
            ],
            values=[
                high,
                medium,
                low
            ],
            hole=.68,
            sort=False,
            marker=dict(
                colors=[
                    "#df5757",
                    "#e89b25",
                    "#18a66a"
                ],
                line=dict(
                    color="#ffffff",
                    width=4
                )
            ),
            textinfo="percent",
            textfont=dict(
                size=10
            ),
            hovertemplate=
                "%{label}<br>"
                "%{value:,} store-items"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.04,
            x=.5,
            xanchor="center"
        )
    )

    return chart_layout(
        fig,
        height=270
    )


def store_stock_chart(data):

    if data.empty:
        return None

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=data["store_id"].astype(str),
            y=data["recommended_stock"],
            marker_color="#2563eb",
            text=[
                f"{x:,.0f}"
                for x in data["recommended_stock"]
            ],
            textposition="outside",
            hovertemplate=
                "Store %{x}<br>"
                "Recommended Stock: %{y:,.0f}"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        showlegend=False
    )

    return chart_layout(
        fig,
        height=270
    )


# ============================================================
# PAGE: OVERVIEW
# ============================================================

if page == "Overview":

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        html(
            f"""
<div class="kpi kpi-blue">

<div class="kpi-label">
Actual Sales
</div>

<div class="kpi-value">
{integer(total_actual)}
</div>

<div class="kpi-description">
Observed demand in test data
</div>

</div>
"""
        )


    with k2:

        html(
            f"""
<div class="kpi kpi-green">

<div class="kpi-label">
Forecast WAPE
</div>

<div class="kpi-value">
{test_wape:.2f}%
</div>

<div class="kpi-description">
Final model performance
</div>

</div>
"""
        )


    with k3:

        html(
            f"""
<div class="kpi kpi-orange">

<div class="kpi-label">
Recommended Stock
</div>

<div class="kpi-value">
{integer(total_recommended_stock)}
</div>

<div class="kpi-description">
Aggregated inventory recommendation
</div>

</div>
"""
        )


    with k4:

        html(
            f"""
<div class="kpi kpi-red">

<div class="kpi-label">
Store-Items
</div>

<div class="kpi-value">
{total_store_items:,}
</div>

<div class="kpi-description">
Unique store-item combinations
</div>

</div>
"""
        )


    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Demand Overview
</div>

<div class="section-description">
Actual demand compared with model forecast.
</div>

</div>

</div>
"""
    )


    filter_a, filter_b, filter_c = st.columns(
        [1, 1, 1]
    )


    stores = ["All"]

    if "store_id" in forecast.columns:

        stores += sorted(
            forecast[
                "store_id"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


    items = ["All"]

    if "item_id" in forecast.columns:

        items += sorted(
            forecast[
                "item_id"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


    selected_store = filter_a.selectbox(
        "Store",
        stores,
        key="overview_store"
    )


    selected_item = filter_b.selectbox(
        "Item",
        items,
        key="overview_item"
    )


    period = filter_c.selectbox(
        "Period",
        [
            "All",
            "Last 30 Days",
            "Last 60 Days",
            "Last 90 Days"
        ],
        key="overview_period"
    )


    overview_data = forecast.copy()


    if selected_store != "All":

        overview_data = overview_data[
            overview_data[
                "store_id"
            ]
            .astype(str)
            ==
            selected_store
        ]


    if selected_item != "All":

        overview_data = overview_data[
            overview_data[
                "item_id"
            ]
            .astype(str)
            ==
            selected_item
        ]


    if (
        period != "All"
        and
        "date" in overview_data.columns
        and
        not overview_data.empty
    ):

        days = {

            "Last 30 Days": 30,

            "Last 60 Days": 60,

            "Last 90 Days": 90

        }[period]


        max_date = overview_data[
            "date"
        ].max()


        min_date = (
            max_date
            -
            pd.Timedelta(
                days=days
            )
        )


        overview_data = overview_data[
            overview_data["date"]
            >= min_date
        ]


    # --------------------------------------------------------
    # MAIN CHARTS
    # --------------------------------------------------------

    left, right = st.columns(
        [1.65, 1]
    )


    with left:

        html(
            """
<div class="dashboard-card">

<div class="card-title">
Demand Forecast
</div>

<div class="card-subtitle">
Actual vs forecast demand over time
</div>

</div>
"""
        )


        if (
            not overview_data.empty
            and
            "date" in overview_data.columns
            and
            "actual_sales" in overview_data.columns
            and
            "predicted_sales" in overview_data.columns
        ):

            daily = (
                overview_data
                .groupby("date")[
                    [
                        "actual_sales",
                        "predicted_sales"
                    ]
                ]
                .sum()
                .reset_index()
                .sort_values("date")
            )


            fig = forecast_chart(
                daily
            )


            if fig is not None:

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    }
                )

        else:

            st.info(
                "Data forecast tidak tersedia."
            )


    with right:

        html(
            """
<div class="dashboard-card">

<div class="card-title">
Demand Segmentation
</div>

<div class="card-subtitle">
Store-item distribution by business level
</div>

</div>
"""
        )


        if (
            not segment_summary.empty
            and
            "business_level"
            in segment_summary.columns
            and
            "store_item_count"
            in segment_summary.columns
        ):

            segment_chart_data = (
                segment_summary
                .copy()
            )


            fig = category_chart(
                segment_chart_data[
                    "business_level"
                ].astype(str).tolist(),
                segment_chart_data[
                    "store_item_count"
                ].tolist()
            )


            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                }
            )

        else:

            st.info(
                "Data segmentation belum tersedia."
            )


    # --------------------------------------------------------
    # RISK + STOCK
    # --------------------------------------------------------

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Inventory Intelligence
</div>

<div class="section-description">
Risk indicators and recommended stock distribution.
</div>

</div>

</div>
"""
    )


    risk_col, stock_col = st.columns(
        [1, 1.6]
    )


    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    with risk_col:

        rec = optimization.copy()


        if "demand_category" in rec.columns:

            category = (
                rec[
                    "demand_category"
                ]
                .astype(str)
                .str.lower()
                .str.strip()
            )


            high_count = int(
                category.isin(
                    [
                        "high",
                        "tinggi"
                    ]
                ).sum()
            )


            medium_count = int(
                category.isin(
                    [
                        "medium",
                        "sedang"
                    ]
                ).sum()
            )


            low_count = int(
                category.isin(
                    [
                        "low",
                        "rendah"
                    ]
                ).sum()
            )

        else:

            high_count = 0
            medium_count = 0
            low_count = 0


        html(
            """
<div class="risk-card">

<div class="card-title">
Stockout Risk Indicators
</div>

<div class="card-subtitle">
Current demand priority distribution
</div>

</div>
"""
        )


        fig = risk_chart(
            high_count,
            medium_count,
            low_count
        )


        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


        html(
            f"""
<div class="risk-card">

<div class="risk-item">

<div class="risk-row">

<div class="risk-name">
High Risk SKUs
</div>

<div class="risk-number">
{high_count:,}
</div>

</div>

<span class="risk-badge risk-high">
Priority Attention
</span>

</div>


<div class="risk-item">

<div class="risk-row">

<div class="risk-name">
Medium Risk SKUs
</div>

<div class="risk-number">
{medium_count:,}
</div>

</div>

<span class="risk-badge risk-medium">
Monitor
</span>

</div>


<div class="risk-item">

<div class="risk-row">

<div class="risk-name">
Low Risk SKUs
</div>

<div class="risk-number">
{low_count:,}
</div>

</div>

<span class="risk-badge risk-low">
Stable
</span>

</div>

</div>
"""
        )


    # --------------------------------------------------------
    # STOCK
    # --------------------------------------------------------

    with stock_col:

        html(
            """
<div class="dashboard-card">

<div class="card-title">
Recommended Stock by Store
</div>

<div class="card-subtitle">
Aggregated recommended inventory level
</div>

</div>
"""
        )


        if (
            "store_id" in optimization.columns
            and
            "recommended_stock"
            in optimization.columns
        ):

            store_stock = (
                optimization
                .groupby(
                    "store_id",
                    as_index=False
                )[
                    "recommended_stock"
                ]
                .sum()
                .sort_values(
                    "recommended_stock",
                    ascending=False
                )
                .head(8)
            )


            fig = store_stock_chart(
                store_stock
            )


            if fig is not None:

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    }
                )


        else:

            st.info(
                "Data recommended stock belum tersedia."
            )


    # --------------------------------------------------------
    # MODEL SNAPSHOT
    # --------------------------------------------------------

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Model Performance
</div>

<div class="section-description">
Final model compared with the baseline.
</div>

</div>

</div>
"""
    )


    m1, m2, m3, m4 = st.columns(4)


    m1.metric(
        "MAE",
        f"{test_mae:.2f}"
    )


    m2.metric(
        "RMSE",
        f"{test_rmse:.2f}"
    )


    m3.metric(
        "WAPE",
        f"{test_wape:.2f}%"
    )


    if (
        improvement is not None
        and len(improvement) > 1
    ):

        mae_improvement = safe_float(
            improvement.iloc[1].get(
                "mae_improvement_pct",
                0
            )
        )

    else:

        mae_improvement = 0


    m4.metric(
        "MAE Improvement",
        f"{mae_improvement:.2f}%"
    )


# ============================================================
# PAGE: FORECAST
# ============================================================

elif page == "Forecast":

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Forecast Analysis
</div>

<div class="section-description">
Compare actual demand with model prediction.
</div>

</div>

</div>
"""
    )


    if (
        "store_id" not in forecast.columns
        or
        "item_id" not in forecast.columns
    ):

        st.error(
            "store_id atau item_id tidak ditemukan."
        )

        st.stop()


    stores = sorted(
        forecast[
            "store_id"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    items = sorted(
        forecast[
            "item_id"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    f1, f2 = st.columns(2)


    selected_store = f1.selectbox(
        "Store",
        ["All"] + stores,
        key="forecast_store"
    )


    selected_item = f2.selectbox(
        "Item",
        ["All"] + items,
        key="forecast_item"
    )


    filtered = forecast.copy()


    if selected_store != "All":

        filtered = filtered[
            filtered[
                "store_id"
            ]
            .astype(str)
            ==
            selected_store
        ]


    if selected_item != "All":

        filtered = filtered[
            filtered[
                "item_id"
            ]
            .astype(str)
            ==
            selected_item
        ]


    if filtered.empty:

        st.warning(
            "Tidak ada data untuk filter."
        )

    else:

        if (
            "actual_sales"
            in filtered.columns
            and
            "predicted_sales"
            in filtered.columns
        ):

            actual = safe_float(
                filtered[
                    "actual_sales"
                ].sum()
            )


            predicted = safe_float(
                filtered[
                    "predicted_sales"
                ].sum()
            )


            error = actual - predicted


            a, b, c = st.columns(3)


            a.metric(
                "Actual Demand",
                integer(actual)
            )


            b.metric(
                "Forecast Demand",
                integer(predicted)
            )


            c.metric(
                "Forecast Error",
                number(error)
            )


            if "date" in filtered.columns:

                daily = (
                    filtered
                    .groupby("date")[
                        [
                            "actual_sales",
                            "predicted_sales"
                        ]
                    ]
                    .sum()
                    .reset_index()
                    .sort_values("date")
                )


                fig = forecast_chart(
                    daily
                )


                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={
                        "displayModeBar": False
                    }
                )


        html(
            """
<div class="section-head">

<div>

<div class="section-title">
Forecast Output
</div>

<div class="section-description">
Detailed prediction records.
</div>

</div>

</div>
"""
        )


        display_dataframe(
            filtered.sort_values(
                "date",
                ascending=False
            )
            if "date" in filtered.columns
            else filtered,
            height=520
        )


# ============================================================
# PAGE: INVENTORY ANALYSIS
# ============================================================

elif page == "Inventory Analysis":

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Inventory Analysis
</div>

<div class="section-description">
Explore demand characteristics and inventory recommendations
by store-item.
</div>

</div>

</div>
"""
    )


    if segments.empty:

        st.warning(
            "Data segmentation belum tersedia."
        )

        st.stop()


    if (
        "store_id" not in segments.columns
        or
        "item_id" not in segments.columns
    ):

        st.error(
            "Kolom store_id atau item_id tidak ditemukan."
        )

        st.stop()


    stores = sorted(
        segments[
            "store_id"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_store = st.selectbox(
        "Store",
        stores,
        key="analysis_store"
    )


    available_items = sorted(
        segments.loc[
            segments[
                "store_id"
            ]
            .astype(str)
            ==
            selected_store,
            "item_id"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_item = st.selectbox(
        "Item",
        available_items,
        key="analysis_item"
    )


    selected_seg = segments[
        (
            segments[
                "store_id"
            ]
            .astype(str)
            ==
            selected_store
        )
        &
        (
            segments[
                "item_id"
            ]
            .astype(str)
            ==
            selected_item
        )
    ]


    selected_inv = optimization[
        (
            optimization[
                "store_id"
            ]
            .astype(str)
            ==
            selected_store
        )
        &
        (
            optimization[
                "item_id"
            ]
            .astype(str)
            ==
            selected_item
        )
    ]


    if selected_seg.empty:

        st.warning(
            "Data segmentation tidak ditemukan."
        )

        st.stop()


    if selected_inv.empty:

        st.warning(
            "Data inventory recommendation tidak ditemukan."
        )

        st.stop()


    seg = selected_seg.iloc[0]

    inv = selected_inv.iloc[0]


    html(
        f"""
<div class="dashboard-card">

<div class="card-title">
Store {selected_store}
</div>

<div class="card-subtitle">
Item {selected_item}
</div>

</div>
"""
    )


    k1, k2, k3, k4 = st.columns(4)


    k1.metric(
        "Avg Forecast",
        number(
            inv.get(
                "avg_forecast_demand",
                0
            )
        )
    )


    k2.metric(
        "Demand Std",
        number(
            inv.get(
                "demand_std",
                0
            )
        )
    )


    k3.metric(
        "Demand Buffer",
        number(
            inv.get(
                "demand_buffer",
                0
            )
        )
    )


    k4.metric(
        "Recommended Stock",
        integer(
            inv.get(
                "recommended_stock",
                0
            )
        )
    )


    left, right = st.columns(2)


    with left:

        html(
            """
<div class="section-head">

<div>

<div class="section-title">
Demand Profile
</div>

</div>

</div>
"""
        )


        detail = pd.DataFrame(
            {
                "Metric": [

                    "Cluster",

                    "Demand Segment",

                    "Average Demand",

                    "Demand Variability",

                    "Coefficient of Variation",

                    "Forecast Error",

                    "Absolute Forecast Error",

                    "Forecast Demand"

                ],

                "Value": [

                    safe_text(
                        seg.get(
                            "cluster_k3",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "demand_segment",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "average_demand",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "demand_variability",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "coefficient_of_variation",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "forecast_error",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "absolute_forecast_error",
                            "-"
                        )
                    ),

                    safe_text(
                        seg.get(
                            "forecast_demand",
                            "-"
                        )
                    )

                ]
            }
        )


        display_dataframe(
            detail
        )


    with right:

        category = safe_text(
            inv.get(
                "demand_category",
                "Medium"
            ),
            "Medium"
        )


        category_lower = (
            category
            .lower()
            .strip()
        )


        if category_lower in [
            "high",
            "tinggi"
        ]:

            badge_class = "risk-high"

            message = (
                "Store-item membutuhkan perhatian "
                "lebih tinggi dalam inventory planning."
            )

        elif category_lower in [
            "medium",
            "sedang"
        ]:

            badge_class = "risk-medium"

            message = (
                "Store-item perlu dimonitor secara "
                "berkala berdasarkan perubahan demand."
            )

        else:

            badge_class = "risk-low"

            message = (
                "Store-item berada pada kategori "
                "demand yang relatif rendah."
            )


        html(
            f"""
<div class="risk-card">

<div class="card-title">
Inventory Recommendation
</div>

<div class="card-subtitle">
Decision support for selected store-item
</div>

<span class="risk-badge {badge_class}">
{category}
</span>

<div style="
font-size:28px;
font-weight:800;
color:#172033;
margin-top:15px;
">

{integer(
    inv.get(
        "recommended_stock",
        0
    )
)}

</div>

<div style="
font-size:10px;
color:#98a2b3;
">

recommended units

</div>

<hr>

<p style="
color:#667085;
font-size:11px;
line-height:1.7;
">

{message}

</p>

</div>
"""
        )


# ============================================================
# PAGE: DEMAND SEGMENTATION
# ============================================================

elif page == "Demand Segmentation":

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Demand Segmentation
</div>

<div class="section-description">
Understand how store-items are distributed
across demand characteristics.
</div>

</div>

</div>
"""
    )


    if segment_summary.empty:

        st.warning(
            "Demand segment summary belum tersedia."
        )

        st.stop()


    if (
        "business_level"
        not in segment_summary.columns
        or
        "store_item_count"
        not in segment_summary.columns
    ):

        st.error(
            "Kolom segment summary tidak lengkap."
        )

        st.stop()


    summary = segment_summary.copy()


    total = safe_int(
        summary[
            "store_item_count"
        ].sum()
    )


    labels = (
        summary[
            "business_level"
        ]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    high = safe_int(
        summary.loc[
            labels.isin(
                [
                    "high",
                    "tinggi"
                ]
            ),
            "store_item_count"
        ].sum()
    )


    medium = safe_int(
        summary.loc[
            labels.isin(
                [
                    "medium",
                    "sedang"
                ]
            ),
            "store_item_count"
        ].sum()
    )


    low = safe_int(
        summary.loc[
            labels.isin(
                [
                    "low",
                    "rendah"
                ]
            ),
            "store_item_count"
        ].sum()
    )


    a, b, c, d = st.columns(4)


    a.metric(
        "Total",
        f"{total:,}"
    )


    b.metric(
        "High",
        f"{high:,}"
    )


    c.metric(
        "Medium",
        f"{medium:,}"
    )


    d.metric(
        "Low",
        f"{low:,}"
    )


    left, right = st.columns(
        [1, 1.5]
    )


    with left:

        fig = category_chart(
            summary[
                "business_level"
            ].astype(str).tolist(),
            summary[
                "store_item_count"
            ].tolist()
        )


        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


    with right:

        display_dataframe(
            summary
        )


    if not segments.empty:

        html(
            """
<div class="section-head">

<div>

<div class="section-title">
Store-Item Detail
</div>

</div>

</div>
"""
        )


        search = st.text_input(
            "Search store / item",
            key="segment_search"
        )


        detail = segments.copy()


        if search:

            mask = (

                detail[
                    "store_id"
                ]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )

                |

                detail[
                    "item_id"
                ]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )

            )


            detail = detail[
                mask
            ]


        display_dataframe(
            detail,
            height=520
        )


# ============================================================
# PAGE: RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Inventory Recommendations
</div>

<div class="section-description">
Prioritize store-items based on demand and
recommended inventory level.
</div>

</div>

</div>
"""
    )


    rec = optimization.copy()


    search = st.text_input(
        "Search store / item",
        key="recommendation_search"
    )


    f1, f2, f3 = st.columns(3)


    categories = ["All"]

    if "demand_category" in rec.columns:

        categories += sorted(
            rec[
                "demand_category"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


    priority = f1.selectbox(
        "Demand Category",
        categories,
        key="recommendation_priority"
    )


    sort_by = f2.selectbox(
        "Sort By",
        [
            "Recommended Stock",
            "Forecast Demand",
            "Demand Variability",
            "Demand Buffer"
        ],
        key="recommendation_sort"
    )


    direction = f3.selectbox(
        "Order",
        [
            "Highest First",
            "Lowest First"
        ],
        key="recommendation_direction"
    )


    if search:

        mask = (

            rec[
                "store_id"
            ]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )

            |

            rec[
                "item_id"
            ]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )

        )


        rec = rec[
            mask
        ]


    if (
        priority != "All"
        and
        "demand_category"
        in rec.columns
    ):

        rec = rec[
            rec[
                "demand_category"
            ]
            .astype(str)
            ==
            priority
        ]


    sort_map = {

        "Recommended Stock":
            "recommended_stock",

        "Forecast Demand":
            "avg_forecast_demand",

        "Demand Variability":
            "demand_std",

        "Demand Buffer":
            "demand_buffer"

    }


    sort_column = sort_map[
        sort_by
    ]


    if sort_column in rec.columns:

        rec = rec.sort_values(
            sort_column,
            ascending=(
                direction
                == "Lowest First"
            )
        )


    if "demand_category" in rec.columns:

        category = (
            rec[
                "demand_category"
            ]
            .astype(str)
            .str.lower()
            .str.strip()
        )


        high = int(
            category.isin(
                [
                    "high",
                    "tinggi"
                ]
            ).sum()
        )


        medium = int(
            category.isin(
                [
                    "medium",
                    "sedang"
                ]
            ).sum()
        )


        low = int(
            category.isin(
                [
                    "low",
                    "rendah"
                ]
            ).sum()
        )

    else:

        high = 0
        medium = 0
        low = 0


    a, b, c, d = st.columns(4)


    a.metric(
        "High",
        f"{high:,}"
    )


    b.metric(
        "Medium",
        f"{medium:,}"
    )


    c.metric(
        "Low",
        f"{low:,}"
    )


    d.metric(
        "Filtered",
        f"{len(rec):,}"
    )


    columns = [

        "store_id",

        "item_id",

        "demand_category",

        "avg_forecast_demand",

        "max_forecast_demand",

        "demand_std",

        "demand_buffer",

        "recommended_stock"

    ]


    columns = [
        column
        for column in columns
        if column in rec.columns
    ]


    if rec.empty:

        st.info(
            "Tidak ada recommendation yang cocok."
        )

    else:

        display_dataframe(
            rec[
                columns
            ],
            height=560
        )


# ============================================================
# PAGE: AI ANALYSIS
# ============================================================

elif page == "AI Analysis":

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
AI / Business Analysis
</div>

<div class="section-description">
Business interpretation based on forecasting
and inventory outputs.
</div>

</div>

</div>
"""
    )


    avg_demand = safe_float(
        optimization[
            "avg_forecast_demand"
        ].mean()
        if "avg_forecast_demand"
        in optimization.columns
        else 0
    )


    avg_variability = safe_float(
        optimization[
            "demand_std"
        ].mean()
        if "demand_std"
        in optimization.columns
        else 0
    )


    avg_stock = safe_float(
        optimization[
            "recommended_stock"
        ].mean()
        if "recommended_stock"
        in optimization.columns
        else 0
    )


    abs_error = safe_float(
        segments[
            "absolute_forecast_error"
        ].mean()
        if (
            not segments.empty
            and
            "absolute_forecast_error"
            in segments.columns
        )
        else 0
    )


    a, b, c, d = st.columns(4)


    a.metric(
        "Store-Items",
        f"{total_store_items:,}"
    )


    b.metric(
        "Average Demand",
        number(avg_demand)
    )


    c.metric(
        "Demand Variability",
        number(avg_variability)
    )


    d.metric(
        "Recommended Stock",
        number(avg_stock)
    )


    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Business Insights
</div>

<div class="section-description">
Automatically generated interpretation from project outputs.
</div>

</div>

</div>
"""
    )


    insights = []


    if avg_demand >= 30:

        insights.append(
            "Average forecast demand is relatively high."
        )

    elif avg_demand >= 20:

        insights.append(
            "Average forecast demand is at a moderate level."
        )

    else:

        insights.append(
            "Average forecast demand is relatively low."
        )


    if avg_variability > 10:

        insights.append(
            "Demand variability is relatively high and "
            "should be considered when planning inventory."
        )

    else:

        insights.append(
            "Demand variability appears relatively controlled."
        )


    if abs_error > 10:

        insights.append(
            "Absolute forecast error should be monitored "
            "because it can influence inventory planning."
        )

    else:

        insights.append(
            "Absolute forecast error is relatively controlled."
        )


    insights.append(
        f"Average recommended inventory is approximately "
        f"{avg_stock:.0f} units per store-item."
    )


    for insight in insights:

        html(
            f"""
<div class="dashboard-card">

<div style="
color:#344054;
font-size:12px;
line-height:1.7;
">

{insight}

</div>

</div>
"""
        )


    if not segment_summary.empty:

        html(
            """
<div class="section-head">

<div>

<div class="section-title">
Segment Business View
</div>

</div>

</div>
"""
        )


        display_dataframe(
            segment_summary
        )


# ============================================================
# PAGE: SYSTEM HEALTH
# ============================================================

elif page == "System Health":

    html(
        """
<div class="section-head">

<div>

<div class="section-title">
System Health
</div>

<div class="section-description">
Check ForecastOpti pipeline outputs and dataset availability.
</div>

</div>

</div>
"""
    )


    checks = [

        (
            "Forecast",
            FORECAST_DIR /
            "test_forecast.csv"
        ),

        (
            "Evaluation",
            EVALUATION_DIR /
            "test_evaluation.csv"
        ),

        (
            "Optimization",
            OPTIMIZATION_DIR /
            "inventory_recommendations.csv"
        ),

        (
            "Segmentation",
            CLUSTERING_DIR /
            "store_item_demand_segments.csv"
        )

    ]


    for name, path in checks:

        if path.exists():

            html(
                f"""
<div class="dashboard-card">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<div>

<div style="
font-size:12px;
font-weight:800;
color:#172033;
">

{name}

</div>

<div style="
font-size:9px;
color:#98a2b3;
margin-top:3px;
">

{path.name}

</div>

</div>

<div class="risk-badge risk-low">
Healthy
</div>

</div>

</div>
"""
            )

        else:

            html(
                f"""
<div class="dashboard-card">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<div style="
font-size:12px;
font-weight:800;
color:#172033;
">

{name}

</div>

<div class="risk-badge risk-high">
Missing
</div>

</div>

</div>
"""
            )


    a, b, c = st.columns(3)


    a.metric(
        "Forecast Rows",
        f"{len(forecast):,}"
    )


    b.metric(
        "Optimization Rows",
        f"{len(optimization):,}"
    )


    c.metric(
        "Clustering Rows",
        f"{len(segments):,}"
    )


    html(
        """
<div class="section-head">

<div>

<div class="section-title">
Project Configuration
</div>

</div>

</div>
"""
    )


    st.code(
        f"""
Project:
{PROJECT_DIR}

Forecast:
{FORECAST_DIR}

Evaluation:
{EVALUATION_DIR}

Optimization:
{OPTIMIZATION_DIR}

Clustering:
{CLUSTERING_DIR}
""",
        language="text"
    )