from pathlib import Path


# ============================================================
# PROJECT
# ============================================================

# src/config.py
# parent      -> src/
# parent.parent -> ForecastOpti/
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# DATA
# ============================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"


# ============================================================
# FIGURES
# ============================================================

FIGURES_DIR = PROJECT_ROOT / "figures"

EDA_FIGURES_DIR = FIGURES_DIR / "eda"

FORECASTING_FIGURES_DIR = FIGURES_DIR / "forecasting"

OPTIMIZATION_FIGURES_DIR = FIGURES_DIR / "optimization"


# ============================================================
# MODELS
# ============================================================

MODELS_DIR = PROJECT_ROOT / "models"


# ============================================================
# NOTEBOOKS
# ============================================================

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"


# ============================================================
# OUTPUTS
# ============================================================

OUTPUTS_DIR = PROJECT_ROOT / "outputs"


# Forecasting
FORECAST_OUTPUT_DIR = (
    OUTPUTS_DIR / "forecasts"
)


# Inventory optimization
OPTIMIZATION_OUTPUT_DIR = (
    OUTPUTS_DIR / "optimization"
)


# Model evaluation
EVALUATION_OUTPUT_DIR = (
    OUTPUTS_DIR / "evaluation"
)


# Demand clustering / segmentation
CLUSTERING_OUTPUT_DIR = (
    OUTPUTS_DIR / "clustering"
)


# ============================================================
# DATASET
# ============================================================

DATASET_PATH = (
    RAW_DATA_DIR / "retail_sales.csv"
)


# ============================================================
# MODEL FILES
# ============================================================

BASELINE_MODEL_PATH = (
    MODELS_DIR / "hist_gradient_boosting.pkl"
)


FINAL_MODEL_PATH = (
    MODELS_DIR / "hist_gradient_boosting_lag.pkl"
)


# ============================================================
# OUTPUT FILES
# ============================================================

DAILY_FORECAST_PATH = (
    FORECAST_OUTPUT_DIR /
    "daily_forecast_summary.csv"
)


TEST_FORECAST_PATH = (
    FORECAST_OUTPUT_DIR /
    "test_forecast.csv"
)


TEST_EVALUATION_PATH = (
    EVALUATION_OUTPUT_DIR /
    "test_evaluation.csv"
)


MODEL_IMPROVEMENT_PATH = (
    EVALUATION_OUTPUT_DIR /
    "model_improvement_comparison.csv"
)


INVENTORY_RECOMMENDATIONS_PATH = (
    OPTIMIZATION_OUTPUT_DIR /
    "inventory_recommendations.csv"
)


CLUSTER_DETAIL_PATH = (
    CLUSTERING_OUTPUT_DIR /
    "store_item_demand_segments.csv"
)


CLUSTER_SUMMARY_PATH = (
    CLUSTERING_OUTPUT_DIR /
    "demand_segment_summary.csv"
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

SEED = 42