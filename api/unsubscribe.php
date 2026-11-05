<?php
/**
 * TimerHaven Newsletter Unsubscribe Handler
 *
 * The link must be signed: unsubscribe.php?email=...&token=<hmac-sha256>
 * The token is an HMAC of the normalised address using unsubscribe_secret from
 * api/secrets.local.php, so a visitor cannot unsubscribe someone else simply by
 * putting their address in the URL. Requests with a missing or wrong token are
 * refused and change nothing.
 */

header('Content-Type: text/html; charset=UTF-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

// Configuration
$db_path = __DIR__ . '/../data/subscribers.db';

$__secrets = is_file(__DIR__ . '/secrets.local.php') ? (include __DIR__ . '/secrets.local.php') : [];
if (!is_array($__secrets)) { $__secrets = []; }

if (!function_exists('th_secret')) {
    function th_secret($key, $env_name) {
        global $__secrets;
        $from_env = getenv($env_name);
        if ($from_env !== false && $from_env !== '') { return $from_env; }
        return isset($__secrets[$key]) ? $__secrets[$key] : '';
    }
}

$signing_key = th_secret('unsubscribe_secret', 'TH_UNSUBSCRIBE_SECRET');

// PHP has already URL-decoded the query string; decoding again would corrupt
// addresses containing a percent sign.
$email = isset($_GET['email']) ? strtolower(trim((string)$_GET['email'])) : '';
$token = isset($_GET['token']) ? (string)$_GET['token'] : '';

$expected = hash_hmac('sha256', $email, $signing_key);
$authorised = $signing_key !== ''
    && $email !== ''
    && $token !== ''
    && hash_equals($expected, $token);

if (!$authorised) {
    http_response_code(403);
    $message = "<h1>Link not valid</h1><p>This unsubscribe link is incomplete or damaged, so nothing was changed.</p>"
             . "<p>Please use the link from a recent TimerHaven email, or contact us at support@timerhaven.com and we will remove you by hand.</p>";
} else {
    try {
        $db = new PDO("sqlite:$db_path");
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $db->prepare("UPDATE subscribers SET status = 'unsubscribed' WHERE email = ?");
        $stmt->execute([$email]);

        $message = "<h1>Successfully Unsubscribed</h1><p>The email <strong>" . htmlspecialchars($email)
                 . "</strong> has been removed from our active mailing list. We're sorry to see you go!</p>";
    } catch (PDOException $e) {
        http_response_code(500);
        $message = "<h1>Error</h1><p>Something went wrong. Please try again later or contact us directly.</p>";
    }
}

// Simple HTML wrapper for the message
echo '<!DOCTYPE html><html><head><title>Unsubscribe - TimerHaven</title><meta name="robots" content="noindex"><style>body{font-family:sans-serif;text-align:center;padding:50px;} .container{max-width:500px;margin:0 auto;border:1px solid #ddd;padding:30px;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,0.1);}</style></head><body><div class="container">' . $message . '<br><a href="https://timerhaven.com">Back to TimerHaven</a></div></body></html>';
