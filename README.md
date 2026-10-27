# Retail Demand Forecasting & Inventory Optimization

A retail demand analytics project that transforms daily store-item sales into demand forecasts, demand segments, and inventory recommendations using time-based feature engineering, HistGradientBoosting, and an interactive Laravel dashboard.

## Overview

This project was created to understand retail demand patterns, improve store-item sales forecasts, and help prioritize inventory planning across stores and products.

The main workflow is:

`Retail Sales Data -> Data Understanding -> Data Cleaning -> Feature Engineering -> Baseline Forecasting -> Lag-Feature Model Improvement -> Demand Segmentation -> Inventory Optimization -> FastAPI -> Laravel Dashboard`

The data analysis and forecasting pipeline remains in Python. FastAPI exposes the existing analysis outputs, while Laravel provides the dashboard interface. Laravel does not retrain models or replace the forecasting API.

## Project Goals

- Explore sales trends across dates, stores, and items.
- Understand weekly and monthly demand patterns, promotions, and price behavior.
- Compare a baseline forecasting model with an improved model using lag features.
- Group store-item combinations into business-oriented demand segments.
- Recommend stock levels and identify high-priority inventory items.
- Present forecasts and business insights in an accessible dashboard.

## Model Results

The saved model comparison reports the following test-set results:

| Model | MAE | RMSE | WAPE |
|---|---:|---:|---:|
| HistGradientBoosting | 8.98 | 11.07 | 33.86% |
| HistGradientBoosting + Lag Features | **2.97** | **3.74** | **11.20%** |

Compared with the baseline, the lag-feature model reduced MAE by approximately **66.93%**, RMSE by **66.18%**, and WAPE by **66.93%**.

## Demand and Inventory Insights

- Historical daily demand shows recurring weekly and yearly patterns.
- Demand varies between store-item combinations, making segmentation useful for inventory planning.
- The project produces low, medium, and high demand segments.
- Inventory recommendations combine forecast demand with a demand buffer.
- The API ranks recommendations so high-priority store-items are easier to review.

## Dashboard

The Laravel dashboard includes:

- **Overview** - sales, model accuracy, recommended stock, forecasts, and segment distribution.
- **Forecast** - daily actual-versus-predicted sales and date filtering.
- **Inventory Analysis** - detailed analysis for an individual store-item combination.
- **Demand Segmentation** - segment summary and store-item assignments.
- **Recommendations** - prioritized stock recommendations.
- **AI Analysis** - API-generated insights and store-items with the highest forecast error.
- **System Health** - status and record counts from FastAPI.

The dashboard is responsive and uses Chart.js for browser-based visualizations. Laravel is only the presentation layer; demand analysis, forecast outputs, models, and API responses continue to come from the existing Python project.

## Technology Stack

- **Python** - data analysis, feature engineering, forecasting, segmentation, and inventory optimization.
- **Pandas** - data preparation and analysis.
- **Scikit-learn** - HistGradientBoosting and clustering workflows in the notebooks.
- **Jupyter Notebook** - exploration, cleaning, modeling, and optimization workflow.
- **FastAPI** - API for exposing analysis outputs.
- **Laravel 12 / PHP 8.3** - dashboard interface.
- **Docker Compose** - running the Laravel dashboard.
- **Chart.js** - dashboard charts.

## Repository Structure

```text
ForecastOpti/
|-- data/
|   |-- raw/                  # Source dataset (not included in Git)
|   +-- processed/            # Processed data
|-- figures/
|   |-- eda/                  # Exploratory analysis charts
|   |-- forecasting/          # Forecast charts
|   +-- optimization/         # Inventory optimization charts
|-- models/                   # Saved forecasting models
|-- notebooks/
|   |-- 01_setup.ipynb
|   |-- 02_data_understanding.ipynb
|   |-- 03_data_cleaning.ipynb
|   |-- 04_model_improvement.ipynb
|   +-- 05_optimization.ipynb
|-- outputs/
|   |-- clustering/           # Demand segments and cluster summaries
|   |-- evaluation/           # Model evaluation results
|   |-- forecasts/            # Forecast results
|   +-- optimization/         # Inventory recommendations
|-- src/
|   |-- api/main.py           # FastAPI application
|   |-- config.py             # Project paths and output locations
|   +-- dashboard.py          # Original Streamlit dashboard
|-- laravel-dashboard/        # Laravel dashboard and Docker setup
|-- requirements.txt
+-- README.md
```

