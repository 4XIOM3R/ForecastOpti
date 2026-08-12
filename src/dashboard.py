import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PATH
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

FORECAST_DIR = ROOT / "outputs" / "forecasts"
EVALUATION_DIR = ROOT / "outputs" / "evaluation"
OPTIMIZATION_DIR = ROOT / "outputs" / "optimization"
CLUSTERING_DIR = ROOT / "outputs" / "clustering"


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ForecastOpti",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    color-scheme: light !important;
}

.stApp {
    background: #f5f6f8 !important;
    color: #111827 !important;
}

.block-container {
    max-width: 1500px !important;
    padding: 28px 34px 50px 34px !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: #ffffff !important;
    padding: 22px 14px !important;
}

.brand {
    padding: 4px 10px 28px 10px;
}

.brand-title {
    color: #111827 !important;
    font-size: 21px !important;
    font-weight: 800 !important;
    letter-spacing: -0.04em !important;
}

.brand-text {
    color: #6b7280 !important;
    font-size: 10px !important;
    margin-top: 5px !important;
}

.sidebar-title {
    color: #9ca3af !important;
    font-size: 9px !important;
    font-weight: 800 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    padding: 0 10px 7px 10px !important;
}


/* NAV */

[data-testid="stSidebar"] .stButton {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    min-height: 40px !important;
    margin: 2px 0 !important;
    padding: 8px 11px !important;

    background: #ffffff !important;
    border: 1px solid transparent !important;
    border-radius: 9px !important;

    color: #374151 !important;
    text-align: left !important;

    font-size: 12px !important;
    font-weight: 600 !important;

    box-shadow: none !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #f3f4f6 !important;
    color: #111827 !important;
    border-color: #e5e7eb !important;
}

[data-testid="stSidebar"] .stButton > button p {
    color: #374151 !important;
    font-size: 12px !important;
}


/* ACTIVE NAV */

.nav-active {
    background: #f0f2f5 !important;
    border-left: 3px solid #111827 !important;
    border-radius: 9px !important;
}

.nav-active + div .stButton > button {
    color: #111827 !important;
    font-weight: 800 !important;
}


/* SIDEBAR FOOTER */

.sidebar-footer {
    border-top: 1px solid #e5e7eb;
    margin-top: 24px;
    padding: 16px 10px;

    color: #9ca3af !important;
    font-size: 9px;
    line-height: 1.7;
}


/* HEADER */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;

    margin-bottom: 25px;
}

.page-title {
    color: #111827 !important;
    font-size: 30px !important;
    font-weight: 850 !important;
    line-height: 1.1 !important;
    letter-spacing: -0.04em !important;
}

.page-subtitle {
    color: #6b7280 !important;
    font-size: 11px !important;
    margin-top: 7px !important;
}

.system-status {
    display: inline-flex;
    align-items: center;

    padding: 7px 11px;

    border-radius: 999px;
    border: 1px solid #d1d5db;

    background: #ffffff;

    color: #374151 !important;

    font-size: 9px;
    font-weight: 700;
}


/* KPI */

.kpi {
    background: #ffffff;

    border: 1px solid #e5e7eb;
    border-radius: 14px;

    padding: 17px 18px;

    min-height: 112px;

    box-shadow:
        0 3px 12px rgba(17, 24, 39, 0.035);
}

.kpi-label {
    color: #6b7280 !important;
    font-size: 10px !important;
    font-weight: 600 !important;
}

.kpi-value {
    color: #111827 !important;
    font-size: 27px !important;
    font-weight: 850 !important;
    letter-spacing: -0.04em !important;
    margin-top: 8px !important;
}

.kpi-description {
    color: #9ca3af !important;
    font-size: 9px !important;
    margin-top: 4px !important;
}

.kpi-black {
    border-top: 3px solid #111827;
}

.kpi-blue {
    border-top: 3px solid #2563eb;
}

.kpi-green {
    border-top: 3px solid #16a34a;
}

