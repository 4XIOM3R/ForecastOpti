<?php

namespace App\Http\Controllers;

use App\Services\ForecastApi;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class DashboardController extends Controller
{
    private const PAGES = [
        'overview' => ['title' => 'Overview', 'icon' => '◫'],
        'forecast' => ['title' => 'Forecast', 'icon' => '↗'],
        'inventory-analysis' => ['title' => 'Inventory Analysis', 'icon' => '▤'],
        'demand-segmentation' => ['title' => 'Demand Segmentation', 'icon' => '◉'],
        'recommendations' => ['title' => 'Recommendations', 'icon' => '✳'],
        'ai-analysis' => ['title' => 'AI Analysis', 'icon' => '✦'],
        'system-health' => ['title' => 'System Health', 'icon' => '⌁'],
    ];

    public function index(Request $request, ForecastApi $api, string $page = 'overview')
    {
        abort_unless(isset(self::PAGES[$page]), 404);

        $request->validate([
            'store' => ['nullable', 'string', 'max:100'],
            'item' => ['nullable', 'string', 'max:100'],
            'start_date' => ['nullable', 'date'],
            'end_date' => ['nullable', 'date', 'after_or_equal:start_date'],
        ]);

        $data = [];
        $apiError = null;

        try {
            $data = match ($page) {
                'overview' => $this->overview($api),
                'forecast' => $this->forecast($api, $request),
                'inventory-analysis' => $this->inventory($api, $request),
                'demand-segmentation' => $this->segmentation($api),
                'recommendations' => $api->get('/api/recommendations', ['limit' => 100]),
                'ai-analysis' => $api->get('/api/ai-analysis', ['limit' => 10]),
                'system-health' => $api->get('/api/health'),
            };
        } catch (ConnectionException|RequestException $exception) {
            $apiError = $exception->getMessage();
            Log::warning('ForecastOpti API request failed.', [
                'page' => $page,
                'error' => $apiError,
            ]);
        }

        return view('dashboard.index', [
            'page' => $page,
            'pageTitle' => self::PAGES[$page]['title'],
            'pages' => self::PAGES,
            'data' => $data,
            'apiError' => $apiError,
            'filters' => $request->only(['store', 'item', 'start_date', 'end_date']),
        ]);
    }

    private function overview(ForecastApi $api): array
    {
        return [
            'summary' => $api->get('/api/summary'),
            'forecast' => $api->get('/api/forecast'),
            'inventory' => $api->get('/api/inventory'),
            'segments' => $api->get('/api/segments'),
            'segment_summary' => $api->get('/api/segment-summary'),
        ];
    }

    private function forecast(ForecastApi $api, Request $request): array
    {
        $result = $api->get('/api/forecast');
        $rows = collect($result['data'] ?? []);

        if ($request->filled('start_date')) {
            $rows = $rows->where('date', '>=', $request->query('start_date'));
        }

        if ($request->filled('end_date')) {
            $rows = $rows->where('date', '<=', $request->query('end_date'));
        }

        $result['data'] = $rows->values()->all();
        $result['count'] = count($result['data']);

        return $result;
    }

    private function inventory(ForecastApi $api, Request $request): array
    {
        $result = [
            'segments' => $api->get('/api/segments'),
            'inventory' => $api->get('/api/inventory'),
            'analysis' => null,
        ];

        if ($request->filled('store') && $request->filled('item')) {
            $result['analysis'] = $api->post('/api/analyze', [
                'store_id' => $request->query('store'),
                'item_id' => $request->query('item'),
            ]);
        }

        return $result;
    }

    private function segmentation(ForecastApi $api): array
    {
        return [
            'segments' => $api->get('/api/segments'),
            'summary' => $api->get('/api/segment-summary'),
        ];
    }
}