## Data

The Python analysis expects the raw dataset at:

```text
data/raw/retail_sales.csv
```

The source dataset is excluded from Git. Add your authorized dataset locally before running notebooks or regenerating analysis outputs. The expected columns include:

| Column | Description |
|---|---|
| `date` | Sales date |
| `store_id` | Store identifier |
| `item_id` | Product identifier |
| `sales` | Daily units sold |
| `price` | Product price |
| `promo` | Promotion indicator |
| `weekday` | Day-of-week feature |
| `month` | Month feature |

Forecast, evaluation, segmentation, and inventory output files are stored under `outputs/`. The FastAPI service reads these files to serve dashboard data.

## Running the Project

### 1. Start the FastAPI backend

From the project root, create a Python environment and install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run FastAPI so it can be reached from the Laravel Docker container:

```powershell
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Keep this terminal open while using the dashboard. Verify the service at:

- Health check: <http://localhost:8000/api/health>
- Interactive API documentation: <http://localhost:8000/docs>

### 2. Start the Laravel dashboard

In a second terminal, start Docker Compose:

```powershell
Set-Location laravel-dashboard
docker compose up --build
```

Open the dashboard at <http://localhost:8080>.

By default, the Laravel container connects to FastAPI at `http://host.docker.internal:8000`. If FastAPI is running at another address or port, configure it before starting Compose:

```powershell
$env:FORECASTOPTI_API_URL = "http://host.docker.internal:8000"
$env:FORECASTOPTI_API_TIMEOUT = "15"
docker compose up --build
```

Set `FORECASTOPTI_API_URL` to an address that is reachable from inside the dashboard container. Both FastAPI and the Laravel container must be running to display live data.

Stop the dashboard with `Ctrl+C`, or run `docker compose down` from `laravel-dashboard`.

### 3. Regenerate analysis outputs

The notebooks document the project's analysis stages:

1. `01_setup.ipynb` - initialize project paths and folders.
2. `02_data_understanding.ipynb` - inspect sales data and demand patterns.
3. `03_data_cleaning.ipynb` - validate and prepare the dataset.
4. `04_model_improvement.ipynb` - train and evaluate forecasting models.
5. `05_optimization.ipynb` - create demand segments and inventory recommendations.

Run the notebooks in order when you need to reproduce the pipeline outputs. They were originally configured for Google Colab, so review their project path and environment setup when running them locally.

## FastAPI Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | API service information |
| `GET` | `/api/health` | Service status and output record counts |
| `GET` | `/api/summary` | Forecast evaluation metrics and project summary |
| `GET` | `/api/forecast` | Daily aggregate actual and predicted sales |
| `GET` | `/api/inventory` | Inventory recommendation records |
| `GET` | `/api/segments` | Store-item demand segment records |
| `GET` | `/api/segment-summary` | Aggregated demand segment metrics |
| `GET` | `/api/recommendations?limit=20` | Recommendations ordered by priority |
| `GET` | `/api/ai-analysis?limit=5` | Business insights and high-error items |
| `POST` | `/api/analyze` | Analysis for a selected store and item |

The interactive API documentation is available at `/docs` while FastAPI is running.

## Testing

Run the Laravel feature tests from the dashboard directory:

```powershell
Set-Location laravel-dashboard
php artisan test
```

Check PHP formatting with:

```powershell
vendor\bin\pint --test app tests routes config
```

The dashboard tests cover API requests, store-item analysis, forecast display, and API error handling.

## Notes

- `/api/forecast` currently returns daily aggregate forecasts. The Laravel dashboard displays this API data as provided and does not load the saved `.pkl` model files or calculate new predictions.
- The Chart.js library is loaded from jsDelivr, so the browser needs internet access to render charts.
- Laravel's encryption key is persisted in the Docker Compose storage volume.
