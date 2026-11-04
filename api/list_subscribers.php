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
 * TimerHaven Subscriber Manager
 * Password Protected Dashboard with Bulk/All Delete, CSV Export & Password Change
 */

// --- CONFIGURATION ---
$default_password = th_secret('admin_default_password', 'TH_ADMIN_PASSWORD');  // Fallback if no DB password set yet
$db_path = __DIR__ . '/../data/subscribers.db';

session_start();

// --- DATABASE CONNECTION ---
try {
    $db = new PDO("sqlite:$db_path");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    die("Database access failed: " . $e->getMessage());
}

// --- SETTINGS TABLE (for password storage) ---
$db->exec("CREATE TABLE IF NOT EXISTS admin_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)");

// --- PASSWORD HELPER ---
function getStoredPassword($db, $default_password) {
    $stmt = $db->prepare("SELECT value FROM admin_settings WHERE key = 'admin_password_hash'");
    $stmt->execute();
    $row = $stmt->fetch();
    if ($row) {
        return $row['value']; // Returns the hash
    }
    return null; // No custom password set, use default
}

function verifyPassword($input, $db, $default_password) {
    $hash = getStoredPassword($db, $default_password);
    if ($hash) {
        return password_verify($input, $hash);
    }
    // Fallback to plaintext default
    return $input === $default_password;
}

// Logout handler
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: list_subscribers.php");
    exit;
}

// Authentication
$authenticated = isset($_SESSION['th_admin_auth']) && $_SESSION['th_admin_auth'] === true;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['auth_password'])) {
    if (verifyPassword($_POST['auth_password'], $db, $default_password)) {
        $_SESSION['th_admin_auth'] = true;
        header("Location: list_subscribers.php");
        exit;
    } else {
        $error = "Incorrect password.";
    }
}

// --- CSV EXPORT HANDLER ---
if ($authenticated && isset($_GET['export'])) {
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="th_subscribers_' . date('Y-m-d') . '.csv"');
    $output = fopen('php://output', 'w');
    fputcsv($output, ['ID', 'Email', 'Language', 'Status', 'Date Subscribed']);
    $query = $db->query("SELECT * FROM subscribers ORDER BY created_at DESC");
    while ($row = $query->fetch()) {
        fputcsv($output, $row);
    }
    fclose($output);
    exit;
}

// --- CHANGE PASSWORD HANDLER ---
$pw_success = '';
$pw_error = '';
if ($authenticated && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['change_password'])) {
    $current = $_POST['current_password'] ?? '';
    $new = $_POST['new_password'] ?? '';
    $confirm = $_POST['confirm_password'] ?? '';

    if (!verifyPassword($current, $db, $default_password)) {
        $pw_error = "Current password is incorrect.";
    } elseif (strlen($new) < 4) {
        $pw_error = "New password must be at least 4 characters.";
    } elseif ($new !== $confirm) {
        $pw_error = "New passwords do not match.";
    } else {
        $hash = password_hash($new, PASSWORD_DEFAULT);
        $stmt = $db->prepare("INSERT OR REPLACE INTO admin_settings (key, value) VALUES ('admin_password_hash', ?)");
        $stmt->execute([$hash]);
        $pw_success = "Password changed successfully!";
    }
}

// --- DELETION HANDLERS ---
if ($authenticated && $_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['delete_email']) && !empty($_POST['delete_email'])) {
        $stmt = $db->prepare("DELETE FROM subscribers WHERE email = ?");
        $stmt->execute([$_POST['delete_email']]);
        header("Location: list_subscribers.php?msg=deleted");
        exit;
    } elseif (isset($_POST['bulk_delete']) && !empty($_POST['selected_emails'])) {
        $placeholders = str_repeat('?,', count($_POST['selected_emails']) - 1) . '?';
        $stmt = $db->prepare("DELETE FROM subscribers WHERE email IN ($placeholders)");
        $stmt->execute($_POST['selected_emails']);
        header("Location: list_subscribers.php?msg=bulk_deleted");
        exit;
    } elseif (isset($_POST['delete_all'])) {
        $db->exec("DELETE FROM subscribers");
        header("Location: list_subscribers.php?msg=all_deleted");
        exit;
    }
}

