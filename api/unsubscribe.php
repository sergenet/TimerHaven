<?php
/**
 * TimerHaven Newsletter Unsubscribe Handler
 */

header('Content-Type: text/html; charset=UTF-8');

// Configuration
$db_path = __DIR__ . '/../data/subscribers.db';

if (isset($_GET['email'])) {
    $email = urldecode($_GET['email']);
    
    try {
        $db = new PDO("sqlite:$db_path");
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        $stmt = $db->prepare("UPDATE subscribers SET status = 'unsubscribed' WHERE email = ?");
        $stmt->execute([$email]);
        
        $message = "<h1>Successfully Unsubscribed</h1><p>The email <strong>" . htmlspecialchars($email) . "</strong> has been removed from our active mailing list. We're sorry to see you go!</p>";
    } catch (PDOException $e) {
        $message = "<h1>Error</h1><p>Something went wrong. Please try again later or contact us directly.</p>";
    }
} else {
    $message = "<h1>Invalid Link</h1><p>This unsubscribe link appears to be invalid.</p>";
}

// Simple HTML wrapper for the message
echo '<!DOCTYPE html><html><head><title>Unsubscribe - TimerHaven</title><style>body{font-family:sans-serif;text-align:center;padding:50px;} .container{max-width:500px;margin:0 auto;border:1px solid #ddd;padding:30px;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,0.1);}</style></head><body><div class="container">' . $message . '<br><a href="https://timerhaven.com">Back to TimerHaven</a></div></body></html>';
?>
