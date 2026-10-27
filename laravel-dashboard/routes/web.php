<?php

use App\Http\Controllers\DashboardController;
use Illuminate\Support\Facades\Route;

Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
Route::get('/{page}', [DashboardController::class, 'index'])
    ->whereIn('page', [
        'forecast',
        'inventory-analysis',
        'demand-segmentation',
        'recommendations',
        'ai-analysis',
        'system-health',
    ])
    ->name('dashboard.page');