// --- DATA RETRIEVAL ---
$subscribers = [];
if ($authenticated) {
    $subscribers = $db->query("SELECT * FROM subscribers ORDER BY created_at DESC")->fetchAll();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subscriber Manager — TimerHaven</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <style>
        body { background: #f8fafc; font-family: 'Inter', sans-serif; color: #1e293b; }
        .admin-card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); overflow: hidden; }
        .header-gradient { background: linear-gradient(135deg, #185a9d 0%, #43cea2 100%); color: white; padding: 2rem 1rem; border-radius: 12px 12px 0 0; }
        .btn-th { background: linear-gradient(135deg, #185a9d, #43cea2); border: none; color: white; border-radius: 8px; font-weight: 600; transition: all 0.3s; }
        .btn-th:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(24, 90, 157, 0.3); color: white; }
        .status-badge { font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; font-weight: 600; text-transform: uppercase; }
        .status-active { background: #dcfce7; color: #166534; }
        .table { margin-bottom: 0; }
        .form-check-input:checked { background-color: #185a9d; border-color: #185a9d; }
    </style>
</head>
<body>

    <div class="container py-5">
        <?php if (!$authenticated): ?>
            <!-- Login View -->
            <div class="row justify-content-center">
                <div class="col-md-5">
                    <div class="admin-card">
                        <div class="header-gradient text-center">
                            <h2 class="mb-0">TimerHaven Panel</h2>
                            <p class="small opacity-75 mt-1">Subscriber Management</p>
                        </div>
                        <div class="p-4">
                            <form method="POST">
                                <div class="mb-4">
                                    <label class="form-label fw-bold small text-uppercase">Admin Password</label>
                                    <input type="password" name="auth_password" class="form-control form-control-lg border-2" placeholder="••••••••" required autofocus>
                                </div>
                                <?php if (isset($error)): ?>
                                    <div class="alert alert-danger py-2 small"><?= $error ?></div>
                                <?php endif; ?>
                                <button type="submit" class="btn btn-th w-100 py-2 fs-5">Login</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        <?php else: ?>
            <!-- Dashboard View -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h1 class="h3 mb-0 fw-bold">Newsletter Subscribers</h1>
                    <p class="text-muted small mb-0">Manage your subscriber list</p>
                </div>
                <div class="d-flex gap-2">
                    <a href="?export=1" class="btn btn-outline-dark btn-sm fw-bold"><i class="fas fa-file-csv me-1"></i> Export CSV</a>
                    <button type="button" class="btn btn-outline-secondary btn-sm fw-bold" data-bs-toggle="modal" data-bs-target="#changePasswordModal"><i class="fas fa-cog"></i></button>
                    <a href="?logout=1" class="btn btn-danger btn-sm fw-bold"><i class="fas fa-sign-out-alt"></i></a>
                </div>
            </div>

            <?php if (isset($_GET['msg'])): ?>
                <div class="alert alert-success alert-dismissible fade show py-2 small" role="alert">
                    <i class="fas fa-check-circle me-1"></i> 
                    <?php
                        if ($_GET['msg'] === 'deleted') echo 'Subscriber removed successfully.';
                        elseif ($_GET['msg'] === 'bulk_deleted') echo 'Selected subscribers removed.';
                        elseif ($_GET['msg'] === 'all_deleted') echo 'All subscribers have been removed.';
                    ?>
                    <button type="button" class="btn-close py-2" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            <?php endif; ?>

            <?php if ($pw_success): ?>
                <div class="alert alert-success alert-dismissible fade show py-2 small" role="alert">
                    <i class="fas fa-key me-1"></i> <?= $pw_success ?>
                    <button type="button" class="btn-close py-2" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            <?php endif; ?>

            <form method="POST" id="bulk-delete-form">
                <div class="admin-card">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4" style="width: 40px;">
                                        <input type="checkbox" class="form-check-input" id="select-all">
                                    </th>
                                    <th>Email Address</th>
                                    <th>Language</th>
                                    <th>Status</th>
                                    <th>Subscribed At</th>
                                    <th class="text-end pe-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php if (empty($subscribers)): ?>
                                    <tr>
                                        <td colspan="6" class="text-center py-5 text-muted">
                                            <i class="fas fa-users-slash d-block mb-3 fs-3 opacity-25"></i>
                                            No subscribers found in the database.
                                        </td>
                                    </tr>
                                <?php else: ?>
                                    <?php foreach ($subscribers as $sub): ?>
                                        <tr>
                                            <td class="ps-4">
                                                <input type="checkbox" name="selected_emails[]" value="<?= htmlspecialchars($sub['email']) ?>" class="form-check-input sub-checkbox">
                                            </td>
                                            <td class="fw-semibold"><?= htmlspecialchars($sub['email']) ?></td>
                                            <td><span class="text-uppercase text-secondary small fw-bold"><?= htmlspecialchars($sub['lang']) ?></span></td>
                                            <td><span class="status-badge status-active"><?= htmlspecialchars($sub['status']) ?></span></td>
                                            <td class="text-muted small"><?= date('M j, Y H:i', strtotime($sub['created_at'])) ?></td>
                                            <td class="text-end pe-4">
                                                <button type="button" onclick="confirmSingleDelete('<?= htmlspecialchars($sub['email']) ?>')" class="btn btn-link btn-sm text-danger p-0"><i class="fas fa-trash-alt"></i></button>
                                            </td>
                                        </tr>
                                    <?php endforeach; ?>
                                <?php endif; ?>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="mt-3 d-flex justify-content-between align-items-center px-2">
                    <div class="text-muted small fw-bold">
                        TOTAL: <?= count($subscribers) ?>
                    </div>
                    <div class="d-flex gap-2">
                        <button type="submit" name="bulk_delete" id="bulk-delete-btn" class="btn btn-danger btn-sm px-3 fw-bold invisible" onclick="return confirm('Are you sure you want to delete the selected subscribers?')">
                            <i class="fas fa-trash me-1"></i> Delete Selected
                        </button>
                        <?php if (!empty($subscribers)): ?>
                        <button type="submit" name="delete_all" class="btn btn-outline-danger btn-sm px-3 fw-bold" onclick="return confirm('⚠️ DANGER: This will permanently delete ALL <?= count($subscribers) ?> subscribers. Are you absolutely sure?')">
                            <i class="fas fa-trash-alt me-1"></i> Delete All
                        </button>
                        <?php endif; ?>
                    </div>
                </div>
                
                <!-- Hidden single delete field -->
                <input type="hidden" name="delete_email" id="single-delete-email">
            </form>

            <!-- Change Password Modal -->
            <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="changePasswordModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content" style="border-radius: 16px; overflow: hidden;">
                        <div class="header-gradient py-3 text-center">
                            <h5 class="mb-0"><i class="fas fa-key me-2"></i>Change Password</h5>
                        </div>
                        <div class="modal-body p-4">
                            <?php if ($pw_error): ?>
                                <div class="alert alert-danger py-2 small"><?= $pw_error ?></div>
                            <?php endif; ?>
                            <form method="POST">
                                <div class="mb-3">
                                    <label class="form-label fw-bold small">Current Password</label>
                                    <input type="password" name="current_password" class="form-control" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-bold small">New Password</label>
                                    <input type="password" name="new_password" class="form-control" minlength="4" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label fw-bold small">Confirm New Password</label>
                                    <input type="password" name="confirm_password" class="form-control" minlength="4" required>
                                </div>
                                <button type="submit" name="change_password" class="btn btn-th w-100 py-2 fw-bold">
                                    <i class="fas fa-save me-1"></i> Update Password
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

        <?php endif; ?>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const selectAll = document.getElementById('select-all');
        const checkboxes = document.querySelectorAll('.sub-checkbox');
        const bulkBtn = document.getElementById('bulk-delete-btn');
        const form = document.getElementById('bulk-delete-form');
        const singleInput = document.getElementById('single-delete-email');

        if (selectAll) {
            selectAll.addEventListener('change', function() {
                checkboxes.forEach(cb => cb.checked = selectAll.checked);
                toggleBulkBtn();
            });

            checkboxes.forEach(cb => {
                cb.addEventListener('change', toggleBulkBtn);
            });
        }

        function toggleBulkBtn() {
            const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
            if (checkedCount > 0) {
                bulkBtn.classList.remove('invisible');
            } else {
                bulkBtn.classList.add('invisible');
            }
        }

        window.confirmSingleDelete = function(email) {
            if (confirm("Permanently remove " + email + "?")) {
                singleInput.value = email;
                form.submit();
            }
        };

        // Auto-open modal if there was a password error
        <?php if ($pw_error): ?>
        var pwModal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
        pwModal.show();
        <?php endif; ?>
    });
    </script>
</body>
</html>
