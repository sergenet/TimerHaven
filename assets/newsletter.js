
function initNewsletter() {
    const forms = document.querySelectorAll('.newsletter-form');
    if (forms.length === 0) return;

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const message = form.querySelector('#newsletterMessage');
            const data = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');

            if (submitBtn) submitBtn.disabled = true;

            // Capture current page language
            const lang = document.documentElement.lang || 'en';
            data.append('lang', lang);

            fetch('/api/subscribe.php', {
                method: 'POST',
                body: data
            })
                .then(response => response.json())
                .then(result => {
                    if (result.status === 'success') {
                        showThankYouModal();
                        form.reset();
                        if (message) message.style.display = 'none';
                    } else if (result.status === 'duplicate') {
                        if (message) {
                            message.textContent = result.message;
                            message.style.display = 'block';
                            message.style.color = '#43cea2'; // Success green for "already subbed"
                        }
                        form.reset();
                    } else {
                        if (message) {
                            message.textContent = result.message;
                            message.style.display = 'block';
                            message.style.color = '#ff9999';
                        }
                    }
                })
                .catch(error => {
                    if (message) {
                        message.textContent = 'Something went wrong. Please try again.';
                        message.style.display = 'block';
                        message.style.color = '#ff9999';
                    }
                })
                .finally(() => {
                    if (submitBtn) submitBtn.disabled = false;
                });
        });
    });
}

function showThankYouModal() {
    const modalHtml = `
        <div class="thank-you-overlay" id="thankYouOverlay">
            <div class="thank-you-card">
                <span class="success-icon"><i class="fas fa-check-circle"></i></span>
                <h1>You're on the list!</h1>
                <p>Thank you for joining the TimerHaven community. We're excited to help you transform your productivity.</p>
                <ul class="steps-list">
                    <li><span class="step-num">1</span> Check your inbox for a confirmation email</li>
                    <li><span class="step-num">2</span> Add <strong>support@timerhaven.com</strong> to your contacts</li>
                    <li><span class="step-num">3</span> Start your first session using our tools below</li>
                </ul>
                <div style="margin-top: 2rem;">
                    <button class="btn-modal-close" onclick="window.location.href='/index.html';">Explore Our Tools</button>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    // Escape to close
    const handleEsc = (e) => {
        if (e.key === 'Escape') {
            const overlay = document.getElementById('thankYouOverlay');
            if (overlay) overlay.remove();
            document.removeEventListener('keydown', handleEsc);
        }
    };
    document.addEventListener('keydown', handleEsc);
}

document.addEventListener('DOMContentLoaded', initNewsletter);
