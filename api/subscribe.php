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

/**
 * TimerHaven Newsletter Subscription Handler
 * Specifically designed for Namecheap Shared Hosting (PHP 7.4/8.x)
 */

header('Content-Type: application/json');

// Configuration
$db_path = __DIR__ . '/../data/subscribers.db';

// 1. Initialize Database
try {
    $db = new PDO("sqlite:$db_path");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Create table if not exists with lang support
    $db->exec("CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        lang TEXT DEFAULT 'en',
        status TEXT DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )");

    // Migration: Add lang column if it doesn't exist (safety for existing DBs)
    $check_column = $db->query("PRAGMA table_info(subscribers)")->fetchAll();
    $has_lang = false;
    foreach ($check_column as $col) {
        if ($col['name'] === 'lang') {
            $has_lang = true;
            break;
        }
    }
    if (!$has_lang) {
        $db->exec("ALTER TABLE subscribers ADD COLUMN lang TEXT DEFAULT 'en'");
    }
} catch (PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    echo json_encode(['status' => 'error', 'message' => 'Database connection failed']);
    exit;
}

// 2. Process Request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = filter_var($_POST['email'] ?? '', FILTER_SANITIZE_EMAIL);
    // FILTER_SANITIZE_STRING is deprecated in PHP 8.1 and removed in 8.2
    $lang = isset($_POST['lang']) ? preg_replace('/[^a-z-]/', '', strtolower((string)$_POST['lang'])) : 'en';
    if (empty($lang)) $lang = 'en';

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['status' => 'error', 'message' => 'Invalid email address']);
        exit;
    }

    try {
        $stmt = $db->prepare("INSERT INTO subscribers (email, lang) VALUES (?, ?)");
        $stmt->execute([$email, $lang]);
        
        // 3. Send Welcome Email using PHPMailer
        require_once __DIR__ . '/PHPMailer/src/Exception.php';
        require_once __DIR__ . '/PHPMailer/src/PHPMailer.php';
        require_once __DIR__ . '/PHPMailer/src/SMTP.php';

        $mail = new PHPMailer\PHPMailer\PHPMailer(true);

        try {
            // SMTP settings
            $mail->isSMTP();
            $mail->Host       = 'timerhaven.com';
            $mail->SMTPAuth   = true;
            $mail->Username   = 'support@timerhaven.com';
            $mail->Password   = th_secret('smtp_pass', 'TH_SMTP_PASS');
            $mail->SMTPSecure = 'ssl';
            $mail->Port       = 465;
            $mail->CharSet    = 'UTF-8';

            // Recipients
            $mail->setFrom('support@timerhaven.com', 'TimerHaven');
            $mail->addAddress($email);

            // Content
            $mail->isHTML(true);
            $mail->Subject = "Welcome to TimerHaven: Master Your Focus";

            // Signed unsubscribe link (HMAC of the address) so nobody can unsubscribe
            // another person just by putting their email in the URL.
            $unsub_token = hash_hmac('sha256', strtolower(trim($email)), th_secret('unsubscribe_secret', 'TH_UNSUBSCRIBE_SECRET'));
            $unsub_url = 'https://timerhaven.com/api/unsubscribe.php?email=' . urlencode($email) . '&token=' . $unsub_token;

            $mail->Body    = '
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #185a9d 0%, #43cea2 100%); border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">TimerHaven</h1>
                </div>
                <div style="padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
                    <p>Hello,</p>
                    <p>Thank you for joining the TimerHaven community! You are now subscribed to our bi-weekly productivity digest.</p>
                    <p>Our mission is to help you reclaim your focus and master your energy with free, privacy-focused tools.</p>
                    
                    <h3>Quick Start Resources:</h3>
                    <ul>
                        <li><a href="https://timerhaven.com/en/pomodoro-timer/pomodoro-index.html">The Ultimate Pomodoro Guide</a></li>
                        <li><a href="https://timerhaven.com/blog/deep-work-guide.html">Deep Work Mastery</a></li>
                        <li><a href="https://timerhaven.com/recommendations/index.html">Recommended Productivity Gear</a></li>
                    </ul>

                    <p>Stay focused,<br>Serge from TimerHaven</p>
                    
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 0.8rem; color: #888;">
                        You received this email because you signed up at TimerHaven.com.<br>
                        <a href="' . $unsub_url . '">Unsubscribe</a>
                    </p>
                </div>
            </body>
            </html>';

            $mail->send();
        } catch (Exception $e) {
            // Log error but don't fail the subscription process
            error_log("PHPMailer Error: " . $mail->ErrorInfo);
        }

        echo json_encode(['status' => 'success', 'message' => 'Thank you for subscribing! Check your inbox for a welcome gift.']);
    } catch (PDOException $e) {
        if ($e->getCode() == '23000') {
            echo json_encode(['status' => 'duplicate', 'message' => 'You are already subscribed!']);
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Subscription failed. Please try again later.']);
        }
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid request method']);
}
?>
