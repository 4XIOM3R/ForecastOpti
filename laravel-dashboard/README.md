# ForecastOpti Laravel Dashboard

This Laravel application replaces only the Streamlit presentation layer. Forecasting, inventory optimization, segmentation, stored models, and the FastAPI service remain in the existing Python project.

## Run with Docker

1. Start the existing FastAPI service from the repository root:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```

2. In another terminal, build and start the Laravel dashboard:

   ```powershell
   Set-Location laravel-dashboard
   docker compose up --build
   ```

3. Open <http://localhost:8080>.

The Laravel container calls FastAPI at `http://host.docker.internal:8000`. To use another API address, set `FORECASTOPTI_API_URL` before starting Compose. The API is intentionally not reimplemented or included as a second service in this Compose file.

The generated Laravel encryption key is stored in the Compose `dashboard_storage` volume and reused after container restarts.

## Pages

- Overview: project KPIs, daily aggregate forecast, segment summary, and inventory highlights.
- Forecast: actual-versus-predicted daily demand and date filtering.
- Inventory Analysis: store-item details through the existing `/api/analyze` endpoint.
- Demand Segmentation: segment aggregates and store-item assignments.
- Recommendations: prioritized stock recommendations.
- AI Analysis: insights and highest-error items.
- System Health: the existing FastAPI health response.

Charts load Chart.js from jsDelivr. The dashboard requires browser access to that CDN for charts; the tables and other page content are rendered by Laravel.

The current FastAPI forecast endpoint provides daily aggregate forecasts, so the Laravel forecast page uses that same aggregate data rather than changing the API contract or reading model files directly.
