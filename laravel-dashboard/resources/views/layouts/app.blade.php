<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $pageTitle }} | ForecastOpti</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.9/dist/chart.umd.min.js"></script>
    <style>
        :root {
            color: #172033;
            background: #f4f6fa;
            font-family: "DM Sans", sans-serif;
            font-synthesis: none;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-optical-sizing: auto;
        }

        * { box-sizing: border-box; }
        body { min-width: 320px; min-height: 100vh; margin: 0; }
        a { color: inherit; text-decoration: none; }
        button, input, select { font: inherit; }
        :focus-visible { outline: 3px solid #7da2ff; outline-offset: 3px; }

        .shell {
            display: grid;
            grid-template-columns: 252px minmax(0, 1fr);
            min-height: 100vh;
        }

        .sidebar {
            position: sticky;
            top: 0;
            display: flex;
            height: 100vh;
            flex-direction: column;
            gap: 28px;
            padding: 26px 16px;
            overflow-y: auto;
            background: #101a2b;
            color: #d5dbea;
        }

        .brand { display: flex; align-items: center; gap: 12px; padding: 4px 10px 20px; }
        .brand-mark {
            display: grid;
            width: 38px;
            height: 38px;
            flex: 0 0 38px;
            place-items: center;
            border-radius: 12px;
            background: #3167ed;
            color: white;
            font: 800 19px Manrope, sans-serif;
        }
        .brand-name { color: #fff; font: 800 16px Manrope, sans-serif; letter-spacing: -.4px; }
        .brand-subtitle { margin-top: 3px; color: #8e9bb1; font-size: 11px; }
        .nav-label { padding: 0 12px; color: #71809a; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; }
        .nav-list { display: grid; gap: 5px; margin-top: 10px; }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 12px;
            min-height: 40px;
            padding: 10px 12px;
            border-radius: 9px;
            color: #aab5c9;
            font-size: 13px;
            font-weight: 600;
            transition: background .15s ease, color .15s ease;
        }
        .nav-link:hover { background: #1b2940; color: white; }
        .nav-link.active { background: #263a5b; color: white; box-shadow: inset 3px 0 #5c88ff; }
        .nav-icon { width: 19px; flex: 0 0 19px; text-align: center; font-size: 16px; }
        .sidebar-foot { margin-top: auto; padding: 18px 10px 0; border-top: 1px solid #253149; color: #77859d; font-size: 11px; line-height: 1.6; }

        .main { min-width: 0; padding: 30px clamp(18px, 3vw, 42px) 48px; }
        .topbar { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-bottom: 26px; }
        .eyebrow { color: #78859a; font-size: 10px; font-weight: 700; letter-spacing: 1.15px; text-transform: uppercase; }
        h1, h2, h3, p { margin-top: 0; }
        h1 { margin: 6px 0 0; color: #172033; font: 800 27px Manrope, sans-serif; letter-spacing: -.8px; }
        h2 { margin: 0 0 5px; font: 700 16px Manrope, sans-serif; letter-spacing: -.2px; }
        h3 { margin: 0 0 5px; font: 700 14px Manrope, sans-serif; }
        .subtitle { margin: 7px 0 0; color: #7a8698; font-size: 13px; line-height: 1.5; }
        .status { display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 999px; background: #e8f7ef; color: #187449; font-size: 11px; font-weight: 700; white-space: nowrap; }
        .status::before { width: 7px; height: 7px; border-radius: 50%; background: #20a66a; content: ""; }
        .status.down { background: #fff0ed; color: #b33d2b; }
        .status.down::before { background: #e05b46; }

        .alert { margin: 0 0 20px; padding: 14px 16px; overflow-wrap: anywhere; border: 1px solid #f0c4bd; border-radius: 12px; background: #fff2ef; color: #8e3024; font-size: 13px; line-height: 1.55; }
        .alert strong { display: block; margin-bottom: 4px; }
        .banner { margin-bottom: 20px; padding: 25px 27px; border-radius: 16px; background: linear-gradient(112deg, #17263e, #244c8a 68%, #3571e8); box-shadow: 0 12px 30px #25477820; color: white; }
        .banner h2 { margin-bottom: 7px; font-size: 20px; }
        .banner p { max-width: 760px; margin: 0; color: #d1def4; font-size: 13px; line-height: 1.65; }

        .grid { display: grid; gap: 16px; }
        .grid.kpis { grid-template-columns: repeat(4, minmax(0, 1fr)); margin-bottom: 20px; }
        .grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
        .card, .kpi { min-width: 0; border: 1px solid #e7ebf1; border-radius: 14px; background: #fff; box-shadow: 0 4px 15px #1a2c4a07; }
        .card { margin-bottom: 16px; padding: 19px; }
        .card-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 16px; }
        .card-description { margin: 0; color: #8490a2; font-size: 12px; line-height: 1.5; }
        .kpi { min-height: 116px; padding: 17px 18px; border-top: 3px solid #2d63dc; }
        .kpi:nth-child(2) { border-top-color: #179a69; }
        .kpi:nth-child(3) { border-top-color: #d79126; }
        .kpi:nth-child(4) { border-top-color: #7560d7; }
        .kpi-label { color: #778398; font-size: 11px; font-weight: 700; }
        .kpi-value { margin: 10px 0 3px; overflow-wrap: anywhere; color: #172033; font: 800 25px Manrope, sans-serif; letter-spacing: -.6px; }
        .kpi-note { color: #929bad; font-size: 11px; line-height: 1.45; }
        .section-title { margin: 24px 0 13px; font: 800 17px Manrope, sans-serif; }
        .chart-wrap { position: relative; height: 300px; }
        .chart-wrap.small { height: 245px; }
        .chart-empty { display: grid; height: 100%; min-height: 180px; place-content: center; gap: 6px; border: 1px dashed #dfe5ef; border-radius: 10px; background: #fafbfd; color: #68758a; text-align: center; }
        .chart-empty strong { color: #39475d; font-size: 13px; }
        .chart-empty span { font-size: 11px; }

        .table-wrap { min-width: 0; overflow-x: auto; overscroll-behavior-x: contain; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; white-space: nowrap; }
        th { background: #f8f9fb; color: #78859a; font-size: 10px; font-weight: 700; letter-spacing: .3px; text-align: left; text-transform: uppercase; }
        th, td { padding: 11px 12px; border-bottom: 1px solid #edf0f4; }
        th:first-child, td:first-child { padding-left: 14px; }
        td { color: #344054; }
        tbody tr { transition: background .12s ease; }
        tbody tr:hover { background: #f8faff; }
        tbody tr:last-child td { border-bottom: 0; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 99px; background: #eef2f8; color: #4e5e78; font-size: 10px; font-weight: 700; }
        .badge.high, .badge.tinggi { background: #fff0ec; color: #bc4c35; }
        .badge.medium, .badge.sedang { background: #fff6df; color: #986a11; }
        .badge.low, .badge.rendah { background: #eaf6ef; color: #24734a; }

        .form-row { display: flex; align-items: end; gap: 12px; flex-wrap: wrap; }
        .field { display: grid; min-width: 150px; gap: 6px; }
        label { color: #59667b; font-size: 11px; font-weight: 700; }
        select, input { width: 100%; height: 40px; padding: 0 11px; border: 1px solid #dfe4ec; border-radius: 8px; background: #fff; color: #29364b; font-size: 12px; }
        select:focus, input:focus { border-color: #7195ed; outline: 3px solid #3167ed1a; }
        button, .button { display: inline-flex; min-height: 40px; align-items: center; justify-content: center; padding: 0 16px; border: 0; border-radius: 8px; background: #245bd7; color: #fff; cursor: pointer; font: 700 12px "DM Sans", sans-serif; transition: background .15s ease; }
        button:hover, .button:hover { background: #1949b6; }
        .button.secondary { background: #edf1f7; color: #43516a; }
        .button.secondary:hover { background: #e1e7f0; }
        .muted { color: #8591a3; font-size: 12px; }
        .insight-list { display: grid; margin: 0; padding: 0; gap: 10px; list-style: none; }
        .insight-list li { padding: 12px 14px; border: 1px solid #edf0f4; border-radius: 9px; background: #f7f9fc; color: #46536a; font-size: 13px; line-height: 1.5; }
        .health-row { display: flex; justify-content: space-between; gap: 14px; padding: 13px 0; border-bottom: 1px solid #edf0f4; font-size: 13px; }
        .health-row:last-child { border-bottom: 0; }
        .health-row span:first-child { color: #758196; }
        .health-row strong { color: #27354a; text-align: right; }

        @media (max-width: 1100px) {
            .shell { grid-template-columns: 224px minmax(0, 1fr); }
            .grid.kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .main { padding-right: 24px; padding-left: 24px; }
        }

        @media (max-width: 760px) {
            .shell { grid-template-columns: minmax(0, 1fr); }
            .sidebar { position: sticky; z-index: 5; top: 0; height: auto; gap: 10px; padding: 10px 14px 8px; box-shadow: 0 5px 18px #101a2b18; }
            .brand { padding: 2px 6px 5px; }
            .brand-mark { width: 34px; height: 34px; flex-basis: 34px; border-radius: 10px; font-size: 17px; }
            .brand-name { font-size: 15px; }
            .brand-subtitle { font-size: 10px; }
            .nav-label, .sidebar-foot { display: none; }
            .nav-list { display: flex; gap: 5px; margin: 0 -2px; padding: 1px 2px 5px; overflow-x: auto; scrollbar-width: thin; scrollbar-color: #43516a transparent; }
            .nav-link { min-height: 36px; flex: 0 0 auto; gap: 7px; padding: 8px 10px; font-size: 11px; white-space: nowrap; }
            .nav-icon { width: auto; flex-basis: auto; font-size: 14px; }
            .main { padding: 22px 18px 36px; }
            .topbar { align-items: flex-start; margin-bottom: 20px; }
            .grid.two, .grid.three { grid-template-columns: minmax(0, 1fr); }
            .grid.kpis { gap: 11px; }
            .kpi { min-height: 105px; padding: 14px; }
            .kpi-value { font-size: 22px; }
            h1 { font-size: 24px; }
            .chart-wrap { height: 275px; }
        }

        @media (max-width: 480px) {
            .main { padding-right: 13px; padding-left: 13px; }
            .topbar { gap: 10px; }
            .eyebrow { font-size: 9px; letter-spacing: .8px; }
            h1 { font-size: 21px; }
            .subtitle { max-width: 34ch; font-size: 12px; }
            .status { gap: 6px; padding: 7px 9px; font-size: 9px; }
            .status::before { width: 6px; height: 6px; }
            .banner { padding: 19px; }
            .banner h2 { font-size: 18px; }
            .banner p { font-size: 12px; }
            .grid.kpis { gap: 9px; }
            .kpi { min-height: 100px; padding: 12px; }
            .kpi-label, .kpi-note { font-size: 10px; }
            .kpi-value { margin-top: 8px; font-size: 19px; }
            .card { padding: 15px 13px; }
            .card-heading { margin-bottom: 13px; }
            h2 { font-size: 14px; }
            .card-description { font-size: 11px; }
            .chart-wrap { height: 245px; }
            .form-row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .field { min-width: 0; }
            .form-row button, .form-row .button { width: 100%; }
            th, td { padding: 10px; }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
        }
    </style>
</head>
<body>
<div class="shell">
    <aside class="sidebar">
        <a class="brand" href="{{ route('dashboard') }}">
            <span class="brand-mark">F</span>
            <span>
                <span class="brand-name">ForecastOpti</span>
                <span class="brand-subtitle" style="display:block">Demand &amp; Inventory Intelligence</span>
            </span>
        </a>
        <nav aria-label="Main navigation">
            <div class="nav-label">Workspace</div>
            <div class="nav-list">
                @foreach($pages as $slug => $item)
                    <a class="nav-link {{ $page === $slug ? 'active' : '' }}"
                       href="{{ $slug === 'overview' ? route('dashboard') : route('dashboard.page', ['page' => $slug] ) }}">
                        <span class="nav-icon">{{ $item['icon'] }}</span>
                        <span>{{ $item['title'] }}</span>
                    </a>
                @endforeach
            </div>
        </nav>
        <div class="sidebar-foot">ForecastOpti<br>Forecasting · Inventory · Segmentation</div>
    </aside>
    <main class="main">
        <header class="topbar">
            <div>
                <div class="eyebrow">Demand and inventory decision support</div>
                <h1>{{ $pageTitle }}</h1>
                <p class="subtitle">Explore forecasts and inventory insights from your existing ForecastOpti API.</p>
            </div>
            <span class="status {{ $apiError ? 'down' : '' }}">{{ $apiError ? 'API unavailable' : 'API connected' }}</span>
        </header>
        @if($apiError)
            <div class="alert" role="alert">
                <strong>Could not load data from the ForecastOpti API.</strong>
                {{ $apiError }}
                <div style="margin-top:6px">Check that FastAPI is running and that <code>FORECASTOPTI_API_URL</code> points to it.</div>
            </div>
        @endif
        @yield('content')
    </main>
</div>
@yield('scripts')
</body>
</html>
