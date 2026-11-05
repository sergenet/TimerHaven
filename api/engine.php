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
 * TimerHaven Automated Newsletter Engine V2
 * Schedule: 1st and 15th of every month (via Cron)
 * Content: External Productivity Curation + Multi-language Tool Rotation
 */

// --- CONFIGURATION ---
$db_path = __DIR__ . '/../data/subscribers.db';
$sender_email = "support@timerhaven.com";
// The web-run token lives in api/secrets.local.php (never committed). It used to be a
// literal here, which meant anyone reading the public repo could fire a full send.
$secret_token = th_secret('engine_token', 'TH_ENGINE_TOKEN');
$batch_size = 50;
$batch_delay = 2;

// RSS Sources (Top Productivity Blogs)
$rss_feeds = [
    'James Clear' => 'https://jamesclear.com/feed',
    'Zen Habits' => 'https://zenhabits.net/feed',
    'Farnam Street' => 'https://fs.blog/feed',
    'Ness Labs' => 'https://nesslabs.com/feed'
];

// Security: cron may run this over CLI; a web run must present the secret token.
// Fail closed: with no configured token, the web path is disabled entirely.
if (php_sapi_name() !== 'cli') {
    $provided = (string)($_GET['token'] ?? '');
    if ($secret_token === '' || !hash_equals($secret_token, $provided)) {
        http_response_code(403);
        exit('Forbidden');
    }
}

// --- 1. INITIALIZE DATABASE & STATE ---
try {
    $db = new PDO("sqlite:$db_path");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

    // Create required tables
    $db->exec("CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        status TEXT DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )");

    // Migration: Add lang column if it doesn't exist
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

    $db->exec("CREATE TABLE IF NOT EXISTS newsletter_state (
        id INTEGER PRIMARY KEY,
        last_tool_index INTEGER DEFAULT 0,
        rotation_count INTEGER DEFAULT 0,
        last_sent_at DATETIME
    )");

    $db->exec("CREATE TABLE IF NOT EXISTS sent_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_url TEXT UNIQUE,
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )");

    if ($db->query("SELECT COUNT(*) FROM newsletter_state")->fetchColumn() == 0) {
        $db->exec("INSERT INTO newsletter_state (id, last_tool_index, rotation_count) VALUES (1, -1, 0)");
    }
} catch (PDOException $e) {
    die("Database Error: " . $e->getMessage());
}

// --- 2. FETCH EXTERNAL ARTICLE ---
function fetch_latest_article($feeds, $db) {
    // Pick a random feed to rotate sources
    $source_names = array_keys($feeds);
    shuffle($source_names);
    
    foreach ($source_names as $source) {
        $url = $feeds[$source];
        try {
            $rss = @simplexml_load_file($url);
            if (!$rss) continue;

            foreach ($rss->channel->item as $item) {
                $link = (string)$item->link;
                $title = (string)$item->title;
                $description = strip_tags((string)$item->description);
                if (strlen($description) > 250) $description = substr($description, 0, 247) . "...";

                // Check if already sent
                $stmt = $db->prepare("SELECT id FROM sent_articles WHERE article_url = ?");
                $stmt->execute([$link]);
                if (!$stmt->fetch()) {
                    return [
                        'source' => $source,
                        'title' => $title,
                        'url' => $link,
                        'excerpt' => $description
                    ];
                }
            }
        } catch (Exception $e) { continue; }
    }
    return null; // No fresh articles found
}

$article = fetch_latest_article($rss_feeds, $db);
if (!$article) {
    die("No new external articles found. Keeping rotation on hold.");
}

// --- 3. TOOL ROTATION (Localized descriptions) ---
$tools = [
    'pomodoro' => [
        'name' => ['en'=>'Pomodoro Timer', 'fr'=>'Minuteur Pomodoro', 'es'=>'Temporizador Pomodoro', 'de'=>'Pomodoro-Timer'],
        'url' => 'https://timerhaven.com/%l/pomodoro-timer/pomodoro-index.html',
        'desc' => [
            'en' => 'Master the 25/5 rhythm to reclaim your focus.',
            'fr' => 'Maîtrisez le rythme 25/5 pour retrouver votre concentration.',
            'es' => 'Domina el ritmo 25/5 para recuperar tu enfoque.',
            'de' => 'Meistern Sie den 25/5-Rhythmus, um Ihren Fokus zurückzugewinnen.'
        ]
    ],
    'meeting-planner' => [
        'name' => ['en'=>'Meeting Planner', 'fr'=>'Planificateur de Réunion', 'es'=>'Planificador de Reuniones', 'de'=>'Besprechungsplaner'],
        'url' => 'https://timerhaven.com/%l/meeting-planner/meeting-planner-index.html',
        'desc' => [
            'en' => 'Find the perfect overlap for your global team.',
            'fr' => 'Trouvez le chevauchement parfait pour votre équipe mondiale.',
            'es' => 'Encuentra el solapamiento perfecto para tu equipo global.',
            'de' => 'Finden Sie die perfekte Überschneidung für Ihr globales Team.'
        ]
    ],
    'deep-work' => [
        'name' => ['en'=>'Deep Work Guide', 'fr'=>'Guide du Travail Profond', 'es'=>'Guía de Trabajo Profundo', 'de'=>'Deep Work Leitfaden'],
        'url' => 'https://timerhaven.com/blog/deep-work-guide.html',
        'desc' => [
            'en' => 'The ultimate framework for high-value output.',
            'fr' => 'Le cadre ultime pour une production de haute valeur.',
            'es' => 'El marco definitivo para una producción de alto valor.',
            'de' => 'Das ultimative Framework für wertvolle Ergebnisse.'
        ]
    ]
];

$state = $db->query("SELECT * FROM newsletter_state WHERE id = 1")->fetch();
$tool_keys = array_keys($tools);
$next_tool_index = ($state['last_tool_index'] + 1) % count($tool_keys);
$featured_tool_id = $tool_keys[$next_tool_index];
$featured_tool = $tools[$featured_tool_id];

// --- 4. SEND CAMPAIGN ---
$subscribers = $db->query("SELECT email, lang FROM subscribers WHERE status = 'active'")->fetchAll();

// Dry run: everything up to here has run for real (article picked, state read,
// recipients counted) but no mail is sent. Lets the schedule be tested safely.
$is_dry_run = isset($_GET['dry']) || (isset($argv) && is_array($argv) && in_array('--dry-run', $argv, true));
if ($is_dry_run) {
    header('Content-Type: text/plain');
    echo "DRY RUN - nothing was sent.\n";
    echo "Recipients who would receive it: " . count($subscribers) . "\n";
    echo "Article: " . $article['title'] . "\n";
    echo "Source:  " . $article['source'] . "\n";
    echo "Featured tool: " . $featured_tool_id . "\n";
    echo "Rotation index: " . $next_tool_index . "\n";
    exit;
}

    // --- 4. SEND EMAILS using PHPMailer ---
    require_once __DIR__ . '/PHPMailer/src/Exception.php';
    require_once __DIR__ . '/PHPMailer/src/PHPMailer.php';
    require_once __DIR__ . '/PHPMailer/src/SMTP.php';

    $mail = new PHPMailer\PHPMailer\PHPMailer(true);
    
    // SMTP settings
    $mail->isSMTP();
    $mail->Host       = 'timerhaven.com';
    $mail->SMTPAuth   = true;
    $mail->Username   = 'support@timerhaven.com';
    $mail->Password   = th_secret('smtp_pass', 'TH_SMTP_PASS');
    $mail->SMTPSecure = 'ssl';
    $mail->Port       = 465;
    $mail->CharSet    = 'UTF-8';
    $mail->setFrom($sender_email, 'TimerHaven');
    $mail->isHTML(true);

    $count = 0; // Initialize count for PHPMailer loop
    foreach ($subscribers as $sub) {
        $to = $sub['email'];
        $lang = in_array($sub['lang'], ['en', 'fr', 'es', 'de', 'ru', 'el', 'ar']) ? $sub['lang'] : 'en';
        
        // Localized Subject
        $subjects = [
            'en' => "The Focus Edge: " . $article['title'],
            'fr' => "Le Focus Edge : " . $article['title'],
            'es' => "The Focus Edge: " . $article['title'],
            'de' => "The Focus Edge: " . $article['title']
        ];
        $subject = $subjects[$lang] ?? $subjects['en'];
        
        // Build Tool Link
        $tool_url = str_replace('%l', $lang, $featured_tool['url']);
        if ($lang == 'en' && strpos($tool_url, '/en/') !== false) $tool_url = str_replace('/en/', '/', $tool_url); // Root fix
        
        // Signed unsubscribe link: the token is an HMAC of the address, so nobody can
        // unsubscribe someone else just by guessing their email address.
        $unsub_token = hash_hmac('sha256', strtolower(trim($to)), th_secret('unsubscribe_secret', 'TH_UNSUBSCRIBE_SECRET'));
        $unsub_link = "https://timerhaven.com/api/unsubscribe.php?email=" . urlencode($to) . "&token=" . $unsub_token;

        $message = "
        <html>
        <body style='font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;'>
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #185a9d 0%, #43cea2 100%); border-radius: 10px 10px 0 0;'>
                <h1 style='color: white; margin: 0;'>The Focus Edge</h1>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0;'>Your Bi-Weekly Performance Digest</p>
            </div>
            <div style='padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;'>
                <p style='color: #666; font-size: 0.85rem; text-transform: uppercase; font-weight: bold;'>Featured Content from " . $article['source'] . "</p>
                <h2 style='margin-top: 0; color: #185a9d;'>" . $article['title'] . "</h2>
                <p>" . $article['excerpt'] . "</p>
                <div style='margin: 25px 0;'>
                    <a href='" . $article['url'] . "' style='background: #43cea2; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px;'>Read Full Article &rarr;</a>
                </div>
                
                <hr style='border: 0; border-top: 1px solid #eee; margin: 30px 0;'>
                
                <div style='background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;'>
                    <p style='margin-top: 0; font-weight: bold; color: #185a9d;'>Tool Spotlight: " . $featured_tool['name'][$lang] . "</p>
                    <p style='font-size: 0.95rem; margin-bottom: 15px;'>" . $featured_tool['desc'][$lang] . "</p>
                    <a href='$tool_url' style='color: #43cea2; text-decoration: none; font-weight: bold;'>Try it now &rarr;</a>
                </div>

                <p style='margin-top: 30px; font-size: 0.9rem; color: #666;'>Stay focused,<br>Serge from TimerHaven</p>
                <p style='font-size: 0.75rem; color: #999; text-align: center; margin-top: 40px;'>
                    Shared with focus from TimerHaven.com.<br>
                    <a href='$unsub_link' style='color: #185a9d;'>Unsubscribe</a>
                </p>
            </div>
        </body>
        </html>";

        try {
            $mail->clearAddresses();
            $mail->addAddress($to);
            $mail->Subject = $subject;
            $mail->Body    = $message;
            $mail->send();
            $count++;
        } catch (Exception $e) {
            echo "Failed to send to $to: " . $mail->ErrorInfo . "\n";
        }
        
        if ($batch_delay > 0) sleep($batch_delay);
        if ($count >= $batch_size) break;
    }

// --- 5. UPDATE STATE ---
if ($count > 0) {
    // Record sent article
    $stmt = $db->prepare("INSERT OR IGNORE INTO sent_articles (article_url) VALUES (?)");
    $stmt->execute([$article['url']]);
    
    // Update rotation state
    $update = $db->prepare("UPDATE newsletter_state SET last_tool_index = ?, last_sent_at = CURRENT_TIMESTAMP WHERE id = 1");
    $update->execute([$next_tool_index]);
    
    echo "Newsletter Sent Successfully: " . $article['title'] . " to $count subscribers.";
} else {
    echo "No emails sent.";
}
