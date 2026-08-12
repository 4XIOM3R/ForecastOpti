from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

FORECAST_DIR = PROJECT_DIR / "outputs" / "forecasts"
EVALUATION_DIR = PROJECT_DIR / "outputs" / "evaluation"
OPTIMIZATION_DIR = PROJECT_DIR / "outputs" / "optimization"
CLUSTERING_DIR = PROJECT_DIR / "outputs" / "clustering"


# ============================================================
# 2. FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="ForecastOpti API",
    description=(
        "Backend API untuk demand forecasting, "
        "inventory optimization, dan segmentasi permintaan."
    ),
    version="1.0.0",
)


# ============================================================
# 3. LOAD EXISTING OUTPUTS
# ============================================================

def load_data():
    """
    Membaca output yang sudah dihasilkan oleh
    tahap forecasting, evaluation, optimization,
    dan clustering.
    """

    daily_forecast = pd.read_csv(
        FORECAST_DIR / "daily_forecast_summary.csv"
    )

    evaluation = pd.read_csv(
        EVALUATION_DIR / "test_evaluation.csv"
    )

    improvement = pd.read_csv(
        EVALUATION_DIR / "model_improvement_comparison.csv"
    )

    optimization = pd.read_csv(
        OPTIMIZATION_DIR / "inventory_recommendations.csv"
    )

    clustering = pd.read_csv(
        CLUSTERING_DIR / "store_item_demand_segments.csv"
    )

    cluster_summary = pd.read_csv(
        CLUSTERING_DIR / "demand_segment_summary.csv"
    )

    return {
        "daily_forecast": daily_forecast,
        "evaluation": evaluation,
        "improvement": improvement,
        "optimization": optimization,
        "clustering": clustering,
        "cluster_summary": cluster_summary,
    }


# ============================================================
# 4. ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "project": "ForecastOpti",
        "status": "online",
        "message": "ForecastOpti API is running."
    }


# ============================================================
# 5. HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health_check():

    try:
        data = load_data()

        return {
            "status": "healthy",
            "forecast_rows": len(
                data["daily_forecast"]
            ),
            "optimization_rows": len(
                data["optimization"]
            ),
            "clustering_rows": len(
                data["clustering"]
            ),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )