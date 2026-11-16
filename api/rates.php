<?php
/**
 * api/rates.php - currency conversion endpoint.
 *
 * The currency pages used to call v6.exchangerate-api.com directly with an API key
 * embedded in the HTML, so the key shipped in every page view and every app build.
 * They now call this endpoint instead: the key stays on the server, and one cached
 * upstream call serves every conversion.
 *
 * GET api/rates.php?from=EUR&to=USD&amount=100
 *   -> {"ok":true,"from":"EUR","to":"USD","amount":100,"conversion_rate":1.08,
 *       "conversion_result":108,"updated":"2026-11-16T00:02:31Z"}
 *
 * The key comes from api/secrets.local.php (uploaded, never committed) or the
 * TH_EXCHANGE_RATE_API_KEY environment variable.
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
// The app loads its pages from file://, so its requests arrive cross-origin.
// This endpoint exposes no credentials and is safe to answer for any origin.
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Max-Age: 86400');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(204);
    exit;
}

const RATES_CACHE_TTL = 21600; // 6h; ExchangeRate-API refreshes daily on the free plan
const RATES_MAX_AMOUNT = 1000000000;

function rates_log(string $detail): void
{
    // Kept out of the response so the caller never sees upstream detail.
    @file_put_contents(
        __DIR__ . '/../data/rates-errors.log',
        date('c') . ' ' . $detail . PHP_EOL,
        FILE_APPEND | LOCK_EX
    );
}

function rates_fail(int $status, string $message): void
{
    http_response_code($status);
    echo json_encode(['ok' => false, 'error' => $message], JSON_UNESCAPED_SLASHES);
    exit;
}

function rates_secret(string $key, string $env_name): string
{
    $from_env = getenv($env_name);
    if ($from_env !== false && $from_env !== '') {
        return $from_env;
    }
    $file = __DIR__ . '/secrets.local.php';
    if (!is_file($file)) {
        return '';
    }
    $secrets = include $file;
    return is_array($secrets) && isset($secrets[$key]) && is_string($secrets[$key]) ? $secrets[$key] : '';
}

/** HTTP GET with a hard timeout. Returns the body or null. */
function rates_http_get(string $url): ?string
{
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_TIMEOUT => 8,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_USERAGENT => 'TimerHaven/1.0 (+https://timerhaven.com)',
        ]);
        $body = curl_exec($ch);
        $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return ($body !== false && $status >= 200 && $status < 300) ? (string) $body : null;
    }

    $context = stream_context_create([
        'http' => ['timeout' => 8, 'ignore_errors' => false, 'header' => "User-Agent: TimerHaven/1.0\r\n"],
    ]);
    $body = @file_get_contents($url, false, $context);
    return $body === false ? null : $body;
}

/**
 * All rates for a USD base, cached on disk. One upstream request per TTL serves
 * every pair, which is what keeps the free-plan quota untouched.
 */
function rates_table(string $api_key): ?array
{
    $cache_dir = __DIR__ . '/../data/rates-cache';
    $cache_file = $cache_dir . '/latest-usd.json';

    if (is_file($cache_file) && (time() - (int) filemtime($cache_file)) < RATES_CACHE_TTL) {
        $cached = json_decode((string) @file_get_contents($cache_file), true);
        if (is_array($cached) && isset($cached['conversion_rates']) && is_array($cached['conversion_rates'])) {
            return $cached;
        }
    }

    $body = rates_http_get('https://v6.exchangerate-api.com/v6/' . rawurlencode($api_key) . '/latest/USD');
    if ($body === null) {
        // Serving a stale table beats failing the conversion outright.
        if (is_file($cache_file)) {
            $stale = json_decode((string) @file_get_contents($cache_file), true);
            if (is_array($stale) && isset($stale['conversion_rates'])) {
                return $stale;
            }
        }
        rates_log('upstream request failed');
        return null;
    }

    $data = json_decode($body, true);
    if (!is_array($data) || ($data['result'] ?? '') !== 'success' || !isset($data['conversion_rates'])) {
        // 403 "quota reached", 401 "invalid key" etc. surface here.
        $reason = is_array($data) ? (string) ($data['error-type'] ?? $data['result'] ?? 'unknown') : 'unparsable';
        rates_log('upstream rejected: ' . $reason);
        return null;
    }

    if (!is_dir($cache_dir)) {
        @mkdir($cache_dir, 0775, true);
    }
    if (is_dir($cache_dir) && is_writable($cache_dir)) {
        $tmp = $cache_file . '.' . bin2hex(random_bytes(4)) . '.tmp';
        if (@file_put_contents($tmp, $body, LOCK_EX) !== false) {
            @rename($tmp, $cache_file);
        } else {
            @unlink($tmp);
        }
    }

    return $data;
}

$api_key = rates_secret('exchangerate_api_key', 'TH_EXCHANGE_RATE_API_KEY');
if ($api_key === '') {
    rates_log('exchangerate_api_key is not configured');
    rates_fail(503, 'Conversion is temporarily unavailable.');
}

$from = strtoupper(trim((string) ($_GET['from'] ?? '')));
$to = strtoupper(trim((string) ($_GET['to'] ?? '')));
$amount_raw = trim((string) ($_GET['amount'] ?? '1'));

if (!preg_match('/^[A-Z]{3}$/', $from) || !preg_match('/^[A-Z]{3}$/', $to)) {
    rates_fail(400, 'Currency codes must be three letters.');
}

if ($amount_raw === '' || !is_numeric($amount_raw)) {
    rates_fail(400, 'Amount must be a number.');
}
$amount = (float) $amount_raw;
if (!is_finite($amount) || $amount <= 0 || $amount > RATES_MAX_AMOUNT) {
    rates_fail(400, 'Amount must be greater than zero.');
}

$table = rates_table($api_key);
if ($table === null) {
    rates_fail(503, 'Conversion is temporarily unavailable.');
}

$rates = $table['conversion_rates'];
if (!isset($rates[$from], $rates[$to])) {
    rates_fail(400, 'Unsupported currency code.');
}

$rate = ((float) $rates[$to]) / ((float) $rates[$from]);
$result = $amount * $rate;

$updated = isset($table['time_last_update_unix'])
    ? gmdate('c', (int) $table['time_last_update_unix'])
    : null;

header('Cache-Control: public, max-age=300');
echo json_encode([
    'ok' => true,
    'from' => $from,
    'to' => $to,
    'amount' => $amount,
    'conversion_rate' => round($rate, 5),
    'conversion_result' => round($result, 5),
    'updated' => $updated,
], JSON_UNESCAPED_SLASHES);
