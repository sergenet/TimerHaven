<?php
// Credentials are not stored in this repo. They come from api/secrets.local.php
// (uploaded with the site, never committed) or from the environment.
$__secrets = is_file(__DIR__ . '/secrets.local.php') ? (include __DIR__ . '/secrets.local.php') : [];
if (!is_array($__secrets)) { $__secrets = []; }

if (!function_exists('th_secret')) {
    // Reads a credential from api/secrets.local.php (never committed) or the
    // environment. Defined as a function so it works inside any scope.
    function th_secret($key, $env_name) {
        global $__secrets;
        $from_env = getenv($env_name);
        if ($from_env !== false && $from_env !== '') { return $from_env; }
        return isset($__secrets[$key]) ? $__secrets[$key] : '';
    }
}

// contact.php - PHPMailer + SMTP contact endpoint
// ---------------------- IMPORTANT ----------------------
// Edit only the configuration block below BEFORE uploading.
// You must replace the two placeholders:
//  - $EXPECTED_SECRET        -> your secret token (keep private)
//  - $SMTP_PASS              -> the SMTP password for support@timerhaven.com
// Do NOT share the secret or SMTP password publicly.
// ------------------------------------------------------

header('Content-Type: application/json; charset=utf-8');

// ---------- CONFIG (edit these) ----------
$EXPECTED_SECRET = th_secret('contact_secret', 'TH_CONTACT_SECRET');
$DEST_EMAIL      = 'support@timerhaven.com';
$FROM_EMAIL      = 'no-reply@timerhaven.com';
$SMTP_HOST       = 'timerhaven.com';
$SMTP_PORT       = 465;
$SMTP_USER       = 'support@timerhaven.com';
$SMTP_PASS       = th_secret('smtp_pass', 'TH_SMTP_PASS');
$SMTP_SECURE     = 'ssl';
// ------------------------------------------

// Security: require PHPMailer library present
$phpMailerPath = __DIR__ . '/PHPMailer/src/PHPMailer.php';
if (!file_exists($phpMailerPath)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'phpmailer_missing', 'detail' => 'PHPMailer library not found in api/PHPMailer']);
    exit;
}

// Read and validate secret header
$allHeaders = function_exists('getallheaders') ? getallheaders() : [];
$providedSecret = $allHeaders['X-Contact-Secret'] ?? $allHeaders['x-contact-secret'] ?? '';

if ($providedSecret !== $EXPECTED_SECRET) {
    http_response_code(403);
    echo json_encode(['ok' => false, 'error' => 'unauthorized']);
    exit;
}

// Read JSON body
$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'invalid_json']);
    exit;
}

$name = trim($data['name'] ?? '');
$email = trim($data['email'] ?? '');
$message = trim($data['message'] ?? '');
$pageUrl = $data['pageUrl'] ?? '';
$userAgent = $data['userAgent'] ?? '';

// Basic validation
if ($message === '') {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'empty_message']);
    exit;
}

// Load PHPMailer
require_once __DIR__ . '/PHPMailer/src/Exception.php';
require_once __DIR__ . '/PHPMailer/src/PHPMailer.php';
require_once __DIR__ . '/PHPMailer/src/SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

$mail = new PHPMailer(true);

try {
    // SMTP config
    $mail->isSMTP();
    $mail->Host       = $SMTP_HOST;
    $mail->SMTPAuth   = true;
    $mail->Username   = $SMTP_USER;
    $mail->Password   = $SMTP_PASS;
    $mail->SMTPSecure = $SMTP_SECURE;
    $mail->Port       = $SMTP_PORT;
    // Optional: timeout and debugging
    $mail->Timeout = 30;
    $mail->SMTPDebug = 0;

    // Message headers/body
    $mail->setFrom($FROM_EMAIL, 'TimerHaven Contact');
    $mail->addAddress($DEST_EMAIL);

    // If user provided an email, set Reply-To
    if (!empty($email)) {
        $mail->addReplyTo($email, $name ?: $email);
    }

    $subject = 'Contact form message from mobile app';
    $body = "Name: $name\nEmail: $email\nPage: $pageUrl\nUserAgent: $userAgent\n\nMessage:\n$message\n";

    $mail->Subject = $subject;
    $mail->Body    = $body;
    $mail->CharSet = 'UTF-8';

    if (!$mail->send()) {
        // In rare case send() returns false
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'mail_failed', 'detail' => $mail->ErrorInfo]);
        exit;
    }

    // Success
    echo json_encode(['ok' => true]);
    exit;
} catch (Exception $e) {
    // PHPMailer exception (network/auth issues)
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'exception', 'detail' => $e->getMessage()]);
    exit;
}