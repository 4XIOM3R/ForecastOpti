<?php

namespace Tests\Feature;

use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class DashboardTest extends TestCase
{
    public function test_overview_uses_existing_api_endpoints(): void
    {
        Http::fake([
            '*/api/summary' => Http::response([
                'total_actual_sales' => 1000,
                'test_mae' => 2.5,
                'test_rmse' => 3.2,
                'test_wape' => 11.2,
                'model' => 'HistGradientBoosting + Lag Features',
                'total_store_items' => 12,
            ]),
            '*/api/forecast' => Http::response([
                'count' => 1,
                'data' => [['date' => '2024-01-01', 'actual_sales' => 30, 'predicted_sales' => 28]],
            ]),
            '*/api/inventory' => Http::response([
                'count' => 1,
                'data' => [['store_id' => 'store_1', 'item_id' => 'item_1', 'recommended_stock' => 40]],
            ]),
            '*/api/segments' => Http::response(['count' => 1, 'data' => []]),
            '*/api/segment-summary' => Http::response([
                'count' => 1,
                'data' => [['business_level' => 'Tinggi', 'store_item_count' => 1]],
            ]),
        ]);

        $this->get('/')
            ->assertOk()
            ->assertSee('Your demand, at a glance')
            ->assertSee('HistGradientBoosting + Lag Features')
            ->assertSee('API connected');

        Http::assertSent(fn (Request $request) => str_ends_with($request->url(), '/api/summary'));
    }

    public function test_inventory_page_uses_existing_store_item_analysis_endpoint(): void
    {
        Http::fake([
            '*/api/segments' => Http::response([
                'count' => 1,
                'data' => [['store_id' => 'store_1', 'item_id' => 'item_1']],
            ]),
            '*/api/inventory' => Http::response(['count' => 0, 'data' => []]),
            '*/api/analyze' => Http::response([
                'store_id' => 'store_1',
                'item_id' => 'item_1',
                'inventory' => [
                    'avg_forecast_demand' => 25,
                    'demand_std' => 4,
                    'demand_buffer' => 8,
                    'recommended_stock' => 33,
                    'demand_category' => 'Medium',
                ],
                'segmentation' => ['demand_segment' => 'Sedang'],
            ]),
        ]);

        $this->get('/inventory-analysis?store=store_1&item=item_1')
            ->assertOk()
            ->assertSee('store_1 · item_1')
            ->assertSee('33');

        Http::assertSent(fn (Request $request) => $request->method() === 'POST'
            && str_ends_with($request->url(), '/api/analyze')
            && $request['store_id'] === 'store_1'
            && $request['item_id'] === 'item_1');
    }

    public function test_forecast_page_displays_rows_from_the_forecast_endpoint(): void
    {
        Http::fake([
            '*/api/forecast' => Http::response([
                'count' => 1,
                'data' => [[
                    'date' => '2024-01-15',
                    'actual_sales' => 1200,
                    'predicted_sales' => 1150,
                ]],
            ]),
        ]);

        $this->get('/forecast')
            ->assertOk()
            ->assertSee('1 daily records in selected range')
            ->assertSee('2024-01-15')
            ->assertSee('1,200')
            ->assertSee('1,150');
    }

    public function test_api_failures_are_reported_in_the_dashboard(): void
    {
        Http::fake([
            '*/api/summary' => Http::response(['detail' => 'service unavailable'], 503),
        ]);

        $this->get('/')
            ->assertOk()
            ->assertSee('Could not load data from the ForecastOpti API.')
            ->assertSee('503');
    }
}
