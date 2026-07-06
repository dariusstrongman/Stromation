// stromation ai daily — feed render + subscribe
const AI_SUBSCRIBE_URL = 'https://n8n.stromation.com/webhook/ai-daily-subscribe';

// ---- feed ----
async function aiLoadFeed() {
  const todayEl = document.getElementById('today-card');
  const feedEl = document.getElementById('feed');
  if (!todayEl && !feedEl) return;
  try {
    const r = await fetch('data/ai-feed.json', { cache: 'no-store' });
    const items = await r.json();
    if (!items.length) throw new Error('empty');

    if (todayEl) {
      const t = items[0];
      todayEl.classList.remove('ai-skeleton');
      todayEl.innerHTML =
        '<div class="ai-date">' + aiEsc(t.date) + '</div>' +
        '<h3><a href="' + aiEsc(t.url) + '" target="_blank" rel="noopener">' + aiEsc(t.title) + '</a></h3>' +
        '<p class="ai-why">' + aiEsc(t.why || t.blurb || '') + '</p>' +
        (t.move ? '<div class="ai-move-box"><div class="ai-move-label">the move</div>' + aiEsc(t.move) + '</div>' : '') +
        '<span class="ai-src-tag">source: ' + aiEsc(t.src || '') + '</span>';
    }
    if (feedEl) {
      feedEl.innerHTML = items.slice(1, 25).map(i =>
        '<article class="ai-feed-card">' +
        '<div class="ai-date">' + aiEsc(i.date) + '</div>' +
        '<h4><a href="' + aiEsc(i.url) + '" target="_blank" rel="noopener">' + aiEsc(i.title) + '</a></h4>' +
        '<p>' + aiEsc(aiShorten(i.blurb || i.why || '', 150)) + '</p>' +
        '</article>').join('') ||
        '<p class="ai-skeleton">the archive fills up one day at a time. come back tomorrow.</p>';
    }
  } catch (e) {
    if (todayEl) todayEl.textContent = 'kitchen is warming up. first serving lands tomorrow 6am ct.';
  }
}
function aiEsc(s) { const d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }
function aiShorten(s, n) { s = String(s); return s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s; }

// ---- subscribe ----
document.querySelectorAll('[data-subscribe]').forEach(f => {
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const email = f.querySelector('[name=email]').value.trim();
    const hp = f.querySelector('[name=website]').value;
    const btn = f.querySelector('button');
    let msg = f.querySelector('.ai-sub-msg');
    if (!msg) { msg = document.createElement('div'); msg.className = 'ai-sub-msg'; f.appendChild(msg); }
    const orig = btn.textContent;
    btn.disabled = true; btn.textContent = 'signing you up…';
    try {
      const r = await fetch(AI_SUBSCRIBE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, website: hp, source: 'stromation_ai_daily', page: location.pathname })
      });
      const d = await r.json();
      if (d.ok) {
        msg.textContent = 'youre in. first serving tomorrow morning.'; msg.className = 'ai-sub-msg ok'; f.reset();
        if (typeof gtag === 'function') gtag('event', 'newsletter_subscribe', { source: 'ai_daily' });
      } else throw new Error(d.error || 'failed');
    } catch (err) {
      msg.textContent = 'that didnt go through, try again in a sec'; msg.className = 'ai-sub-msg err';
    }
    btn.disabled = false; btn.textContent = orig;
  });
});

// ---- tools search ----
const aiSearch = document.querySelector('.ai-tool-search');
if (aiSearch) {
  aiSearch.addEventListener('input', () => {
    const q = aiSearch.value.toLowerCase();
    document.querySelectorAll('.ai-tool-card').forEach(c => {
      c.style.display = c.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
    document.querySelectorAll('.ai-cat-block').forEach(b => {
      const any = [...b.querySelectorAll('.ai-tool-card')].some(c => c.style.display !== 'none');
      b.style.display = any ? '' : 'none';
    });
  });
}

const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

aiLoadFeed();