.kpi-orange {
    border-top: 3px solid #d97706;
}


/* SECTION */

.section {
    margin-top: 28px;
    margin-bottom: 12px;
}

.section-title {
    color: #111827 !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    letter-spacing: -0.025em !important;
}

.section-description {
    color: #6b7280 !important;
    font-size: 10px !important;
    margin-top: 4px !important;
}


/* CARD */

.card {
    background: #ffffff;

    border: 1px solid #e5e7eb;
    border-radius: 15px;

    padding: 18px;

    box-shadow:
        0 3px 14px rgba(17, 24, 39, 0.035);
}

.card-title {
    color: #111827 !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

.card-description {
    color: #6b7280 !important;
    font-size: 9px !important;
    margin-top: 4px !important;
}


/* SEGMENT CARDS */

.segment-card {
    background: #ffffff;

    border: 1px solid #e5e7eb;
    border-radius: 12px;

    padding: 14px 15px;

    min-height: 105px;
}

.segment-name {
    color: #6b7280 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
}

.segment-value {
    color: #111827 !important;
    font-size: 24px !important;
    font-weight: 850 !important;

    margin-top: 8px;
}

.segment-percent {
    color: #6b7280 !important;
    font-size: 9px !important;
    margin-top: 2px !important;
}


/* INSIGHT */

.insight {
    background: #f8f9fb;

    border: 1px solid #e5e7eb;
    border-left: 3px solid #111827;

    border-radius: 10px;

    padding: 13px 15px;

    margin-top: 12px;
}

.insight-title {
    color: #111827 !important;
    font-size: 10px !important;
    font-weight: 800 !important;
}

.insight-text {
    color: #4b5563 !important;
    font-size: 10px !important;
    line-height: 1.6 !important;
    margin-top: 4px !important;
}


/* METRIC */

div[data-testid="stMetric"] {
    background: #ffffff !important;

    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;

    padding: 14px !important;

    box-shadow:
        0 3px 12px rgba(17, 24, 39, 0.035) !important;
}

div[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
}

div[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 800 !important;
}


/* INPUT */

.stSelectbox label,
.stTextInput label {
    color: #374151 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
}

.stSelectbox > div > div,
.stTextInput > div > div {
    background: #ffffff !important;
    color: #111827 !important;
    border-color: #d1d5db !important;
    border-radius: 9px !important;
}

.stSelectbox *,
.stTextInput * {
    color: #111827 !important;
}


/* BUTTON */

.stButton > button {
    background: #ffffff !important;
    color: #111827 !important;

    border: 1px solid #d1d5db !important;
    border-radius: 9px !important;

    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #f3f4f6 !important;
    border-color: #9ca3af !important;
}


/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}


/* ALERT */

[data-testid="stAlert"] {
    border-radius: 10px !important;
}


/* DARK MODE OVERRIDE */

