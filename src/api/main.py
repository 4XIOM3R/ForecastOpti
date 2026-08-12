from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from src.config import (
    FORECAST_OUTPUT_DIR,
    OPTIMIZATION_OUTPUT_DIR,
    EVALUATION_OUTPUT_DIR,
    CLUSTERING_OUTPUT_DIR,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="ForecastOpti API",
    description=(
        "API untuk demand forecasting, "
        "inventory optimization, dan demand segmentation."
    ),
    version="1.0.0",
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AnalyzeRequest(BaseModel):
    store_id: str
    item_id: str


# ============================================================
# DATA LOADER
# ============================================================

def load_csv(directory, filename):

    path = directory / filename

    if not path.exists():

        raise FileNotFoundError(
            f"File tidak ditemukan: {path}"
        )

    return pd.read_csv(path)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "ForecastOpti",
        "status": "online",
        "message": "ForecastOpti API is running."
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health_check():

    try:

        forecast = load_csv(
            FORECAST_OUTPUT_DIR,
            "daily_forecast_summary.csv"
        )

        optimization = load_csv(
            OPTIMIZATION_OUTPUT_DIR,
            "inventory_recommendations.csv"
        )

        clustering = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "store_item_demand_segments.csv"
        )

        return {

            "status": "healthy",

            "forecast_rows": len(
                forecast
            ),

            "optimization_rows": len(
                optimization
            ),

            "clustering_rows": len(
                clustering
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# SUMMARY ENDPOINT
# ============================================================

@app.get("/api/summary")
def summary():

    try:

        forecast = load_csv(
            FORECAST_OUTPUT_DIR,
            "daily_forecast_summary.csv"
        )

        improvement = load_csv(
            EVALUATION_OUTPUT_DIR,
            "model_improvement_comparison.csv"
        )

        clustering = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "store_item_demand_segments.csv"
        )

        # ----------------------------------------------------
        # FINAL MODEL
        # ----------------------------------------------------

        if len(improvement) < 2:

            raise ValueError(
                "File model_improvement_comparison.csv "
                "tidak memiliki baris model final."
            )

        final_model = improvement.iloc[1]

        # ----------------------------------------------------
        # TOTAL SALES
        # ----------------------------------------------------

        total_actual_sales = (
            forecast["actual_sales"]
            .sum()
        )

        # ----------------------------------------------------
        # TOTAL STORE ITEMS
        # ----------------------------------------------------

        total_store_items = (
            clustering[
                [
                    "store_id",
                    "item_id"
                ]
            ]
            .drop_duplicates()
            .shape[0]
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return {

            "total_actual_sales": float(
                total_actual_sales
            ),

            "test_mae": float(
                final_model["test_mae"]
            ),

            "test_rmse": float(
                final_model["test_rmse"]
            ),

            "test_wape": float(
                final_model["test_wape"]
            ),

            "model": str(
                final_model["model"]
            ),

            "total_store_items": int(
                total_store_items
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# FORECAST ENDPOINT
# ============================================================

@app.get("/api/forecast")
def forecast():

    try:

        data = load_csv(
            FORECAST_OUTPUT_DIR,
            "daily_forecast_summary.csv"
        )

        # ----------------------------------------------------
        # DATE FORMAT
        # ----------------------------------------------------

        if "date" in data.columns:

            data["date"] = (
                pd.to_datetime(
                    data["date"]
                )
                .dt.strftime("%Y-%m-%d")
            )

        return {

            "count": len(data),

            "data": data.to_dict(
                orient="records"
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# INVENTORY ENDPOINT
# ============================================================

@app.get("/api/inventory")
def inventory():

    try:

        data = load_csv(
            OPTIMIZATION_OUTPUT_DIR,
            "inventory_recommendations.csv"
        )

        return {

            "count": len(data),

            "data": data.to_dict(
                orient="records"
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# DEMAND SEGMENTS ENDPOINT
# ============================================================

@app.get("/api/segments")
def segments():

    try:

        data = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "store_item_demand_segments.csv"
        )

        return {

            "count": len(data),

            "data": data.to_dict(
                orient="records"
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# SEGMENT SUMMARY ENDPOINT
# ============================================================

@app.get("/api/segment-summary")
def segment_summary():

    try:

        data = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "demand_segment_summary.csv"
        )

        return {

            "count": len(data),

            "data": data.to_dict(
                orient="records"
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# STOCK RECOMMENDATIONS
# ============================================================

@app.get("/api/recommendations")
def recommendations(
    limit: int = 20
):

    try:

        # ====================================================
        # LOAD INVENTORY
        # ====================================================

        inventory = load_csv(
            OPTIMIZATION_OUTPUT_DIR,
            "inventory_recommendations.csv"
        )

        # ====================================================
        # LOAD CLUSTERING
        # ====================================================

        clustering = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "store_item_demand_segments.csv"
        )

        # ====================================================
        # VALIDATE INVENTORY COLUMNS
        # ====================================================

        inventory_required = [

            "store_id",
            "item_id",
            "avg_forecast_demand",
            "demand_std",
            "demand_buffer",
            "recommended_stock",
            "demand_category",

        ]

        missing_inventory = [

            column

            for column in inventory_required

            if column not in inventory.columns

        ]

        if missing_inventory:

            raise ValueError(
                "Kolom inventory tidak ditemukan: "
                f"{missing_inventory}"
            )

        # ====================================================
        # VALIDATE CLUSTERING COLUMNS
        # ====================================================

        clustering_required = [

            "store_id",
            "item_id",
            "demand_segment",
            "forecast_error",
            "absolute_forecast_error",

        ]

        missing_clustering = [

            column

            for column in clustering_required

            if column not in clustering.columns

        ]

        if missing_clustering:

            raise ValueError(
                "Kolom clustering tidak ditemukan: "
                f"{missing_clustering}"
            )

        # ====================================================
        # SELECT CLUSTERING DATA
        # ====================================================

        clustering_data = clustering[
            [
                "store_id",
                "item_id",
                "demand_segment",
                "forecast_error",
                "absolute_forecast_error",
            ]
        ].copy()

        # ====================================================
        # MERGE
        # ====================================================

        data = inventory.merge(

            clustering_data,

            on=[
                "store_id",
                "item_id"
            ],

            how="left",

        )

        # ====================================================
        # NUMERIC CONVERSION
        # ====================================================

        numeric_columns = [

            "avg_forecast_demand",
            "demand_std",
            "demand_buffer",
            "recommended_stock",
            "forecast_error",
            "absolute_forecast_error",

        ]

        for column in numeric_columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

        # ====================================================
        # NORMALIZATION
        # ====================================================

        def normalize(series):

            minimum = series.min()
            maximum = series.max()

            if (
                pd.isna(minimum)
                or pd.isna(maximum)
            ):

                return pd.Series(
                    0.0,
                    index=series.index
                )

            if maximum == minimum:

                return pd.Series(
                    0.0,
                    index=series.index
                )

            return (
                (series - minimum)
                / (maximum - minimum)
            )

        # ====================================================
        # SCORE FEATURES
        # ====================================================

        data["error_score"] = normalize(
            data[
                "absolute_forecast_error"
            ]
        )

        data["variability_score"] = normalize(
            data[
                "demand_std"
            ]
        )

        data["stock_score"] = normalize(
            data[
                "recommended_stock"
            ]
        )

        # ====================================================
        # SEGMENT SCORE
        # ====================================================

        segment_score_map = {

            "Tinggi": 1.00,
            "Sedang": 0.60,
            "Rendah": 0.30,

            "High": 1.00,
            "Medium": 0.60,
            "Low": 0.30,

        }

        data["segment_score"] = (

            data[
                "demand_segment"
            ]

            .map(
                segment_score_map
            )

            .fillna(

                data[
                    "demand_category"
                ]
                .map(
                    segment_score_map
                )

            )

            .fillna(0.30)

        )

        # ====================================================
        # PRIORITY SCORE
        # ====================================================

        data["priority_score"] = (

            (
                data["segment_score"]
                * 0.40
            )

            +

            (
                data["error_score"]
                * 0.30
            )

            +

            (
                data["variability_score"]
                * 0.20
            )

            +

            (
                data["stock_score"]
                * 0.10
            )

        ) * 100

        data["priority_score"] = (

            data[
                "priority_score"
            ]
            .round(2)

        )

        # ====================================================
        # PRIORITY LEVEL
        # ====================================================

        def determine_priority(
            score
        ):

            if score >= 70:

                return "Tinggi"

            elif score >= 40:

                return "Sedang"

            else:

                return "Rendah"

        data["priority"] = (

            data[
                "priority_score"
            ]
            .apply(
                determine_priority
            )

        )

        # ====================================================
        # PRIORITY RANK
        # ====================================================

        priority_order = {

            "Tinggi": 3,
            "Sedang": 2,
            "Rendah": 1,

        }

        data["priority_rank"] = (

            data[
                "priority"
            ]
            .map(
                priority_order
            )
            .fillna(0)

        )

        # ====================================================
        # SORT
        # ====================================================

        data = data.sort_values(

            by=[

                "priority_rank",
                "priority_score",
                "recommended_stock",

            ],

            ascending=False

        )

        # ====================================================
        # LIMIT
        # ====================================================

        limit = max(
            1,
            min(limit, 100)
        )

        result = data.head(
            limit
        ).copy()

        # ====================================================
        # OUTPUT COLUMNS
        # ====================================================

        output_columns = [

            "store_id",
            "item_id",
            "demand_segment",
            "priority",
            "priority_score",
            "avg_forecast_demand",
            "demand_std",
            "forecast_error",
            "absolute_forecast_error",
            "demand_buffer",
            "recommended_stock",

        ]

        result = result[

            [
                column

                for column in output_columns

                if column in result.columns

            ]

        ]

        # ====================================================
        # NaN -> None
        # ====================================================

        result = result.where(
            pd.notna(result),
            None
        )

        # ====================================================
        # RESPONSE
        # ====================================================

        return {

            "count": len(result),

            "total_items": len(data),

            "data": result.to_dict(
                orient="records"
            ),

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# AI ANALYSIS ENDPOINT
# ============================================================

@app.get("/api/ai-analysis")
def ai_analysis(
    limit: int = 5
):

    try:

        # ====================================================
        # LOAD DATA
        # ====================================================

        inventory = load_csv(
            OPTIMIZATION_OUTPUT_DIR,
            "inventory_recommendations.csv"
        )

        clustering = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "store_item_demand_segments.csv"
        )

        # ====================================================
        # MERGE DATA
        # ====================================================

        cluster_data = clustering[
            [
                "store_id",
                "item_id",
                "demand_segment",
                "average_demand",
                "demand_variability",
                "coefficient_of_variation",
                "forecast_error",
                "absolute_forecast_error",
                "forecast_demand",
            ]
        ].copy()

        data = inventory.merge(

            cluster_data,

            on=[
                "store_id",
                "item_id"
            ],

            how="left",

            suffixes=(
                "_inventory",
                "_cluster"
            )

        )

        # ====================================================
        # NUMERIC CONVERSION
        # ====================================================

        numeric_columns = [

            "average_demand",
            "demand_variability",
            "coefficient_of_variation",
            "forecast_error",
            "absolute_forecast_error",
            "forecast_demand",
            "recommended_stock",

        ]

        for column in numeric_columns:

            if column in data.columns:

                data[column] = pd.to_numeric(
                    data[column],
                    errors="coerce"
                )

        # ====================================================
        # TOP ERROR
        # ====================================================

        top_error = (

            data.sort_values(
                "absolute_forecast_error",
                ascending=False
            )

            .head(limit)

        )

        # ====================================================
        # SEGMENT SUMMARY
        # ====================================================

        segment_summary = (

            data.groupby(
                "demand_segment"
            )

            .agg(

                store_item_count=(
                    "item_id",
                    "count"
                ),

                average_demand=(
                    "average_demand",
                    "mean"
                ),

                demand_variability=(
                    "demand_variability",
                    "mean"
                ),

                forecast_error=(
                    "forecast_error",
                    "mean"
                ),

                recommended_stock=(
                    "recommended_stock",
                    "mean"
                ),

            )

            .reset_index()

        )

        # ====================================================
        # OVERALL METRICS
        # ====================================================

        total_items = len(data)

        average_demand = (
            data[
                "average_demand"
            ].mean()
        )

        average_variability = (
            data[
                "demand_variability"
            ].mean()
        )

        average_forecast_error = (
            data[
                "forecast_error"
            ].mean()
        )

        average_absolute_error = (
            data[
                "absolute_forecast_error"
            ].mean()
        )

        average_recommended_stock = (
            data[
                "recommended_stock"
            ].mean()
        )

        # ====================================================
        # BUSINESS INSIGHTS
        # ====================================================

        insights = []

        # ----------------------------------------------------
        # DEMAND
        # ----------------------------------------------------

        if average_demand > 30:

            insights.append(
                "Permintaan rata-rata berada pada "
                "tingkat tinggi sehingga pengelolaan "
                "persediaan perlu mendapat perhatian."
            )

        elif average_demand > 20:

            insights.append(
                "Permintaan rata-rata berada pada "
                "tingkat sedang."
            )

        else:

            insights.append(
                "Permintaan rata-rata relatif rendah."
            )

        # ----------------------------------------------------
        # VARIABILITY
        # ----------------------------------------------------

        if average_variability > 8:

            insights.append(
                "Variabilitas permintaan relatif tinggi, "
                "sehingga kebutuhan stok pengaman perlu "
                "diperhatikan."
            )

        else:

            insights.append(
                "Variabilitas permintaan relatif terkendali."
            )

        # ----------------------------------------------------
        # FORECAST ERROR
        # ----------------------------------------------------

        if average_absolute_error > 10:

            insights.append(
                "Absolute forecast error relatif tinggi. "
                "Beberapa store-item perlu mendapat "
                "perhatian lebih dalam perencanaan stok."
            )

        else:

            insights.append(
                "Absolute forecast error secara umum "
                "masih relatif terkendali."
            )

        # ----------------------------------------------------
        # STOCK
        # ----------------------------------------------------

        insights.append(

            f"Rata-rata stok yang direkomendasikan "
            f"adalah sekitar "
            f"{average_recommended_stock:.0f} unit "
            f"per store-item."

        )

        # ====================================================
        # TOP RISK ITEMS
        # ====================================================

        top_risk_items = []

        for _, row in top_error.iterrows():

            top_risk_items.append({

                "store_id":
                    row["store_id"],

                "item_id":
                    row["item_id"],

                "segment":
                    row["demand_segment"],

                "forecast_error": (

                    None

                    if pd.isna(
                        row[
                            "forecast_error"
                        ]
                    )

                    else round(
                        float(
                            row[
                                "forecast_error"
                            ]
                        ),
                        2
                    )

                ),

                "absolute_forecast_error": (

                    None

                    if pd.isna(
                        row[
                            "absolute_forecast_error"
                        ]
                    )

                    else round(
                        float(
                            row[
                                "absolute_forecast_error"
                            ]
                        ),
                        2
                    )

                ),

                "recommended_stock": (

                    None

                    if pd.isna(
                        row[
                            "recommended_stock"
                        ]
                    )

                    else round(
                        float(
                            row[
                                "recommended_stock"
                            ]
                        ),
                        0
                    )

                ),

            })

        # ====================================================
        # RESPONSE
        # ====================================================

        return {

            "analysis": {

                "total_store_items":
                    int(total_items),

                "average_demand":
                    round(
                        float(
                            average_demand
                        ),
                        2
                    ),

                "average_demand_variability":
                    round(
                        float(
                            average_variability
                        ),
                        2
                    ),

                "average_forecast_error":
                    round(
                        float(
                            average_forecast_error
                        ),
                        2
                    ),

                "average_absolute_forecast_error":
                    round(
                        float(
                            average_absolute_error
                        ),
                        2
                    ),

                "average_recommended_stock":
                    round(
                        float(
                            average_recommended_stock
                        ),
                        2
                    ),

            },

            "insights":
                insights,

            "segment_summary": (

                segment_summary

                .where(
                    pd.notna(
                        segment_summary
                    ),
                    None
                )

                .to_dict(
                    orient="records"
                )

            ),

            "top_risk_items":
                top_risk_items,

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# STORE-ITEM ANALYSIS
# ============================================================

@app.post("/api/analyze")
def analyze_store_item(
    request: AnalyzeRequest
):

    # ========================================================
    # GET REQUEST BODY
    # ========================================================

    store_id = request.store_id
    item_id = request.item_id

    try:

        # ====================================================
        # LOAD INVENTORY
        # ====================================================

        inventory = load_csv(
            OPTIMIZATION_OUTPUT_DIR,
            "inventory_recommendations.csv"
        )

        # ====================================================
        # LOAD CLUSTERING
        # ====================================================

        clustering = load_csv(
            CLUSTERING_OUTPUT_DIR,
            "store_item_demand_segments.csv"
        )

        # ====================================================
        # FILTER STORE + ITEM
        # ====================================================

        inventory_result = inventory[

            (inventory["store_id"] == store_id)

            &

            (inventory["item_id"] == item_id)

        ].copy()

        clustering_result = clustering[

            (clustering["store_id"] == store_id)

            &

            (clustering["item_id"] == item_id)

        ].copy()

        # ====================================================
        # VALIDATE
        # ====================================================

        if inventory_result.empty:

            raise HTTPException(

                status_code=404,

                detail=(
                    f"Store-item tidak ditemukan: "
                    f"{store_id} / {item_id}"
                )

            )

        # ====================================================
        # INVENTORY ROW
        # ====================================================

        inventory_row = (
            inventory_result.iloc[0]
        )

        # ====================================================
        # CLUSTER ROW
        # ====================================================

        clustering_row = (

            clustering_result.iloc[0]

            if not clustering_result.empty

            else None

        )

        # ====================================================
        # NUMBER HELPER
        # ====================================================

        def number(
            value,
            digits=2
        ):

            if pd.isna(value):

                return None

            return round(
                float(value),
                digits
            )

        # ====================================================
        # BASE RESPONSE
        # ====================================================

        result = {

            "store_id":
                store_id,

            "item_id":
                item_id,

            "inventory": {

                "avg_forecast_demand":
                    number(
                        inventory_row[
                            "avg_forecast_demand"
                        ]
                    ),

                "max_forecast_demand":
                    number(
                        inventory_row[
                            "max_forecast_demand"
                        ]
                    ),

                "demand_std":
                    number(
                        inventory_row[
                            "demand_std"
                        ]
                    ),

                "demand_buffer":
                    number(
                        inventory_row[
                            "demand_buffer"
                        ]
                    ),

                "recommended_stock":
                    number(
                        inventory_row[
                            "recommended_stock"
                        ],
                        0
                    ),

                "demand_category":
                    str(
                        inventory_row[
                            "demand_category"
                        ]
                    ),

            },

            "segmentation":
                None,

        }

        # ====================================================
        # SEGMENTATION
        # ====================================================

        if clustering_row is not None:

            result["segmentation"] = {

                "cluster_k3":
                    int(
                        clustering_row[
                            "cluster_k3"
                        ]
                    ),

                "demand_segment":
                    str(
                        clustering_row[
                            "demand_segment"
                        ]
                    ),

                "average_demand":
                    number(
                        clustering_row[
                            "average_demand"
                        ]
                    ),

                "demand_variability":
                    number(
                        clustering_row[
                            "demand_variability"
                        ]
                    ),

                "coefficient_of_variation":
                    number(
                        clustering_row[
                            "coefficient_of_variation"
                        ]
                    ),

                "forecast_error":
                    number(
                        clustering_row[
                            "forecast_error"
                        ]
                    ),

                "absolute_forecast_error":
                    number(
                        clustering_row[
                            "absolute_forecast_error"
                        ]
                    ),

                "forecast_demand":
                    number(
                        clustering_row[
                            "forecast_demand"
                        ]
                    ),

            }

        # ====================================================
        # BUSINESS RECOMMENDATION
        # ====================================================

        category = str(
            inventory_row[
                "demand_category"
            ]
        )

        recommended_stock = number(

            inventory_row[
                "recommended_stock"
            ],

            0

        )

        if category.lower() == "high":

            recommendation = (
                "Prioritas tinggi. "
                "Store-item memiliki permintaan tinggi "
                "dan perlu mendapat perhatian dalam "
                "perencanaan persediaan."
            )

        elif category.lower() == "medium":

            recommendation = (
                "Prioritas sedang. "
                "Persediaan perlu dipantau secara berkala "
                "berdasarkan perkembangan permintaan."
            )

        else:

            recommendation = (
                "Prioritas rendah. "
                "Persediaan relatif tidak membutuhkan "
                "perhatian khusus dalam jangka pendek."
            )

        result[
            "business_recommendation"
        ] = {

            "priority":
                category,

            "recommended_stock":
                recommended_stock,

            "message":
                recommendation,

        }

        return result

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )