<?php
/**
 * TimerHaven Weekly Digest Cron Job
 * Designed for Namecheap Shared Hosting.
 * Compiles latest blog posts and sends to subscribers.
 */

// Configuration
$db_path = __DIR__ . '/../data/subscribers.db';
$blog_index_path = __DIR__ . '/../blog/index.html';
$sender_email = "newsletter@timerhaven.com";

// 1. Fetch Latest Articles from blog/index.html
$articles = [];
if (file_exists($blog_index_path)) {
    $html = file_get_contents($blog_index_path);
    // Extract first 3 articles (Title, Excerpt, Link)
    // Simple regex for our standardized structure
    preg_match_all('/<article class="article-card">.*?<a\s+href="(?P<link>\/blog\/.*?)".*?class="article-title">(?P<title>.*?)<\/a>.*?<p\s+class="article-excerpt">(?P<excerpt>.*?)<\/p>/s', $html, $matches, PREG_SET_ORDER);
    
    $articles = array_slice($matches, 0, 3);
}

if (empty($articles)) {
    die("No articles found to send.");
}

// 2. Connect to Database
try {
    $db = new PDO("sqlite:$db_path");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $stmt = $db->query("SELECT email FROM subscribers WHERE status = 'active'");
    $subscribers = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (PDOException $e) {
    die("Database error: " . $e->getMessage());
}

if (empty($subscribers)) {
    die("No active subscribers.");
}

// 3. Compile Email Content
$subject = "Your Weekly TimerHaven Digest: Master Your Energy";
$headers = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
$headers .= "From: TimerHaven Newsletter <$sender_email>" . "\r\n";

$article_html = "";
foreach ($articles as $art) {
    $link = "https://timerhaven.com" . $art['link'];
    $title = trim($art['title']);
    $excerpt = trim($art['excerpt']);
    
    $article_html .= "
        <div style='margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px;'>
            <h3 style='margin: 0 0 10px 0;'><a href='$link' style='color: #185a9d; text-decoration: none;'>$title</a></h3>
            <p style='color: #666; margin: 0 0 15px 0;'>$excerpt</p>
            <a href='$link' style='display: inline-block; padding: 10px 20px; background: #43cea2; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;'>Read More</a>
        </div>
    ";
}

$message_template = '
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #185a9d 0%, #43cea2 100%); border-radius: 10px 10px 0 0;">
        <h1 style="color: white; margin: 0;">TimerHaven Weekly Digest</h1>
    </div>
    <div style="padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
        <p>Hello Focus Master,</p>
        <p>Here are this week\'s top resources to help you master your focus and energy:</p>
        
        ' . $article_html . '

        <p>Stay focused,<br>Serge from TimerHaven</p>
        
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 0.8rem; color: #888;">
            You received this because you master focus at TimerHaven.com.<br>
            <a href="https://timerhaven.com/api/unsubscribe.php?email={{EMAIL}}">Unsubscribe</a>
        </p>
    </div>
</body>
</html>
';

// 4. Send to each subscriber (Batching would be better for massive lists, but this works for starter growth)
foreach ($subscribers as $email) {
    $personal_message = str_replace('{{EMAIL}}', urlencode($email), $message_template);
    @mail($email, $subject, $personal_message, $headers);
}

echo "Success: Compiled and sent digest to " . count($subscribers) . " subscribers.";
?>
