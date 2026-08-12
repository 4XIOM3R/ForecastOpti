import streamlit as st
import pandas as pd
from pathlib import Path
from textwrap import dedent


# ============================================================
# FORECASTOPTI
# STREAMLIT BUSINESS INTELLIGENCE DASHBOARD
# ============================================================


# ============================================================
# PROJECT PATH
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
# HTML RENDERER
# ============================================================

def html(markup):
    """
    Render HTML tanpa indentation yang menyebabkan
    Streamlit menganggapnya sebagai code block.
    """

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
    """
    Mengamankan DataFrame sebelum dikirim ke Streamlit.

    Masalah yang diamankan:
    - mixed int/string
    - object dtype
    - nilai seperti:
        10
        20
        Tinggi

    Hal ini mencegah PyArrow:
    ArrowInvalid:
    Could not convert 'Tinggi'
    with type str: tried to convert to int64
    """

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


# ============================================================
# DATAFRAME DISPLAY
# ============================================================

def display_dataframe(
    df,
    hide_index=True,
    height=None
):

    safe_df = safe_dataframe(df)

    kwargs = {
        "hide_index": hide_index,
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


def money(value):

    return f"{safe_float(value):,.0f}"


def number(value):

    return f"{safe_float(value):,.2f}"


# ============================================================
# CSV LOADER
# ============================================================

def load_csv(
    directory,
    filename
):

    path = directory / filename

    if not path.exists():
        return None

    return pd.read_csv(path)


# ============================================================
# CUSTOM CSS
# ============================================================

html("""
<style>

/* ============================================================
   GLOBAL VARIABLES
   ============================================================ */

:root {

    --blue: #2563eb;
    --blue-dark: #1d4ed8;

    --navy: #172033;

    --text: #344054;
    --muted: #667085;

    --border: #e4e7ec;

    --background: #f5f7fa;

    --white: #ffffff;

    --green: #16a34a;
    --orange: #f59e0b;
    --red: #dc2626;
}


/* ============================================================
   MAIN APPLICATION
   ============================================================ */

.stApp {

    background: #f5f7fa !important;

    color: #344054 !important;
}


.block-container {

    max-width: 1450px !important;

    padding-top: 1.5rem !important;

    padding-bottom: 3rem !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

/*
   IMPORTANT:

   Sidebar ForecastOpti dibuat selalu LIGHT.

   Jadi walaupun Streamlit berada pada Dark Mode,
   sidebar tetap:

   background = putih
   text       = dark
*/

[data-testid="stSidebar"] {

    background: #ffffff !important;

    color: #344054 !important;

    border-right: 1px solid #e4e7ec !important;
}


/*
   Jangan menggunakan:

   [data-testid="stSidebar"] *

   dengan color global karena dapat menimpa
   warna button active.
*/


[data-testid="stSidebar"] > div:first-child {

    background: #ffffff !important;

    padding-top: 1rem !important;
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.sidebar-brand {

    padding:
        8px
        8px
        22px
        8px;
}


.sidebar-brand-label {

    color: #2563eb !important;

    font-size: 10px !important;

    font-weight: 800 !important;

    letter-spacing: .18em !important;

    margin-bottom: 4px !important;
}


.sidebar-brand-title {

    color: #172033 !important;

    font-size: 21px !important;

    font-weight: 800 !important;

    line-height: 1.15 !important;
}


.sidebar-brand-subtitle {

    color: #98a2b3 !important;

    font-size: 11px !important;

    margin-top: 5px !important;

    line-height: 1.4 !important;
}


/* ============================================================
   SIDEBAR SECTION LABEL
   ============================================================ */

.sidebar-section-label {

    color: #98a2b3 !important;

    font-size: 10px !important;

    font-weight: 800 !important;

    letter-spacing: .12em !important;

    text-transform: uppercase !important;

    padding:
        0
        8px
        8px
        8px !important;
}


/* ============================================================
   NAV BUTTON CONTAINER
   ============================================================ */

[data-testid="stSidebar"] .nav-button,
[data-testid="stSidebar"] .nav-active {

    width: 100% !important;
}


/* ============================================================
   NORMAL NAV BUTTON
   ============================================================ */

[data-testid="stSidebar"]
.nav-button
button {

    width: 100% !important;

    min-height: 42px !important;

    padding:
        8px
        12px !important;

    margin:
        2px
        0 !important;

    border-radius: 10px !important;

    border:
        1px solid
        transparent !important;

    background:
        #ffffff !important;

    color:
        #344054 !important;

    font-size:
        13px !important;

    font-weight:
        600 !important;

    text-align:
        left !important;

    box-shadow:
        none !important;

    transition:
        background-color .15s ease,
        color .15s ease,
        border-color .15s ease !important;
}


/* ============================================================
   NORMAL NAV TEXT
   ============================================================ */

[data-testid="stSidebar"]
.nav-button
button p {

    color: #344054 !important;

    font-size: 13px !important;

    font-weight: 600 !important;

    text-align: left !important;
}


[data-testid="stSidebar"]
.nav-button
button span {

    color: #344054 !important;
}


[data-testid="stSidebar"]
.nav-button
button div {

    color: #344054 !important;
}


/* ============================================================
   NAV HOVER
   ============================================================ */

[data-testid="stSidebar"]
.nav-button
button:hover {

    background:
        #f2f4f7 !important;

    color:
        #172033 !important;

    border:
        1px solid
        #eaecf0 !important;
}


[data-testid="stSidebar"]
.nav-button
button:hover p {

    color:
        #172033 !important;
}


/* ============================================================
   ACTIVE NAV BUTTON
   ============================================================ */

[data-testid="stSidebar"]
.nav-active
button {

    width: 100% !important;

    min-height: 42px !important;

    padding:
        8px
        12px !important;

    margin:
        2px
        0 !important;

    border-radius:
        10px !important;

    background:
        #eff6ff !important;

    border:
        1px solid
        #dbeafe !important;

    color:
        #1d4ed8 !important;

    font-size:
        13px !important;

    font-weight:
        800 !important;

    text-align:
        left !important;

    box-shadow:
        inset 3px 0 0 #2563eb !important;
}


/* ============================================================
   ACTIVE NAV TEXT
   ============================================================ */

[data-testid="stSidebar"]
.nav-active
button p {

    color:
        #1d4ed8 !important;

    font-size:
        13px !important;

    font-weight:
        800 !important;
}


[data-testid="stSidebar"]
.nav-active
button span {

    color:
        #1d4ed8 !important;
}


[data-testid="stSidebar"]
.nav-active
button div {

    color:
        #1d4ed8 !important;
}


/* ============================================================
   CLEAR CACHE BUTTON
   ============================================================ */

[data-testid="stSidebar"]
.stButton
button {

    background:
        #ffffff !important;

    color:
        #344054 !important;

    border:
        1px solid
        #e4e7ec !important;

    border-radius:
        9px !important;

    font-size:
        12px !important;

    font-weight:
        700 !important;
}


[data-testid="stSidebar"]
.stButton
button p {

    color:
        #344054 !important;

    font-size:
        12px !important;

    font-weight:
        700 !important;
}


[data-testid="stSidebar"]
.stButton
button:hover {

    background:
        #f2f4f7 !important;

    color:
        #172033 !important;
}


/* ============================================================
   SIDEBAR FOOTER
   ============================================================ */

.sidebar-footer {

    margin-top:
        18px !important;

    padding:
        12px 8px !important;

    border-top:
        1px solid
        #e4e7ec !important;

    color:
        #98a2b3 !important;

    font-size:
        10px !important;

    line-height:
        1.5 !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    background:
        linear-gradient(
            135deg,
            #172033 0%,
            #223a67 55%,
            #2563eb 100%
        ) !important;

    padding:
        30px 32px !important;

    border-radius:
        18px !important;

    margin-bottom:
        24px !important;

    box-shadow:
        0 10px 30px
        rgba(
            16,
            24,
            40,
            0.10
        ) !important;
}


.hero-eyebrow {

    color:
        #93c5fd !important;

    font-size:
        10px !important;

    font-weight:
        800 !important;

    letter-spacing:
        .18em !important;

    margin-bottom:
        6px !important;
}


.hero-title {

    color:
        #ffffff !important;

    font-size:
        32px !important;

    font-weight:
        800 !important;

    line-height:
        1.1 !important;

    margin:
        0 !important;
}


.hero-description {

    color:
        #dbe5f1 !important;

    font-size:
        13px !important;

    line-height:
        1.6 !important;

    margin-top:
        8px !important;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {

    color:
        #172033 !important;

    font-size:
        18px !important;

    font-weight:
        800 !important;

    margin-top:
        24px !important;

    margin-bottom:
        10px !important;
}


.section-subtitle {

    color:
        #667085 !important;

    font-size:
        12px !important;

    line-height:
        1.5 !important;

    margin-top:
        -3px !important;

    margin-bottom:
        15px !important;
}


/* ============================================================
   CARD
   ============================================================ */

.card {

    background:
        #ffffff !important;

    border:
        1px solid
        #e4e7ec !important;

    border-radius:
        14px !important;

    padding:
        18px !important;

    box-shadow:
        0 3px 12px
        rgba(
            16,
            24,
            40,
            0.035
        ) !important;

    color:
        #344054 !important;
}


/* ============================================================
   METRIC
   ============================================================ */

div[data-testid="stMetric"] {

    background:
        #ffffff !important;

    border:
        1px solid
        #e4e7ec !important;

    border-radius:
        14px !important;

    padding:
        15px !important;

    box-shadow:
        0 3px 12px
        rgba(
            16,
            24,
            40,
            0.035
        ) !important;
}


div[data-testid="stMetricLabel"] {

    color:
        #667085 !important;
}


div[data-testid="stMetricValue"] {

    color:
        #172033 !important;

    font-weight:
        800 !important;
}


div[data-testid="stMetricDelta"] {

    color:
        #667085 !important;
}


/* ============================================================
   INPUT
   ============================================================ */

.stSelectbox > div > div,
.stTextInput > div > div {

    border-radius:
        9px !important;
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
        1px solid
        #e4e7ec !important;
}


/* ============================================================
   INSIGHT
   ============================================================ */

.insight {

    background:
        #ffffff !important;

    border:
        1px solid
        #e4e7ec !important;

    border-left:
        4px solid
        #2563eb !important;

    border-radius:
        0 9px 9px 0 !important;

    padding:
        12px 15px !important;

    margin-bottom:
        9px !important;

    color:
        #344054 !important;

    font-size:
        13px !important;

    line-height:
        1.55 !important;
}


/* ============================================================
   BADGES
   ============================================================ */

.badge {

    display:
        inline-block;

    padding:
        5px 10px;

    border-radius:
        999px;

    font-size:
        11px;

    font-weight:
        800;
}


.badge-high {

    background:
        #fef2f2;

    color:
        #b91c1c;
}


.badge-medium {

    background:
        #fff7ed;

    color:
        #c2410c;
}


.badge-low {

    background:
        #ecfdf3;

    color:
        #15803d;
}


/* ============================================================
   HEALTH CARD
   ============================================================ */

.health-card {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    background:
        #ffffff;

    border:
        1px solid
        #e4e7ec;

    border-radius:
        12px;

    padding:
        13px 16px;

    margin-bottom:
        9px;
}


.health-name {

    color:
        #172033;

    font-size:
        13px;

    font-weight:
        700;
}


.health-status {

    color:
        #15803d;

    font-size:
        12px;

    font-weight:
        800;

    background:
        #ecfdf3;

    padding:
        5px 10px;

    border-radius:
        999px;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {

    border-color:
        #e4e7ec !important;
}


/* ============================================================
   CODE BLOCK
   ============================================================ */

[data-testid="stCodeBlock"] {

    border-radius:
        12px !important;
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
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {

    border-radius:
        10px !important;
}


/* ============================================================
   DARK MODE PROTECTION
   ============================================================ */

/*
   Beberapa elemen Streamlit menggunakan CSS theme
   dengan specificity tinggi.

   Kita override elemen teks utama agar dashboard
   tetap readable ketika browser/Streamlit berada
   pada dark mode.
*/

@media (prefers-color-scheme: dark) {

    [data-testid="stSidebar"] {

        background:
            #ffffff !important;

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"]
    .sidebar-brand-title {

        color:
            #172033 !important;
    }


    [data-testid="stSidebar"]
    .sidebar-section-label {

        color:
            #98a2b3 !important;
    }


    [data-testid="stSidebar"]
    .nav-button
    button {

        background:
            #ffffff !important;

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"]
    .nav-button
    button p {

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"]
    .nav-active
    button {

        background:
            #eff6ff !important;

        color:
            #1d4ed8 !important;
    }


    [data-testid="stSidebar"]
    .nav-active
    button p {

        color:
            #1d4ed8 !important;
    }


    [data-testid="stSidebar"]
    .stButton
    button {

        background:
            #ffffff !important;

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"]
    .stButton
    button p {

        color:
            #344054 !important;
    }


    [data-testid="stSidebar"]
    .sidebar-footer {

        color:
            #98a2b3 !important;
    }
}

</style>
""")


# ============================================================
# LOAD DATA
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
        and
        "date" in forecast.columns
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


# ============================================================
# INITIALIZE DATA
# ============================================================

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
# DATA VALIDATION
# ============================================================

if forecast is None:

    st.error(
        "File tidak ditemukan:\n\n"
        "outputs/forecasts/test_forecast.csv"
    )

    st.stop()


if optimization is None:

    st.error(
        "File tidak ditemukan:\n\n"
        "outputs/optimization/inventory_recommendations.csv"
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
    and
    len(improvement) > 1
):

    final_model = improvement.iloc[1]

elif (
    improvement is not None
    and
    len(improvement) > 0
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
# TOTAL ACTUAL
# ============================================================

if "actual_sales" in forecast.columns:

    total_actual = safe_float(
        forecast[
            "actual_sales"
        ].sum()
    )

else:

    total_actual = 0


# ============================================================
# TOTAL STORE ITEMS
# ============================================================

if (
    not segments.empty
    and
    "store_id" in segments.columns
    and
    "item_id" in segments.columns
):

    total_store_items = (
        segments[
            [
                "store_id",
                "item_id"
            ]
        ]
        .drop_duplicates()
        .shape[0]
    )

elif (
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


# ============================================================
# NAVIGATION
# ============================================================

PAGES = [
    "Overview",
    "Forecast",
    "Inventory Analysis",
    "Demand Segmentation",
    "Recommendations",
    "AI Analysis",
    "System Health"
]


if "forecastopti_page" not in st.session_state:

    st.session_state.forecastopti_page = "Overview"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html(
        """
<div class="sidebar-brand">

<div class="sidebar-brand-label">
FORECASTOPTI
</div>

<div class="sidebar-brand-title">
BI Dashboard
</div>

<div class="sidebar-brand-subtitle">
Demand & Inventory Intelligence
</div>

</div>
"""
    )


    html(
        """
<div class="sidebar-section-label">
Navigation
</div>
"""
    )


    for page_name in PAGES:

        is_active = (
            st.session_state.forecastopti_page
            == page_name
        )

        if is_active:

            button_class = "nav-active"

        else:

            button_class = "nav-button"


        st.markdown(
            f'<div class="{button_class}">',
            unsafe_allow_html=True
        )


        clicked = st.button(
            page_name,
            key=f"nav_{page_name}",
            width="stretch"
        )


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

Demand Forecasting &
Inventory Intelligence

</div>
"""
    )


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.forecastopti_page


# ============================================================
# HERO
# ============================================================

html(
    f"""
<div class="hero">

<div class="hero-eyebrow">
BUSINESS INTELLIGENCE
</div>

<div class="hero-title">
{page}
</div>

<div class="hero-description">
Forecasting, inventory optimization,
segmentation, dan decision support
dalam satu dashboard.
</div>

</div>
"""
)


# ============================================================
# PAGE: OVERVIEW
# ============================================================

if page == "Overview":

    html(
        """
<div class="section-title">
Executive Overview
</div>

<div class="section-subtitle">
Ringkasan performa forecasting dan kondisi inventory.
</div>
"""
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    c1.metric(
        "Actual Sales",
        money(total_actual)
    )


    c2.metric(
        "MAE",
        number(test_mae)
    )


    c3.metric(
        "RMSE",
        number(test_rmse)
    )


    c4.metric(
        "WAPE",
        f"{test_wape:.2f}%"
    )


    c5.metric(
        "Store-Items",
        f"{total_store_items:,}"
    )


    st.caption(
        f"Final model: {model_name}"
    )


    left, right = st.columns(
        [1.65, 1]
    )


    with left:

        html(
            """
<div class="section-title">
Actual vs Predicted
</div>
"""
        )


        if (
            "date" in forecast.columns
            and
            "actual_sales" in forecast.columns
            and
            "predicted_sales" in forecast.columns
        ):

            daily = (
                forecast
                .groupby("date")[
                    [
                        "actual_sales",
                        "predicted_sales"
                    ]
                ]
                .sum()
                .sort_index()
            )


            st.line_chart(
                daily,
                width="stretch"
            )

        else:

            st.warning(
                "Kolom forecasting tidak lengkap."
            )


    with right:

        html(
            """
<div class="section-title">
Demand Distribution
</div>
"""
        )


        if not segment_summary.empty:

            if (
                "business_level"
                in segment_summary.columns
                and
                "store_item_count"
                in segment_summary.columns
            ):

                counts = (
                    segment_summary
                    .set_index(
                        "business_level"
                    )[
                        "store_item_count"
                    ]
                )


                st.bar_chart(
                    counts,
                    width="stretch"
                )


                display_dataframe(
                    segment_summary[
                        [
                            "business_level",
                            "store_item_count"
                        ]
                    ]
                )

            else:

                st.warning(
                    "Kolom segment summary tidak lengkap."
                )

        else:

            st.info(
                "Data segment summary belum tersedia."
            )


    html(
        """
<div class="section-title">
Business Snapshot
</div>
"""
    )


    a, b = st.columns(2)


    with a:

        html(
            f"""
<div class="card">

<b>
Model Performance
</b>

<p style="
color:#667085;
">

Model:
<strong>
{model_name}
</strong>

</p>

<p style="
color:#667085;
">

MAE:
<strong>
{test_mae:.2f}
</strong>

&nbsp;&nbsp;

RMSE:
<strong>
{test_rmse:.2f}
</strong>

&nbsp;&nbsp;

WAPE:
<strong>
{test_wape:.2f}%
</strong>

</p>

</div>
"""
        )


    with b:

        html(
            """
<div class="card">

<b>
Inventory Decision Support
</b>

<p style="
color:#667085;
line-height:1.7;
">

Forecast demand,
demand variability,
demand buffer,
dan recommended stock
digunakan untuk membantu
menentukan prioritas persediaan.

</p>

</div>
"""
        )


# ============================================================
# PAGE: FORECAST
# ============================================================

elif page == "Forecast":

    html(
        """
<div class="section-title">
Forecast Analysis
</div>

<div class="section-subtitle">
Analisis actual demand dibandingkan dengan
hasil forecasting.
</div>
"""
    )


    if (
        "store_id" not in forecast.columns
        or
        "item_id" not in forecast.columns
    ):

        st.error(
            "Kolom store_id atau item_id tidak ditemukan."
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
            "Tidak ada data untuk filter tersebut."
        )

    else:

        if (
            "actual_sales"
            in filtered.columns
            and
            "predicted_sales"
            in filtered.columns
        ):

            filtered = filtered.copy()


            filtered[
                "forecast_error"
            ] = (
                filtered[
                    "actual_sales"
                ]
                -
                filtered[
                    "predicted_sales"
                ]
            )


            a, b, c = st.columns(3)


            a.metric(
                "Actual Demand",
                money(
                    filtered[
                        "actual_sales"
                    ].sum()
                )
            )


            b.metric(
                "Forecast Demand",
                money(
                    filtered[
                        "predicted_sales"
                    ].sum()
                )
            )


            c.metric(
                "Average Error",
                number(
                    filtered[
                        "forecast_error"
                    ].mean()
                )
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
                    .sort_index()
                )


                st.line_chart(
                    daily,
                    width="stretch"
                )


        html(
            """
<div class="section-title">
Forecast Output
</div>
"""
        )


        if "date" in filtered.columns:

            filtered = filtered.sort_values(
                "date",
                ascending=False
            )


        display_dataframe(
            filtered,
            height=500
        )


# ============================================================
# PAGE: INVENTORY ANALYSIS
# ============================================================

elif page == "Inventory Analysis":

    html(
        """
<div class="section-title">
Interactive Store-Item Analysis
</div>

<div class="section-subtitle">
Pilih store dan item untuk melihat profil demand
dan rekomendasi inventory.
</div>
"""
    )


    if segments.empty:

        st.warning(
            "Data segmentation belum tersedia."
        )

        st.stop()


    required_columns = [
        "store_id",
        "item_id"
    ]


    missing_columns = [
        column
        for column in required_columns
        if column not in segments.columns
    ]


    if missing_columns:

        st.error(
            "Kolom segmentation yang diperlukan tidak tersedia: "
            +
            ", ".join(
                missing_columns
            )
        )

        st.stop()


    store_list = sorted(
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
        store_list,
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


    if not available_items:

        st.warning(
            "Tidak ada item untuk store tersebut."
        )

        st.stop()


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
            "Data segmentation store-item tidak tersedia."
        )

        st.stop()


    if selected_inv.empty:

        st.warning(
            "Data inventory recommendation "
            "store-item tidak tersedia."
        )

        st.stop()


    seg = selected_seg.iloc[0]

    inv = selected_inv.iloc[0]


    html(
        f"""
<div class="card">

<span style="
color:#667085;
">
Store
</span>

<strong>
{selected_store}
</strong>

<span style="
color:#98a2b3;
">
/
</span>

<span style="
color:#667085;
">
Item
</span>

<strong>
{selected_item}
</strong>

</div>
"""
    )


    st.write("")


    k1, k2, k3, k4, k5 = st.columns(5)


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
        "Max Forecast",
        number(
            inv.get(
                "max_forecast_demand",
                0
            )
        )
    )


    k3.metric(
        "Demand Std",
        number(
            inv.get(
                "demand_std",
                0
            )
        )
    )


    k4.metric(
        "Demand Buffer",
        number(
            inv.get(
                "demand_buffer",
                0
            )
        )
    )


    k5.metric(
        "Recommended Stock",
        f"{safe_float(
            inv.get(
                'recommended_stock',
                0
            )
        ):,.0f}"
    )


    left, right = st.columns(2)


    with left:

        html(
            """
<div class="section-title">
Demand Profile
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

        html(
            """
<div class="section-title">
Business Recommendation
</div>
"""
        )


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

            badge_class = "badge-high"

            recommendation = (
                "Prioritas tinggi. Store-item memiliki "
                "permintaan tinggi dan perlu mendapat "
                "perhatian dalam perencanaan persediaan."
            )

        elif category_lower in [
            "medium",
            "sedang"
        ]:

            badge_class = "badge-medium"

            recommendation = (
                "Prioritas sedang. Monitor demand dan "
                "stok secara berkala."
            )

        else:

            badge_class = "badge-low"

            recommendation = (
                "Prioritas rendah. Persediaan dapat "
                "dikelola dengan monitoring rutin."
            )


        recommended_stock = safe_float(
            inv.get(
                "recommended_stock",
                0
            )
        )


        html(
            f"""
<div class="card">

<span class="badge {badge_class}">
{category}
</span>

<h2 style="
color:#172033;
margin-top:15px;
">

{recommended_stock:,.0f}

units

</h2>

<p style="
color:#667085;
line-height:1.7;
">

{recommendation}

</p>

<hr>

<b>
Recommended Stock
</b>

<p style="
color:#667085;
">

Berdasarkan forecast demand,
demand variability,
dan demand buffer.

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
<div class="section-title">
Demand Segmentation
</div>

<div class="section-subtitle">
Distribusi store-item berdasarkan karakteristik
permintaan.
</div>
"""
    )


    if segment_summary.empty:

        st.warning(
            "demand_segment_summary.csv belum tersedia."
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
            "Kolom business_level atau store_item_count "
            "tidak ditemukan."
        )

        st.stop()


    total = safe_int(
        segment_summary[
            "store_item_count"
        ].sum()
    )


    business_level = (
        segment_summary[
            "business_level"
        ]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    low = safe_int(
        segment_summary.loc[
            business_level.isin(
                [
                    "rendah",
                    "low"
                ]
            ),
            "store_item_count"
        ].sum()
    )


    medium = safe_int(
        segment_summary.loc[
            business_level.isin(
                [
                    "sedang",
                    "medium"
                ]
            ),
            "store_item_count"
        ].sum()
    )


    high = safe_int(
        segment_summary.loc[
            business_level.isin(
                [
                    "tinggi",
                    "high"
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
        "Low",
        f"{low:,}"
    )


    c.metric(
        "Medium",
        f"{medium:,}"
    )


    d.metric(
        "High",
        f"{high:,}"
    )


    left, right = st.columns(
        [1, 1.5]
    )


    with left:

        chart_data = (
            segment_summary
            .set_index(
                "business_level"
            )[
                "store_item_count"
            ]
        )


        st.bar_chart(
            chart_data,
            width="stretch"
        )


    with right:

        display_dataframe(
            segment_summary
        )


    if not segments.empty:

        html(
            """
<div class="section-title">
Store-Item Detail
</div>
"""
        )


        q = st.text_input(
            "Search store / item",
            key="segment_search"
        )


        segment_values = [
            "All"
        ]


        if (
            "demand_segment"
            in segments.columns
        ):

            detected_segments = sorted(
                segments[
                    "demand_segment"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            segment_values += [
                value
                for value in detected_segments
                if value
                not in segment_values
            ]


        seg_filter = st.selectbox(
            "Demand Segment",
            segment_values,
            key="segment_filter"
        )


        detail = segments.copy()


        if q:

            mask = (
                detail[
                    "store_id"
                ]
                .astype(str)
                .str.contains(
                    q,
                    case=False,
                    na=False
                )
                |
                detail[
                    "item_id"
                ]
                .astype(str)
                .str.contains(
                    q,
                    case=False,
                    na=False
                )
            )


            detail = detail[
                mask
            ]


        if (
            seg_filter != "All"
            and
            "demand_segment"
            in detail.columns
        ):

            detail = detail[
                detail[
                    "demand_segment"
                ]
                .astype(str)
                ==
                seg_filter
            ]


        display_dataframe(
            detail,
            height=500
        )


# ============================================================
# PAGE: RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    html(
        """
<div class="section-title">
Inventory Recommendations
</div>

<div class="section-subtitle">
Prioritaskan store-item berdasarkan demand,
variability, forecast error, dan recommended stock.
</div>
"""
    )


    if optimization.empty:

        st.warning(
            "Data inventory recommendation kosong."
        )

        st.stop()


    rec = optimization.copy()


    search = st.text_input(
        "Search Store / Item",
        key="recommendation_search"
    )


    f1, f2, f3 = st.columns(3)


    priority_options = [
        "All"
    ]


    if "demand_category" in rec.columns:

        categories = sorted(
            rec[
                "demand_category"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        priority_options += [
            value
            for value in categories
            if value
            not in priority_options
        ]


    priority = f1.selectbox(
        "Demand Category",
        priority_options,
        key="recommendation_priority"
    )


    segment_options = [
        "All"
    ]


    if (
        not segments.empty
        and
        "demand_segment"
        in segments.columns
    ):

        segment_values = sorted(
            segments[
                "demand_segment"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


        segment_options += [
            value
            for value in segment_values
            if value
            not in segment_options
        ]


    segment = f2.selectbox(
        "Demand Segment",
        segment_options,
        key="recommendation_segment"
    )


    sort_by = f3.selectbox(
        "Sort By",
        [
            "Recommended Stock",
            "Forecast Demand",
            "Demand Variability",
            "Demand Buffer"
        ],
        key="recommendation_sort"
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


    if (
        segment != "All"
        and
        not segments.empty
        and
        "demand_segment"
        in segments.columns
    ):

        seg_lookup = segments[
            [
                "store_id",
                "item_id",
                "demand_segment"
            ]
        ].drop_duplicates()


        rec = rec.merge(
            seg_lookup,
            on=[
                "store_id",
                "item_id"
            ],
            how="left"
        )


        rec = rec[
            rec[
                "demand_segment"
            ]
            .astype(str)
            ==
            segment
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
            ascending=False
        )


    if "demand_category" in rec.columns:

        category_lower = (
            rec[
                "demand_category"
            ]
            .astype(str)
            .str.lower()
            .str.strip()
        )


        high_count = int(
            category_lower.isin(
                [
                    "high",
                    "tinggi"
                ]
            ).sum()
        )


        medium_count = int(
            category_lower.isin(
                [
                    "medium",
                    "sedang"
                ]
            ).sum()
        )


        low_count = int(
            category_lower.isin(
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


    k1, k2, k3, k4 = st.columns(4)


    k1.metric(
        "High",
        f"{high_count:,}"
    )


    k2.metric(
        "Medium",
        f"{medium_count:,}"
    )


    k3.metric(
        "Low",
        f"{low_count:,}"
    )


    k4.metric(
        "Filtered",
        f"{len(rec):,}"
    )


    display_columns = [

        "store_id",

        "item_id",

        "demand_category",

        "avg_forecast_demand",

        "max_forecast_demand",

        "demand_std",

        "demand_buffer",

        "recommended_stock"
    ]


    display_columns = [
        column
        for column in display_columns
        if column
        in rec.columns
    ]


    if rec.empty:

        st.info(
            "Tidak ada recommendation yang cocok "
            "dengan filter."
        )

    else:

        display_dataframe(
            rec[
                display_columns
            ],
            height=550
        )


# ============================================================
# PAGE: AI ANALYSIS
# ============================================================

elif page == "AI Analysis":

    html(
        """
<div class="section-title">
AI / Business Analysis
</div>

<div class="section-subtitle">
Interpretasi otomatis berdasarkan forecast,
variability, forecast error, dan inventory.
</div>
"""
    )


    if (
        "avg_forecast_demand"
        in optimization.columns
    ):

        avg_demand = safe_float(
            optimization[
                "avg_forecast_demand"
            ].mean()
        )

    else:

        avg_demand = 0


    if (
        "demand_std"
        in optimization.columns
    ):

        avg_variability = safe_float(
            optimization[
                "demand_std"
            ].mean()
        )

    else:

        avg_variability = 0


    if (
        "recommended_stock"
        in optimization.columns
    ):

        avg_stock = safe_float(
            optimization[
                "recommended_stock"
            ].mean()
        )

    else:

        avg_stock = 0


    if (
        not segments.empty
        and
        "absolute_forecast_error"
        in segments.columns
    ):

        abs_error = safe_float(
            segments[
                "absolute_forecast_error"
            ].mean()
        )

    else:

        abs_error = 0


    a, b, c, d, e = st.columns(5)


    a.metric(
        "Store-Items",
        f"{total_store_items:,}"
    )


    b.metric(
        "Avg Demand",
        number(
            avg_demand
        )
    )


    c.metric(
        "Variability",
        number(
            avg_variability
        )
    )


    d.metric(
        "Abs Forecast Error",
        number(
            abs_error
        )
    )


    e.metric(
        "Avg Recommended Stock",
        number(
            avg_stock
        )
    )


    html(
        """
<div class="section-title">
Business Insights
</div>
"""
    )


    insights = []


    if avg_demand >= 30:

        insights.append(
            "Permintaan rata-rata berada "
            "pada tingkat tinggi."
        )

    elif avg_demand >= 20:

        insights.append(
            "Permintaan rata-rata berada "
            "pada tingkat sedang."
        )

    else:

        insights.append(
            "Permintaan rata-rata berada "
            "pada tingkat rendah."
        )


    if avg_variability <= 10:

        insights.append(
            "Variabilitas demand relatif terkendali."
        )

    else:

        insights.append(
            "Variabilitas demand cukup tinggi "
            "dan perlu diperhatikan dalam "
            "perencanaan safety stock."
        )


    if abs_error <= 10:

        insights.append(
            "Absolute forecast error secara umum "
            "masih relatif terkendali."
        )

    else:

        insights.append(
            "Forecast error perlu dimonitor karena "
            "dapat mempengaruhi inventory planning."
        )


    insights.append(
        f"Rata-rata stok yang direkomendasikan "
        f"sekitar {avg_stock:.0f} unit per store-item."
    )


    for insight in insights:

        html(
            f"""
<div class="insight">
{insight}
</div>
"""
        )


    html(
        """
<div class="section-title">
Segment Business View
</div>
"""
    )


    if not segment_summary.empty:

        display_dataframe(
            segment_summary
        )

    else:

        st.info(
            "Segment summary belum tersedia."
        )


# ============================================================
# PAGE: SYSTEM HEALTH
# ============================================================

elif page == "System Health":

    html(
        """
<div class="section-title">
System Health
</div>

<div class="section-subtitle">
Pemeriksaan file output dan jumlah data ForecastOpti.
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
<div class="health-card">

<div class="health-name">
{name}
</div>

<div class="health-status">
Healthy
</div>

</div>
"""
            )

        else:

            st.error(
                f"{name}: Missing — {path}"
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
<div class="section-title">
Project Configuration
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