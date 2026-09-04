// Theme Switcher Logic
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggleIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    if (!document.startViewTransition) {
        setTheme(newTheme);
        return;
    }
    
    // Disable CSS transitions during view transition to prevent conflicts
    document.documentElement.classList.add('theme-transitioning');
    
    const transition = document.startViewTransition(() => {
        setTheme(newTheme);
    });
    
    transition.finished.finally(() => {
        document.documentElement.classList.remove('theme-transitioning');
    });
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeToggleIcon(theme);
}

function updateThemeToggleIcon(theme) {
    const icon = document.querySelector('.theme-toggle svg') || document.querySelector('.theme-toggle i');
    if (!icon) return;
    if (theme === 'dark') {
        icon.setAttribute('class', 'feather feather-sun');
        icon.innerHTML = `<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>`;
    } else {
        icon.setAttribute('class', 'feather feather-moon');
        icon.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>`;
    }
}

// Toast Notifications Helper
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        padding: 12px 20px;
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border-left: 4px solid var(--accent-color);
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease forwards;
        margin-top: 10px;
    `;

    if (type === 'success') toast.style.borderLeftColor = 'var(--success)';
    if (type === 'warning') toast.style.borderLeftColor = 'var(--warning)';
    if (type === 'danger') toast.style.borderLeftColor = 'var(--danger)';

    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Firebase Analytics & Config Integration
let appAnalytics = null;
function initFirebase(config) {
    if (typeof firebase !== 'undefined') {
        try {
            // Initialize Firebase App
            const app = firebase.initializeApp(config);
            // Initialize Analytics
            appAnalytics = firebase.analytics(app);
            console.log("Firebase initialized successfully with Analytics ID:", config.measurementId);
        } catch (e) {
            console.error("Firebase SDK init failed, running in sandbox mode:", e);
        }
    } else {
        console.log("Firebase CDN not loaded or running offline. Sandbox reporting active.");
    }
}

function logFirebaseEvent(eventName, params = {}) {
    if (appAnalytics) {
        appAnalytics.logEvent(eventName, params);
        console.log(`[Firebase Analytics] Event Logged: "${eventName}"`, params);
    } else {
        console.log(`[Firebase Analytics Sandbox] Log Event: "${eventName}"`, params);
    }
}

// Live Listing NLP Moderation Check
let moderationTimeout = null;
function initLiveModeration() {
    const titleInput = document.getElementById('listing-title');
    const descInput = document.getElementById('listing-description');
    const priceInput = document.getElementById('listing-price');
    const catInput = document.getElementById('listing-category');
    const modBox = document.getElementById('moderation-results');

    if (!titleInput || !descInput || !priceInput || !catInput || !modBox) return;

    const runCheck = () => {
        clearTimeout(moderationTimeout);
        moderationTimeout = setTimeout(() => {
            const title = titleInput.value;
            const description = descInput.value;
            const price = parseFloat(priceInput.value) || 0;
            const category_id = catInput.value;

            if (description.length < 5 && title.length < 5) {
                modBox.innerHTML = '';
                return;
            }

            fetch('/api/moderate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, description, price, category_id })
            })
            .then(res => res.json())
            .then(data => {
                if (data.is_flagged) {
                    let reasonsHtml = data.reasons.map(r => `<li>⚠️ ${r}</li>`).join('');
                    modBox.innerHTML = `
                        <div class="moderation-flag">
                            <div>
                                <strong>AI Moderation Flags Detected:</strong>
                                <ul style="margin-left: 20px; margin-top: 6px; font-size:12px;">${reasonsHtml}</ul>
                                <p style="font-size:11px; margin-top:8px; opacity:0.8;">Warning: Listings with flags will be auto-flagged and subject to admin review.</p>
                            </div>
                        </div>
                    `;
                } else {
                    modBox.innerHTML = `
                        <div class="moderation-ok">
                            <strong>✅ AI Status: Safe to List</strong>
                            <p style="font-size: 11px; margin-top: 4px;">No suspicious keywords, price outliers, or external contact details found.</p>
                        </div>
                    `;
                }
            })
            .catch(err => console.error("Moderation API Error:", err));
        }, 500);
    };

    titleInput.addEventListener('input', runCheck);
    descInput.addEventListener('input', runCheck);
    priceInput.addEventListener('input', runCheck);
    catInput.addEventListener('change', runCheck);
}

// Live Search AI Ranking suggestions
function initLiveSearchSuggestions() {
    const searchInput = document.getElementById('search-input');
    const suggestBox = document.getElementById('search-suggestions');
    if (!searchInput || !suggestBox) return;

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        if (query.length < 2) {
            suggestBox.style.display = 'none';
            return;
        }

        fetch(`/api/search_suggest?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                suggestBox.innerHTML = data.results.map(item => `
                    <a href="/product/${item.id}" class="suggestion-item" style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; text-decoration:none; color:var(--text-primary); border-bottom:1px solid var(--border-color);">
                        <span>🔍 ${item.title}</span>
                        <span style="font-size:10px; background:var(--border-color); padding:2px 6px; border-radius:10px; color:var(--text-secondary);">Score: ${item.score}</span>
                    </a>
                `).join('');
                suggestBox.style.display = 'block';
            } else {
                suggestBox.style.display = 'none';
            }
        })
        .catch(err => console.error("Search suggestion error:", err));
    });

    document.addEventListener('click', (e) => {
        if (e.target !== searchInput) {
            suggestBox.style.display = 'none';
        }
    });
}

// Trigger animations & document setup
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLiveModeration();
    initLiveSearchSuggestions();

    // Setup Theme Click Listener
    const themeBtn = document.querySelector('.theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleTheme);
    }
});