@media (prefers-color-scheme: dark) {

    .stApp {
        background: #f5f6f8 !important;
        color: #111827 !important;
    }

    [data-testid="stSidebar"] {
        background: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: #ffffff !important;
        color: #374151 !important;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #374151 !important;
    }

    .page-title,
    .section-title,
    .card-title,
    .kpi-value,
    .segment-value,
    .insight-title {
        color: #111827 !important;
    }

    .page-subtitle,
    .section-description,
    .card-description,
    .kpi-label,
    .kpi-description,
    .segment-name,
    .segment-percent,
    .insight-text {
        color: #6b7280 !important;
    }

    .card,
    .kpi,
    .segment-card,
    .insight,
    div[data-testid="stMetric"] {
        background: #ffffff !important;
    }

    .stSelectbox > div > div,
    .stTextInput > div > div {
        background: #ffffff !important;
        color: #111827 !important;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def load_csv(folder, filename):

    path = folder / filename

    if not path.exists():
        return None

    try:
        return pd.read_csv(path)
    except Exception:
        return None


def fmt_number(value):

    try:
        return f"{float(value):,.0f}"
    except Exception:
        return "0"


def fmt_decimal(value):

    try:
        return f"{float(value):,.2f}"
    except Exception:
        return "0.00"


def fmt_percent(value):

    try:
        return f"{float(value):.1f}%"
    except Exception:
        return "0.0%"


def show_card(title, description=""):

    st.markdown(
        f"""
<div class="card">

<div class="card-title">
{title}
</div>

<div class="card-description">
{description}
</div>

</div>
""",
        unsafe_allow_html=True
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


(
    forecast,
    evaluation,
    improvement,
    optimization,
    segments,
    segment_summary
) = load_data()


if forecast is None:

    st.error(
        "Forecast data tidak ditemukan."
    )

    st.stop()


if optimization is None:

    st.error(
        "Inventory recommendation data tidak ditemukan."
    )

    st.stop()


if segments is None:
    segments = pd.DataFrame()


if segment_summary is None:
    segment_summary = pd.DataFrame()


# ============================================================
# MODEL
# ============================================================

if (
    improvement is not None
    and len(improvement) > 0
):

    if len(improvement) > 1:
        model = improvement.iloc[1]
    else:
        model = improvement.iloc[0]

else:

    model = {}


mae = float(
    model.get(
        "test_mae",
        0
    )
)


rmse = float(
    model.get(
        "test_rmse",
        0
    )
)


wape = float(
    model.get(
        "test_wape",
        0
    )
)


mae_improvement = float(
    model.get(
        "mae_improvement_pct",
        0
    )
)


# ============================================================
# KPI
# ============================================================

if "actual_sales" in forecast.columns:

    actual_total = forecast[
        "actual_sales"
    ].sum()

else:

    actual_total = 0


if "predicted_sales" in forecast.columns:

    forecast_total = forecast[
        "predicted_sales"
    ].sum()

else:

    forecast_total = 0


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

    recommended_stock = optimization[
        "recommended_stock"
    ].sum()

else:

    recommended_stock = 0


# ============================================================
# NAV
# ============================================================

PAGES = [
    "Overview",
    "Forecast",
    "Inventory Analysis",
    "Demand Segmentation",
    "Recommendations",
    "AI Analysis",
    "System Health",
]


if "page" not in st.session_state:

    st.session_state.page = "Overview"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
<div class="brand">

<div class="brand-title">
ForecastOpti
</div>

<div class="brand-text">
Demand and Inventory Intelligence
</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="sidebar-title">
Workspace
</div>
""",
        unsafe_allow_html=True
    )

    for item in PAGES:

        active = (
            st.session_state.page
            == item
        )

        if active:

            st.markdown(
                '<div class="nav-active">',
                unsafe_allow_html=True
            )

        clicked = st.button(
            item,
            key=f"nav_{item}",
            use_container_width=True
        )

        if active:

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        if clicked:

            st.session_state.page = item

            st.rerun()


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    if st.button(
        "Clear cached data",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


    st.markdown(
        """
<div class="sidebar-footer">

ForecastOpti<br>
Forecasting - Inventory - Segmentation

</div>
""",
        unsafe_allow_html=True
    )


page = st.session_state.page


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
<div class="top-header">

<div>

<div class="page-title">
{page}
</div>

<div class="page-subtitle">
Forecasting and inventory decision support
</div>

</div>

<div class="system-status">
System Online
</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# CHART
# ============================================================

def base_layout(fig, height=330):

    fig.update_layout(

        height=height,

        margin=dict(
            l=15,
            r=15,
            t=35,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial, sans-serif",
            color="#111827",
            size=10
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            font_color="#ffffff"
        )
    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False,

        linecolor="#e5e7eb",

        tickfont=dict(
            color="#6b7280",
            size=9
        )
    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#eef0f3",

        zeroline=False,

        showline=False,

        tickfont=dict(
            color="#6b7280",
            size=9
        )
    )

    return fig


def forecast_chart(data):

    fig = go.Figure()


    if "actual_sales" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["actual_sales"],
                mode="lines",
                name="Actual",
                line=dict(
                    color="#111827",
                    width=2.5
                ),
                hovertemplate=
                    "Actual: %{y:,.0f}<extra></extra>"
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
                    width=2.5
                ),
                hovertemplate=
                    "Forecast: %{y:,.0f}<extra></extra>"
            )
        )


    fig.update_layout(

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        )

    )

    return base_layout(
        fig,
        350
    )


def segmentation_chart(summary):

    labels = (
        summary["business_level"]
        .astype(str)
        .str.strip()
    )


    values = summary[
        "store_item_count"
    ].astype(float)


    total = values.sum()


    percentages = (
        values / total * 100
        if total > 0
        else values * 0
    )


    colors = []

    for label in labels:

        text = label.lower()

        if text in ["rendah", "low"]:

            colors.append("#d1d5db")

        elif text in ["sedang", "medium"]:

            colors.append("#111827")

        else:

            colors.append("#4b5563")


    fig = go.Figure()


    fig.add_trace(
        go.Bar(

            x=labels,

            y=values,

            marker=dict(
                color=colors,
                line=dict(
                    width=0
                )
            ),

            text=[
                f"{int(v):,}"
                for v in values
            ],

            textposition="outside",

            textfont=dict(
                color="#111827",
                size=11
            ),

            customdata=[
                f"{p:.1f}%"
                for p in percentages
            ],

            hovertemplate=
                "<b>%{x}</b><br>"
                "Store-items: %{y:,}<br>"
                "Share: %{customdata}"
                "<extra></extra>"
        )
    )


    fig.update_layout(

        showlegend=False,

        bargap=0.42,

        yaxis=dict(
            title="Store-items"
        )

    )


    fig.update_traces(
        marker_line_width=0
    )


    return base_layout(
        fig,
        310
    )


def stock_chart(data):

    fig = go.Figure()


    fig.add_trace(
        go.Bar(

            x=data["store_id"].astype(str),

            y=data[
                "recommended_stock"
            ],

            marker=dict(
                color="#111827"
            ),

            text=[
                f"{v:,.0f}"
                for v in data[
                    "recommended_stock"
                ]
            ],

            textposition="outside",

            textfont=dict(
                color="#111827",
                size=10
            ),

            hovertemplate=
                "Store %{x}<br>"
                "Recommended Stock: %{y:,.0f}"
                "<extra></extra>"
        )
    )


    fig.update_layout(
        showlegend=False
    )


    return base_layout(
        fig,
        300
    )


def risk_chart(high, medium, low):

    fig = go.Figure()


    fig.add_trace(
        go.Pie(

            labels=[
                "High",
                "Medium",
                "Low"
            ],

            values=[
                high,
                medium,
                low
            ],

            hole=0.68,

            marker=dict(
                colors=[
                    "#111827",
                    "#6b7280",
                    "#d1d5db"
                ]
            ),

            textinfo="percent",

            hovertemplate=
                "<b>%{label}</b><br>"
                "%{value:,} store-items"
                "<extra></extra>"
        )
    )


    fig.update_layout(

        showlegend=True,

        legend=dict(
            orientation="h",
            y=-0.03,
            x=0.5,
            xanchor="center"
        )

    )


    return base_layout(
        fig,
        280
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    k1, k2, k3, k4 = st.columns(4)


    with k1:

        st.markdown(
            f"""
<div class="kpi kpi-black">

<div class="kpi-label">
Actual Sales
</div>

<div class="kpi-value">
{fmt_number(actual_total)}
</div>

<div class="kpi-description">
Observed demand in test data
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with k2:

        st.markdown(
            f"""
<div class="kpi kpi-blue">

<div class="kpi-label">
Forecast WAPE
</div>

<div class="kpi-value">
{wape:.2f}%
</div>

<div class="kpi-description">
Final model performance
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with k3:

        st.markdown(
            f"""
<div class="kpi kpi-green">

<div class="kpi-label">
Recommended Stock
</div>

<div class="kpi-value">
{fmt_number(recommended_stock)}
</div>

<div class="kpi-description">
Aggregated inventory recommendation
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with k4:

        st.markdown(
            f"""
<div class="kpi kpi-orange">

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
""",
            unsafe_allow_html=True
        )


    # DEMAND

    st.markdown(
        """
<div class="section">

<div class="section-title">
Demand Overview
</div>

<div class="section-description">
Actual demand compared with model forecast.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    left, right = st.columns(
        [1.65, 1]
    )


    with left:

        st.markdown(
            """
<div class="card">

<div class="card-title">
Demand Forecast
</div>

<div class="card-description">
Actual versus predicted demand over time
</div>

</div>
""",
            unsafe_allow_html=True
        )


        daily = (
            forecast
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


        st.plotly_chart(
            forecast_chart(daily),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    # SEGMENTATION

    with right:

        st.markdown(
            """
<div class="card">

<div class="card-title">
Demand Segmentation
</div>

<div class="card-description">
Store-item distribution by demand level
</div>

</div>
""",
            unsafe_allow_html=True
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

            summary = (
                segment_summary
                .copy()
            )


            values = (
                summary[
                    "store_item_count"
                ]
                .astype(float)
            )


            total_segment = values.sum()


            st.plotly_chart(
                segmentation_chart(
                    summary
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


            # SEGMENT CARDS

            segment_cols = st.columns(
                len(summary)
            )


            for col, (_, row) in zip(
                segment_cols,
                summary.iterrows()
            ):

                value = float(
                    row[
                        "store_item_count"
                    ]
                )


                share = (
                    value /
                    total_segment *
                    100
                    if total_segment > 0
                    else 0
                )


                with col:

                    st.markdown(
                        f"""
<div class="segment-card">

<div class="segment-name">
{row["business_level"]}
</div>

<div class="segment-value">
{int(value):,}
</div>

<div class="segment-percent">
{share:.1f}% of store-items
</div>

</div>
""",
                        unsafe_allow_html=True
                    )


            # INSIGHT

            top_row = summary.loc[
                summary[
                    "store_item_count"
                ].idxmax()
            ]


            top_name = str(
                top_row[
                    "business_level"
                ]
            )


            top_value = float(
                top_row[
                    "store_item_count"
                ]
            )


            top_share = (
                top_value /
                total_segment *
                100
                if total_segment > 0
                else 0
            )


            st.markdown(
                f"""
<div class="insight">

<div class="insight-title">
Segmentation Insight
</div>

<div class="insight-text">
{top_name} is the largest demand segment,
representing {top_share:.1f}% of all store-item combinations.
This segment should receive the highest attention
when planning inventory capacity.
</div>

</div>
""",
                unsafe_allow_html=True
            )


        else:

            st.info(
                "Demand segmentation data belum tersedia."
            )


    # INVENTORY

    st.markdown(
        """
<div class="section">

<div class="section-title">
Inventory Intelligence
</div>

<div class="section-description">
Risk distribution and recommended inventory level.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    risk_col, stock_col = st.columns(
        [1, 1.6]
    )


    with risk_col:

        category = (
            optimization[
                "demand_category"
            ]
            .astype(str)
            .str.lower()
            .str.strip()
            if "demand_category"
            in optimization.columns
            else pd.Series(dtype=str)
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


        st.markdown(
            """
<div class="card">

<div class="card-title">
Stockout Risk
</div>

<div class="card-description">
Current demand priority distribution
</div>

</div>
""",
            unsafe_allow_html=True
        )


        st.plotly_chart(
            risk_chart(
                high,
                medium,
                low
            ),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    with stock_col:

        st.markdown(
            """
<div class="card">

<div class="card-title">
Recommended Stock by Store
</div>

<div class="card-description">
Aggregated recommended inventory
</div>

</div>
""",
            unsafe_allow_html=True
        )


        if (
            "store_id"
            in optimization.columns
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
                .head(10)
            )


            st.plotly_chart(
                stock_chart(
                    store_stock
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


    # MODEL

    st.markdown(
        """
<div class="section">

<div class="section-title">
Model Performance
</div>

<div class="section-description">
Evaluation of the final forecasting model.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    m1, m2, m3, m4 = st.columns(4)


    m1.metric(
        "MAE",
        f"{mae:.2f}"
    )


    m2.metric(
        "RMSE",
        f"{rmse:.2f}"
    )


    m3.metric(
        "WAPE",
        f"{wape:.2f}%"
    )


    m4.metric(
        "MAE Improvement",
        f"{mae_improvement:.2f}%"
    )


# ============================================================
# FORECAST
# ============================================================

elif page == "Forecast":

    st.markdown(
        """
<div class="section">

<div class="section-title">
Forecast Analysis
</div>

<div class="section-description">
Analyze actual demand and model predictions.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    stores = ["All"]

    items = ["All"]


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


    f1, f2 = st.columns(2)


    selected_store = f1.selectbox(
        "Store",
        stores
    )


    selected_item = f2.selectbox(
        "Item",
        items
    )


    filtered = forecast.copy()


    if (
        selected_store != "All"
        and
        "store_id" in filtered.columns
    ):

        filtered = filtered[
            filtered[
                "store_id"
            ]
            .astype(str)
            ==
            selected_store
        ]


    if (
        selected_item != "All"
        and
        "item_id" in filtered.columns
    ):

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
            "Tidak ada data untuk filter yang dipilih."
        )

    else:

        actual = (
            filtered[
                "actual_sales"
            ].sum()
            if "actual_sales"
            in filtered.columns
            else 0
        )


        predicted = (
            filtered[
                "predicted_sales"
            ].sum()
            if "predicted_sales"
            in filtered.columns
            else 0
        )


        a, b, c = st.columns(3)


        a.metric(
            "Actual Demand",
            fmt_number(actual)
        )


        b.metric(
            "Forecast Demand",
            fmt_number(predicted)
        )


        c.metric(
            "Difference",
            fmt_number(
                actual - predicted
            )
        )


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


        st.plotly_chart(
            forecast_chart(
                daily
            ),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


        st.markdown(
            """
<div class="section">

<div class="section-title">
Forecast Records
</div>

<div class="section-description">
Detailed prediction output.
</div>

</div>
""",
            unsafe_allow_html=True
        )


        st.dataframe(
            filtered.sort_values(
                "date",
                ascending=False
            ),
            hide_index=True,
            use_container_width=True,
            height=520
        )


# ============================================================
# INVENTORY
# ============================================================

elif page == "Inventory Analysis":

    st.markdown(
        """
<div class="section">

<div class="section-title">
Inventory Analysis
</div>

<div class="section-description">
Demand characteristics and inventory recommendation
for each store-item.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    if segments.empty:

        st.warning(
            "Segmentation data belum tersedia."
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
        stores
    )


    item_list = sorted(
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
        item_list
    )


    seg = segments[
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


    inv = optimization[
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


    if seg.empty or inv.empty:

        st.warning(
            "Detail store-item tidak ditemukan."
        )

        st.stop()


    s = seg.iloc[0]

    i = inv.iloc[0]


    k1, k2, k3, k4 = st.columns(4)


    k1.metric(
        "Average Forecast",
        fmt_decimal(
            i.get(
                "avg_forecast_demand",
                0
            )
        )
    )


    k2.metric(
        "Demand Variability",
        fmt_decimal(
            i.get(
                "demand_std",
                0
            )
        )
    )


    k3.metric(
        "Demand Buffer",
        fmt_decimal(
            i.get(
                "demand_buffer",
                0
            )
        )
    )


    k4.metric(
        "Recommended Stock",
        fmt_number(
            i.get(
                "recommended_stock",
                0
            )
        )
    )


    st.markdown(
        """
<div class="section">

<div class="section-title">
Store-Item Profile
</div>

</div>
""",
        unsafe_allow_html=True
    )


    detail = pd.DataFrame(
        {
            "Metric": [
                "Store",
                "Item",
                "Demand Segment",
                "Cluster",
                "Average Demand",
                "Demand Variability",
                "Coefficient of Variation",
                "Forecast Error",
                "Absolute Forecast Error"
            ],

            "Value": [
                selected_store,
                selected_item,
                s.get(
                    "demand_segment",
                    "-"
                ),
                s.get(
                    "cluster_k3",
                    "-"
                ),
                s.get(
                    "average_demand",
                    "-"
                ),
                s.get(
                    "demand_variability",
                    "-"
                ),
                s.get(
                    "coefficient_of_variation",
                    "-"
                ),
                s.get(
                    "forecast_error",
                    "-"
                ),
                s.get(
                    "absolute_forecast_error",
                    "-"
                )
            ]
        }
    )


    st.dataframe(
        detail,
        hide_index=True,
        use_container_width=True
    )


# ============================================================
# SEGMENTATION
# ============================================================

elif page == "Demand Segmentation":

    st.markdown(
        """
<div class="section">

<div class="section-title">
Demand Segmentation
</div>

<div class="section-description">
Store-item distribution based on demand behavior.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    if segment_summary.empty:

        st.warning(
            "Demand segment summary belum tersedia."
        )

        st.stop()


    summary = (
        segment_summary.copy()
    )


    summary["store_item_count"] = (
        pd.to_numeric(
            summary[
                "store_item_count"
            ],
            errors="coerce"
        )
        .fillna(0)
    )


    total = summary[
        "store_item_count"
    ].sum()


    summary["share"] = (
        summary[
            "store_item_count"
        ]
        /
        total
        *
        100
        if total > 0
        else 0
    )


    k1, k2, k3, k4 = st.columns(4)


    k1.metric(
        "Total Store-Items",
        f"{int(total):,}"
    )


    for idx, (_, row) in enumerate(
        summary.iterrows()
    ):

        if idx >= 3:
            break

        label = str(
            row["business_level"]
        )

        value = int(
            row[
                "store_item_count"
            ]
        )

        share = float(
            row["share"]
        )


        if idx == 0:
            target = k2

        elif idx == 1:
            target = k3

        else:
            target = k4


        with target:

            st.metric(
                label,
                f"{value:,}",
                f"{share:.1f}%"
            )


    st.markdown(
        """
<div class="section">

<div class="section-title">
Segment Distribution
</div>

<div class="section-description">
Comparison of store-item volume across demand levels.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    st.plotly_chart(
        segmentation_chart(
            summary
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    dominant = summary.loc[
        summary[
            "store_item_count"
        ].idxmax()
    ]


    dominant_name = str(
        dominant[
            "business_level"
        ]
    )


    dominant_count = int(
        dominant[
            "store_item_count"
        ]
    )


    dominant_share = float(
        dominant[
            "share"
        ]
    )


    st.markdown(
        f"""
<div class="insight">

<div class="insight-title">
Key Insight
</div>

<div class="insight-text">
The {dominant_name.lower()} segment is the largest group,
with {dominant_count:,} store-item combinations
or {dominant_share:.1f}% of the portfolio.
This segment should be considered when prioritizing
inventory planning and demand monitoring.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        """
<div class="section">

<div class="section-title">
Store-Item Segments
</div>

<div class="section-description">
Detailed segmentation output.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    st.dataframe(
        segments,
        hide_index=True,
        use_container_width=True,
        height=540
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.markdown(
        """
<div class="section">

<div class="section-title">
Inventory Recommendations
</div>

<div class="section-description">
Prioritized inventory recommendations by store-item.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    rec = optimization.copy()


    search = st.text_input(
        "Search store or item"
    )


    if search:

        store_match = (
            rec[
                "store_id"
            ]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )


        item_match = (
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
            store_match
            |
            item_match
        ]


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


    selected_category = st.selectbox(
        "Demand Category",
        categories
    )


    if selected_category != "All":

        rec = rec[
            rec[
                "demand_category"
            ]
            .astype(str)
            ==
            selected_category
        ]


    rec = rec.sort_values(
        "recommended_stock",
        ascending=False
    )


    st.metric(
        "Filtered Recommendations",
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
        c
        for c in columns
        if c in rec.columns
    ]


    st.dataframe(
        rec[columns],
        hide_index=True,
        use_container_width=True,
        height=570
    )


# ============================================================
# AI
# ============================================================

elif page == "AI Analysis":

    st.markdown(
        """
<div class="section">

<div class="section-title">
Business Analysis
</div>

<div class="section-description">
Interpretation generated from forecasting,
segmentation, and inventory outputs.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    avg_demand = (
        optimization[
            "avg_forecast_demand"
        ].mean()
        if "avg_forecast_demand"
        in optimization.columns
        else 0
    )


    avg_std = (
        optimization[
            "demand_std"
        ].mean()
        if "demand_std"
        in optimization.columns
        else 0
    )


    avg_stock = (
        optimization[
            "recommended_stock"
        ].mean()
        if "recommended_stock"
        in optimization.columns
        else 0
    )


    a, b, c = st.columns(3)


    a.metric(
        "Average Demand",
        fmt_decimal(avg_demand)
    )


    b.metric(
        "Average Variability",
        fmt_decimal(avg_std)
    )


    c.metric(
        "Average Recommended Stock",
        fmt_decimal(avg_stock)
    )


    st.markdown(
        """
<div class="section">

<div class="section-title">
Business Insights
</div>

</div>
""",
        unsafe_allow_html=True
    )


    if avg_demand > 30:

        demand_text = (
            "Average forecast demand is relatively high."
        )

    elif avg_demand > 15:

        demand_text = (
            "Average forecast demand is at a moderate level."
        )

    else:

        demand_text = (
            "Average forecast demand is relatively low."
        )


    if avg_std > 10:

        variability_text = (
            "Demand variability is relatively high, "
            "so inventory buffers should be considered carefully."
        )

    else:

        variability_text = (
            "Demand variability is relatively controlled."
        )


    insights = [
        demand_text,
        variability_text,
        (
            f"The average recommended stock is "
            f"{avg_stock:.0f} units per store-item."
        ),
        (
            f"The forecasting model achieved "
            f"{wape:.2f}% WAPE on the test data."
        )
    ]


    for insight in insights:

        st.markdown(
            f"""
<div class="insight">

<div class="insight-text">
{insight}
</div>

</div>
""",
            unsafe_allow_html=True
        )


# ============================================================
# HEALTH
# ============================================================

elif page == "System Health":

    st.markdown(
        """
<div class="section">

<div class="section-title">
System Health
</div>

<div class="section-description">
Availability of ForecastOpti pipeline outputs.
</div>

</div>
""",
        unsafe_allow_html=True
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

        exists = path.exists()


        status = (
            "Available"
            if exists
            else "Missing"
        )


        color = (
            "#166534"
            if exists
            else "#991b1b"
        )


        background = (
            "#f0fdf4"
            if exists
            else "#fef2f2"
        )


        st.markdown(
            f"""
<div style="
background:#ffffff;
border:1px solid #e5e7eb;
border-radius:12px;
padding:14px 16px;
margin-bottom:9px;
display:flex;
justify-content:space-between;
align-items:center;
">

<div>

<div style="
font-size:12px;
font-weight:800;
color:#111827;
">
{name}
</div>

<div style="
font-size:9px;
color:#6b7280;
margin-top:3px;
">
{path.name}
</div>

</div>

<div style="
background:{background};
color:{color};
border-radius:999px;
padding:5px 9px;
font-size:8px;
font-weight:800;
">
{status}
</div>

</div>
""",
            unsafe_allow_html=True
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
        "Segmentation Rows",
        f"{len(segments):,}"
    )