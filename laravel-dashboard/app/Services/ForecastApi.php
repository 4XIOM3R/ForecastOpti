<?php

namespace App\Services;

use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Support\Facades\Http;
use UnexpectedValueException;

class ForecastApi
{
    /**
     * @throws ConnectionException
     * @throws RequestException
     */
    public function get(string $path, array $query = []): array
    {
        return $this->request('get', $path, $query);
    }

    /**
     * @throws ConnectionException
     * @throws RequestException
     */
    public function post(string $path, array $payload = []): array
    {
        return $this->request('post', $path, $payload);
    }

    /**
     * @throws ConnectionException
     * @throws RequestException
     */
    private function request(string $method, string $path, array $data): array
    {
        $response = Http::baseUrl(rtrim(config('services.forecastopti.api_url'), '/'))
            ->acceptJson()
            ->timeout(config('services.forecastopti.api_timeout'))
            ->{$method}($path, $data)
            ->throw();

        $payload = $response->json();

        if (! is_array($payload)) {
            throw new UnexpectedValueException(
                "ForecastOpti API returned an invalid JSON payload for {$path}."
            );
        }

        return $payload;
    }
}
