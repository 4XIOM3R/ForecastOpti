#!/bin/sh
set -eu

if [ -z "${APP_KEY:-}" ]; then
    key_file="storage/app/.app-key"

    if [ ! -s "$key_file" ]; then
        php artisan key:generate --show > "$key_file"
    fi

    export APP_KEY="$(cat "$key_file")"
fi

exec apache2-foreground
