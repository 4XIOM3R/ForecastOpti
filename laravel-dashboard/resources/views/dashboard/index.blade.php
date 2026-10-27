@extends('layouts.app')

@section('content')
@php
    $forecastRows = data_get($data, 'forecast.data', data_get($data, 'data', []));
    $inventoryRows = data_get($data, 'inventory.data', []);
    $segmentRows = data_get($data, 'segments.data', []);
    $segmentSummary = data_get($data, 'segment_summary.data', data_get($data, 'summary.data', []));
    $recommendationRows = data_get($data, 'data', []);
    $formatNumber = fn ($value, $decimals = 0) => is_numeric($value)
        ? number_format((float) $value, $decimals)
        : '—';
@endphp

@if($page === 'overview')
    @php
        $summary = data_get($data, 'summary', []);
        $stockTotal = collect($inventoryRows)->sum(fn ($row) => (float) ($row['recommended_stock'] ?? 0));
        $chartForecast = collect($forecastRows)->sortBy('date')->values();
        $segmentLabels = collect($segmentSummary)->pluck('business_level')->values();
        $segmentCounts = collect($segmentSummary)->pluck('store_item_count')->values();
        $topStock = collect($inventoryRows)->sortByDesc('recommended_stock')->take(10)->values();
    @endphp
    <section class="banner">
        <h2>Your demand, at a glance</h2>
        <p>Monitor demand forecasts, evaluate model performance, and review inventory recommendations. All figures come from the existing ForecastOpti API.</p>
    </section>
    <section class="grid kpis">
        <article class="kpi"><div class="kpi-label">Actual Sales</div><div class="kpi-value">{{ $formatNumber($summary['total_actual_sales'] ?? null) }}</div><div class="kpi-note">Total actual sales in the forecast dataset</div></article>
        <article class="kpi"><div class="kpi-label">Forecast WAPE</div><div class="kpi-value">{{ $formatNumber($summary['test_wape'] ?? null, 2) }}%</div><div class="kpi-note">Final model test performance</div></article>
        <article class="kpi"><div class="kpi-label">Recommended Stock</div><div class="kpi-value">{{ $formatNumber($stockTotal) }}</div><div class="kpi-note">Total recommended units across store-items</div></article>
        <article class="kpi"><div class="kpi-label">Store-Items</div><div class="kpi-value">{{ $formatNumber($summary['total_store_items'] ?? null) }}</div><div class="kpi-note">Unique store and product combinations</div></article>
    </section>
    <div class="grid two">
        <section class="card">
            <div class="card-heading"><div><h2>Daily demand forecast</h2><p class="card-description">Actual sales compared with predicted sales</p></div></div>
            <div class="chart-wrap">
                @if($chartForecast->isNotEmpty())
                    <canvas id="overviewForecast" aria-label="Daily actual and predicted sales" role="img"></canvas>
                @else
                    <div class="chart-empty"><strong>No forecast data available</strong><span>Check the forecast API response and try again.</span></div>
                @endif
            </div>
        </section>
        <section class="card">
            <div class="card-heading"><div><h2>Demand segments</h2><p class="card-description">Store-item distribution by business demand level</p></div></div>
            <div class="chart-wrap">
                @if($segmentLabels->isNotEmpty())
                    <canvas id="overviewSegments" aria-label="Number of store items in each demand segment" role="img"></canvas>
                @else
                    <div class="chart-empty"><strong>No segment data available</strong><span>Segment data will appear here when available.</span></div>
                @endif
            </div>
        </section>
    </div>
    <section class="grid three">
        <article class="kpi"><div class="kpi-label">MAE</div><div class="kpi-value">{{ $formatNumber($summary['test_mae'] ?? null, 2) }}</div><div class="kpi-note">Mean absolute error</div></article>
        <article class="kpi"><div class="kpi-label">RMSE</div><div class="kpi-value">{{ $formatNumber($summary['test_rmse'] ?? null, 2) }}</div><div class="kpi-note">Root mean squared error</div></article>
        <article class="kpi"><div class="kpi-label">Final model</div><div class="kpi-value" style="font-size:18px">{{ $summary['model'] ?? '—' }}</div><div class="kpi-note">Forecasting model currently evaluated</div></article>
    </section>
    <h2 class="section-title">Highest recommended stock</h2>
    <section class="card table-wrap">
        <table>
            <thead><tr><th>Store</th><th>Item</th><th>Demand category</th><th>Average forecast</th><th>Recommended stock</th></tr></thead>
            <tbody>
            @forelse($topStock as $row)
                <tr><td>{{ $row['store_id'] ?? '—' }}</td><td>{{ $row['item_id'] ?? '—' }}</td><td><span class="badge {{ strtolower($row['demand_category'] ?? '') }}">{{ $row['demand_category'] ?? '—' }}</span></td><td>{{ $formatNumber($row['avg_forecast_demand'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null) }}</td></tr>
            @empty
                <tr><td colspan="5" class="muted">No inventory records returned by the API.</td></tr>
            @endforelse
            </tbody>
        </table>
    </section>
@elseif($page === 'forecast')
    @php
        $chartForecast = collect($forecastRows)->sortBy('date')->values();
        $actualTotal = collect($forecastRows)->sum(fn ($row) => (float) ($row['actual_sales'] ?? 0));
        $predictedTotal = collect($forecastRows)->sum(fn ($row) => (float) ($row['predicted_sales'] ?? 0));
    @endphp
    <section class="card">
        <div class="card-heading"><div><h2>Forecast analysis</h2><p class="card-description">Daily actual and predicted sales, provided by <code>/api/forecast</code>.</p></div></div>
        <form class="form-row" method="get" action="{{ route('dashboard.page', ['page' => 'forecast']) }}">
            <div class="field"><label for="start_date">From</label><input id="start_date" name="start_date" type="date" value="{{ $filters['start_date'] ?? '' }}"></div>
            <div class="field"><label for="end_date">To</label><input id="end_date" name="end_date" type="date" value="{{ $filters['end_date'] ?? '' }}"></div>
            <button type="submit">Apply dates</button>
            <a class="button secondary" href="{{ route('dashboard.page', ['page' => 'forecast']) }}">Reset</a>
        </form>
    </section>
    <section class="grid kpis">
        <article class="kpi"><div class="kpi-label">Actual Demand</div><div class="kpi-value">{{ $formatNumber($actualTotal) }}</div><div class="kpi-note">{{ count($forecastRows) }} daily records in selected range</div></article>
        <article class="kpi"><div class="kpi-label">Forecast Demand</div><div class="kpi-value">{{ $formatNumber($predictedTotal) }}</div><div class="kpi-note">Predicted demand in selected range</div></article>
        <article class="kpi"><div class="kpi-label">Difference</div><div class="kpi-value">{{ $formatNumber($actualTotal - $predictedTotal) }}</div><div class="kpi-note">Actual demand minus forecast</div></article>
        <article class="kpi"><div class="kpi-label">Records</div><div class="kpi-value">{{ count($forecastRows) }}</div><div class="kpi-note">Rows returned by the API</div></article>
    </section>
    <section class="card">
        <div class="card-heading"><div><h2>Actual vs forecast</h2><p class="card-description">Daily aggregated sales over time</p></div></div>
        <div class="chart-wrap">
            @if($chartForecast->isNotEmpty())
                <canvas id="forecastChart" aria-label="Daily actual and predicted sales" role="img"></canvas>
            @else
                <div class="chart-empty"><strong>No forecast data in this date range</strong><span>Choose another date range or reset the filters.</span></div>
            @endif
        </div>
    </section>
    <section class="card table-wrap">
        <div class="card-heading"><div><h2>Forecast records</h2><p class="card-description">Daily output from the existing API</p></div></div>
        <table><thead><tr><th>Date</th><th>Actual sales</th><th>Predicted sales</th><th>Difference</th></tr></thead><tbody>
        @forelse(collect($forecastRows)->sortByDesc('date') as $row)
            <tr><td>{{ $row['date'] ?? '—' }}</td><td>{{ $formatNumber($row['actual_sales'] ?? null) }}</td><td>{{ $formatNumber($row['predicted_sales'] ?? null) }}</td><td>{{ $formatNumber((float) ($row['actual_sales'] ?? 0) - (float) ($row['predicted_sales'] ?? 0)) }}</td></tr>
        @empty
            <tr><td colspan="4" class="muted">No forecast records match the selected dates.</td></tr>
        @endforelse
        </tbody></table>
    </section>
@elseif($page === 'inventory-analysis')
    @php
        $selectedStore = $filters['store'] ?? '';
        $stores = collect($segmentRows)->pluck('store_id')->filter()->unique()->sort()->values();
        $storeItems = collect($segmentRows)->where('store_id', $selectedStore);
        $items = $selectedStore !== '' ? $storeItems->pluck('item_id')->filter()->unique()->sort()->values() : collect();
        $analysis = $data['analysis'] ?? null;
        $stockRows = collect($inventoryRows)->where('store_id', $selectedStore)->sortByDesc('recommended_stock')->take(8);
    @endphp
    <section class="card">
        <div class="card-heading"><div><h2>Store-item inventory profile</h2><p class="card-description">Choose a store and item to request detailed analysis from the existing <code>/api/analyze</code> endpoint.</p></div></div>
        <form class="form-row" method="get" action="{{ route('dashboard.page', ['page' => 'inventory-analysis']) }}">
            <div class="field"><label for="store">Store</label><select id="store" name="store" required onchange="this.form.submit()"><option value="">Select a store</option>@foreach($stores as $store)<option value="{{ $store }}" @selected($selectedStore === $store)>{{ $store }}</option>@endforeach</select></div>
            <div class="field"><label for="item">Item</label><select id="item" name="item" required><option value="">Select an item</option>@foreach($items as $item)<option value="{{ $item }}" @selected(($filters['item'] ?? '') === $item)>{{ $item }}</option>@endforeach</select></div>
            <button type="submit">View profile</button>
        </form>
    </section>
    @if($analysis)
        @php
            $stock = $analysis['inventory'] ?? [];
            $segment = $analysis['segmentation'] ?? [];
        @endphp
        <section class="grid kpis">
            <article class="kpi"><div class="kpi-label">Average Forecast</div><div class="kpi-value">{{ $formatNumber($stock['avg_forecast_demand'] ?? null, 2) }}</div><div class="kpi-note">Units per forecast period</div></article>
            <article class="kpi"><div class="kpi-label">Demand Variability</div><div class="kpi-value">{{ $formatNumber($stock['demand_std'] ?? null, 2) }}</div><div class="kpi-note">Standard deviation of demand</div></article>
            <article class="kpi"><div class="kpi-label">Demand Buffer</div><div class="kpi-value">{{ $formatNumber($stock['demand_buffer'] ?? null, 2) }}</div><div class="kpi-note">Safety buffer in the recommendation</div></article>
            <article class="kpi"><div class="kpi-label">Recommended Stock</div><div class="kpi-value">{{ $formatNumber($stock['recommended_stock'] ?? null) }}</div><div class="kpi-note">{{ $stock['demand_category'] ?? '—' }} demand</div></article>
        </section>
        <section class="card">
            <div class="card-heading"><div><h2>{{ $analysis['store_id'] }} · {{ $analysis['item_id'] }}</h2><p class="card-description">Detailed demand and inventory attributes</p></div></div>
            <div class="grid two">
                <div><div class="health-row"><span>Demand segment</span><strong>{{ $segment['demand_segment'] ?? '—' }}</strong></div><div class="health-row"><span>Cluster</span><strong>{{ $segment['cluster_k3'] ?? '—' }}</strong></div><div class="health-row"><span>Average demand</span><strong>{{ $formatNumber($segment['average_demand'] ?? null, 2) }}</strong></div><div class="health-row"><span>Demand variability</span><strong>{{ $formatNumber($segment['demand_variability'] ?? null, 2) }}</strong></div></div>
                <div><div class="health-row"><span>Coefficient of variation</span><strong>{{ $formatNumber($segment['coefficient_of_variation'] ?? null, 3) }}</strong></div><div class="health-row"><span>Forecast error</span><strong>{{ $formatNumber($segment['forecast_error'] ?? null, 2) }}</strong></div><div class="health-row"><span>Absolute forecast error</span><strong>{{ $formatNumber($segment['absolute_forecast_error'] ?? null, 2) }}</strong></div><div class="health-row"><span>Maximum forecast demand</span><strong>{{ $formatNumber($stock['max_forecast_demand'] ?? null, 2) }}</strong></div></div>
            </div>
        </section>
    @else
        <div class="muted" style="margin:8px 2px 20px">Choose a store and item, then select “View profile” to load the detailed analysis.</div>
    @endif
    <section class="card table-wrap">
        <div class="card-heading"><div><h2>Inventory recommendations</h2><p class="card-description">Highest suggested stock levels{{ $selectedStore ? ' for '.$selectedStore : '' }}</p></div></div>
        <table><thead><tr><th>Store</th><th>Item</th><th>Average forecast</th><th>Demand buffer</th><th>Recommended stock</th><th>Category</th></tr></thead><tbody>
        @forelse($stockRows as $row)
            <tr><td>{{ $row['store_id'] ?? '—' }}</td><td>{{ $row['item_id'] ?? '—' }}</td><td>{{ $formatNumber($row['avg_forecast_demand'] ?? null, 2) }}</td><td>{{ $formatNumber($row['demand_buffer'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null) }}</td><td><span class="badge {{ strtolower($row['demand_category'] ?? '') }}">{{ $row['demand_category'] ?? '—' }}</span></td></tr>
        @empty
            <tr><td colspan="6" class="muted">No inventory records returned for this store.</td></tr>
        @endforelse
        </tbody></table>
    </section>
@elseif($page === 'demand-segmentation')
    @php
        $segmentLabels = collect($segmentSummary)->pluck('business_level')->values();
        $segmentCounts = collect($segmentSummary)->pluck('store_item_count')->values();
    @endphp
    <section class="grid two">
        <section class="card">
            <div class="card-heading"><div><h2>Demand distribution</h2><p class="card-description">Number of store-item combinations per segment</p></div></div>
            <div class="chart-wrap">
                @if($segmentLabels->isNotEmpty())
                    <canvas id="segmentChart" aria-label="Number of store items in each demand segment" role="img"></canvas>
                @else
                    <div class="chart-empty"><strong>No segment data available</strong><span>Segment data will appear here when available.</span></div>
                @endif
            </div>
        </section>
        <section class="card table-wrap">
            <div class="card-heading"><div><h2>Segment summary</h2><p class="card-description">Aggregated demand characteristics</p></div></div>
            <table><thead><tr><th>Segment</th><th>Store-items</th><th>Average demand</th><th>Variability</th><th>Recommended stock</th></tr></thead><tbody>
            @forelse($segmentSummary as $row)
                <tr><td><span class="badge {{ strtolower($row['business_level'] ?? '') }}">{{ $row['business_level'] ?? '—' }}</span></td><td>{{ $formatNumber($row['store_item_count'] ?? null) }}</td><td>{{ $formatNumber($row['average_demand'] ?? null, 2) }}</td><td>{{ $formatNumber($row['demand_variability'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null, 2) }}</td></tr>
            @empty
                <tr><td colspan="5" class="muted">No segment summary returned.</td></tr>
            @endforelse
            </tbody></table>
        </section>
    </section>
    <section class="card table-wrap">
        <div class="card-heading"><div><h2>Store-item segments</h2><p class="card-description">Segment assignment and demand metrics</p></div></div>
        <table><thead><tr><th>Store</th><th>Item</th><th>Segment</th><th>Average demand</th><th>Demand variability</th><th>Forecast error</th><th>Recommended stock</th></tr></thead><tbody>
        @forelse(collect($segmentRows)->take(100) as $row)
            <tr><td>{{ $row['store_id'] ?? '—' }}</td><td>{{ $row['item_id'] ?? '—' }}</td><td><span class="badge {{ strtolower($row['demand_segment'] ?? '') }}">{{ $row['demand_segment'] ?? '—' }}</span></td><td>{{ $formatNumber($row['average_demand'] ?? null, 2) }}</td><td>{{ $formatNumber($row['demand_variability'] ?? null, 2) }}</td><td>{{ $formatNumber($row['forecast_error'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null) }}</td></tr>
        @empty
            <tr><td colspan="7" class="muted">No segment records returned.</td></tr>
        @endforelse
        </tbody></table>
        @if(count($segmentRows) > 100)<p class="muted" style="margin:12px 2px 0">Showing the first 100 of {{ count($segmentRows) }} records.</p>@endif
    </section>
@elseif($page === 'recommendations')
    <section class="grid kpis">
        <article class="kpi"><div class="kpi-label">Items in this view</div><div class="kpi-value">{{ count($recommendationRows) }}</div><div class="kpi-note">Highest-priority recommendations returned</div></article>
        <article class="kpi"><div class="kpi-label">Total store-items</div><div class="kpi-value">{{ $formatNumber($data['total_items'] ?? null) }}</div><div class="kpi-note">Items analyzed by the recommendation API</div></article>
    </section>
    <section class="card table-wrap">
        <div class="card-heading"><div><h2>Inventory priorities</h2><p class="card-description">Sorted by the priority score calculated by the existing API</p></div></div>
        <table><thead><tr><th>Priority</th><th>Score</th><th>Store</th><th>Item</th><th>Segment</th><th>Forecast demand</th><th>Variability</th><th>Absolute error</th><th>Recommended stock</th></tr></thead><tbody>
        @forelse($recommendationRows as $row)
            <tr><td><span class="badge {{ strtolower($row['priority'] ?? '') }}">{{ $row['priority'] ?? '—' }}</span></td><td>{{ $formatNumber($row['priority_score'] ?? null, 2) }}</td><td>{{ $row['store_id'] ?? '—' }}</td><td>{{ $row['item_id'] ?? '—' }}</td><td>{{ $row['demand_segment'] ?? '—' }}</td><td>{{ $formatNumber($row['avg_forecast_demand'] ?? null, 2) }}</td><td>{{ $formatNumber($row['demand_std'] ?? null, 2) }}</td><td>{{ $formatNumber($row['absolute_forecast_error'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null) }}</td></tr>
        @empty
            <tr><td colspan="9" class="muted">No recommendations returned by the API.</td></tr>
        @endforelse
        </tbody></table>
    </section>
@elseif($page === 'ai-analysis')
    @php($analysis = $data['analysis'] ?? [])
    <section class="grid kpis">
        <article class="kpi"><div class="kpi-label">Store-items analyzed</div><div class="kpi-value">{{ $formatNumber($analysis['total_store_items'] ?? null) }}</div><div class="kpi-note">Inventory and segment records</div></article>
        <article class="kpi"><div class="kpi-label">Average demand</div><div class="kpi-value">{{ $formatNumber($analysis['average_demand'] ?? null, 2) }}</div><div class="kpi-note">Units per store-item</div></article>
        <article class="kpi"><div class="kpi-label">Average absolute error</div><div class="kpi-value">{{ $formatNumber($analysis['average_absolute_forecast_error'] ?? null, 2) }}</div><div class="kpi-note">Forecast accuracy indicator</div></article>
        <article class="kpi"><div class="kpi-label">Average recommended stock</div><div class="kpi-value">{{ $formatNumber($analysis['average_recommended_stock'] ?? null, 2) }}</div><div class="kpi-note">Units per store-item</div></article>
    </section>
    <section class="grid two">
        <article class="card"><div class="card-heading"><div><h2>Business insights</h2><p class="card-description">Analysis produced by the existing API</p></div></div>
            <ul class="insight-list">@forelse($data['insights'] ?? [] as $insight)<li>{{ $insight }}</li>@empty<li>No insights returned by the API.</li>@endforelse</ul>
        </article>
        <article class="card table-wrap"><div class="card-heading"><div><h2>Segment profile</h2><p class="card-description">Average performance and stock by demand segment</p></div></div>
            <table><thead><tr><th>Segment</th><th>Store-items</th><th>Avg demand</th><th>Avg error</th><th>Avg stock</th></tr></thead><tbody>
            @forelse($data['segment_summary'] ?? [] as $row)
                <tr><td>{{ $row['demand_segment'] ?? '—' }}</td><td>{{ $formatNumber($row['store_item_count'] ?? null) }}</td><td>{{ $formatNumber($row['average_demand'] ?? null, 2) }}</td><td>{{ $formatNumber($row['forecast_error'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null, 2) }}</td></tr>
            @empty
                <tr><td colspan="5" class="muted">No segment analysis returned.</td></tr>
            @endforelse
            </tbody></table>
        </article>
    </section>
    <section class="card table-wrap"><div class="card-heading"><div><h2>Highest forecast error</h2><p class="card-description">Store-items flagged as the highest-risk predictions</p></div></div>
        <table><thead><tr><th>Store</th><th>Item</th><th>Segment</th><th>Forecast error</th><th>Absolute error</th><th>Recommended stock</th></tr></thead><tbody>
        @forelse($data['top_risk_items'] ?? [] as $row)
            <tr><td>{{ $row['store_id'] ?? '—' }}</td><td>{{ $row['item_id'] ?? '—' }}</td><td>{{ $row['segment'] ?? '—' }}</td><td>{{ $formatNumber($row['forecast_error'] ?? null, 2) }}</td><td>{{ $formatNumber($row['absolute_forecast_error'] ?? null, 2) }}</td><td>{{ $formatNumber($row['recommended_stock'] ?? null) }}</td></tr>
        @empty
            <tr><td colspan="6" class="muted">No high-risk items returned.</td></tr>
        @endforelse
        </tbody></table>
    </section>
@elseif($page === 'system-health')
    <section class="card">
        <div class="card-heading"><div><h2>ForecastOpti API status</h2><p class="card-description">Live health check from the existing FastAPI service</p></div><span class="badge {{ ($data['status'] ?? '') === 'healthy' ? 'low' : 'high' }}">{{ $data['status'] ?? 'Unavailable' }}</span></div>
        <div class="health-row"><span>Forecast records</span><strong>{{ $formatNumber($data['forecast_rows'] ?? null) }}</strong></div>
        <div class="health-row"><span>Inventory recommendation records</span><strong>{{ $formatNumber($data['optimization_rows'] ?? null) }}</strong></div>
        <div class="health-row"><span>Demand segmentation records</span><strong>{{ $formatNumber($data['clustering_rows'] ?? null) }}</strong></div>
    </section>
@endif
@endsection

@section('scripts')
<script>
    const numberFormat = new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 });
    const compactNumberFormat = new Intl.NumberFormat(undefined, {
        notation: 'compact',
        maximumFractionDigits: 1
    });
    const dateFormat = new Intl.DateTimeFormat(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        timeZone: 'UTC'
    });
    const chartDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
            legend: {
                position: 'bottom',
                align: 'start',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxWidth: 7,
                    boxHeight: 7,
                    padding: 18,
                    color: '#66738a',
                    font: { family: 'DM Sans', size: 11 }
                }
            },
            tooltip: {
                backgroundColor: '#142139',
                titleColor: '#fff',
                bodyColor: '#e5ebf5',
                borderColor: '#ffffff24',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 9,
                displayColors: true,
                usePointStyle: true,
                titleFont: { family: 'DM Sans', weight: '700' },
                bodyFont: { family: 'DM Sans' },
                callbacks: {
                    title(items) {
                        const value = items[0]?.label;
                        const date = value ? new Date(`${value}T00:00:00Z`) : null;
                        return date && !Number.isNaN(date.valueOf()) ? dateFormat.format(date) : value;
                    },
                    label(context) {
                        return `${context.dataset.label}: ${numberFormat.format(context.parsed.y ?? context.parsed.x)}`;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: { display: false },
                border: { display: false },
                ticks: { color: '#8691a3', maxTicksLimit: 8, maxRotation: 0, autoSkip: true, font: { family: 'DM Sans', size: 10 } }
            },
            y: {
                beginAtZero: true,
                border: { display: false },
                grid: { color: '#edf0f4', drawTicks: false },
                ticks: { color: '#8691a3', padding: 9, font: { family: 'DM Sans', size: 10 }, callback: value => compactNumberFormat.format(value) }
            }
        }
    };
    const makeLineChart = (id, rows) => {
        const canvas = document.getElementById(id);
        if (!canvas || !rows.length || typeof Chart === 'undefined') return;
        new Chart(canvas, {
            type: 'line',
            data: {
                labels: rows.map(row => row.date),
                datasets: [
                    {
                        label: 'Actual sales',
                        data: rows.map(row => Number(row.actual_sales ?? 0)),
                        borderColor: '#254c82',
                        backgroundColor(context) {
                            const { chart } = context;
                            const { chartArea } = chart;
                            if (!chartArea) return 'rgba(37, 76, 130, .14)';
                            const gradient = chart.ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                            gradient.addColorStop(0, 'rgba(37, 76, 130, .24)');
                            gradient.addColorStop(1, 'rgba(37, 76, 130, .01)');
                            return gradient;
                        },
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderWidth: 2,
                        tension: .3,
                        fill: true
                    },
                    {
                        label: 'Forecast',
                        data: rows.map(row => Number(row.predicted_sales ?? 0)),
                        borderColor: '#3472e8',
                        borderDash: [6, 4],
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderWidth: 2,
                        tension: .3
                    }
                ]
            },
            options: {
                ...chartDefaults,
                scales: {
                    ...chartDefaults.scales,
                    y: { ...chartDefaults.scales.y, beginAtZero: false, grace: '8%' }
                }
            }
        });
    };
    const makeBarChart = (id, labels, values, label) => {
        const canvas = document.getElementById(id);
        if (!canvas || !labels.length || typeof Chart === 'undefined') return;
        const colors = labels.map(value => {
            const segment = String(value).toLowerCase();
            if (['low', 'rendah'].includes(segment)) return '#9aa9bd';
            if (['medium', 'sedang'].includes(segment)) return '#3472e8';
            if (['high', 'tinggi'].includes(segment)) return '#20a477';
            return '#7560d7';
        });
        new Chart(canvas, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label,
                    data: values,
                    backgroundColor: colors.map(color => `${color}d9`),
                    hoverBackgroundColor: colors,
                    borderRadius: 7,
                    borderSkipped: false,
                    maxBarThickness: 48
                }]
            },
            options: {
                ...chartDefaults,
                indexAxis: 'y',
                interaction: { intersect: false, mode: 'nearest' },
                plugins: {
                    ...chartDefaults.plugins,
                    legend: { display: false },
                    tooltip: {
                        ...chartDefaults.plugins.tooltip,
                        callbacks: {
                            title: items => items[0]?.label ?? '',
                            label: context => `${numberFormat.format(context.parsed.x)} store-items`
                        }
                    }
                },
                scales: {
                    x: {
                        ...chartDefaults.scales.y,
                        suggestedMax: Math.max(...values.map(Number)) * 1.15,
                        ticks: {
                            ...chartDefaults.scales.y.ticks,
                            callback: value => compactNumberFormat.format(value)
                        }
                    },
                    y: {
                        ...chartDefaults.scales.x,
                        grid: { display: false },
                        ticks: { ...chartDefaults.scales.x.ticks, color: '#4b5870', font: { family: 'DM Sans', size: 11, weight: '600' } }
                    }
                }
            }
        });
    };
    @if($page === 'overview')
        makeLineChart('overviewForecast', @js($chartForecast));
        makeBarChart('overviewSegments', @js($segmentLabels), @js($segmentCounts), 'Store-items');
    @elseif($page === 'forecast')
        makeLineChart('forecastChart', @js($chartForecast));
    @elseif($page === 'demand-segmentation')
        makeBarChart('segmentChart', @js($segmentLabels), @js($segmentCounts), 'Store-items');
    @endif
</script>
@endsection
