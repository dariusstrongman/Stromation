/**
 * STROMATION - WORKFLOW REPLACEMENT STUDIO
 * Clean JavaScript for Professional Site
 */

// ==========================================
// FORM ENDPOINT CONFIGURATION
// ==========================================
const FORM_ENDPOINT = 'https://formspree.io/f/mkobkvwl';
const N8N_WEBHOOK_URL = 'https://n8n.myaibuffet.com/webhook/lead-capture';

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initHeaderScroll();
    initScrollAnimations();
    initHeroParallax();
    initStepsProgress();
    initCountUp();
    initSmoothScroll();
    initActiveNavHighlight();
    initContactForm();
    initNewsletterForm();
    initFaqAccordion();
});

// ==========================================
// MOBILE MENU TOGGLE
// ==========================================
function initMobileMenu() {
    const toggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.getElementById('navLinks');

    if (!toggle || !navLinks) return;

    toggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        toggle.classList.toggle('active');
        toggle.setAttribute('aria-expanded', navLinks.classList.contains('active'));
    });

    // Keyboard support for toggle
    toggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggle.click();
        }
    });

    // Close menu when clicking a link
    const links = navLinks.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            toggle.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
            toggle.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
        }
    });
}

// ==========================================
// HEADER SCROLL EFFECT
// ==========================================
function initHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}

// ==========================================
// SCROLL ANIMATIONS
// ==========================================
function initScrollAnimations() {
    const animElements = document.querySelectorAll('.fade-in, .slide-left, .slide-right');

    if (animElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animElements.forEach(el => observer.observe(el));
}

// ==========================================
// HERO PARALLAX ON SCROLL
// ==========================================
function initHeroParallax() {
    var hero = document.querySelector('.hero');
    if (!hero) return;

    // Respect reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var heroText = hero.querySelector('.hero-text');
    var heroIllustration = hero.querySelector('.hero-illustration');
    var isMobile = window.innerWidth < 768;
    var ticking = false;

    window.addEventListener('resize', function() {
        isMobile = window.innerWidth < 768;
    });

    window.addEventListener('scroll', function() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function() {
            if (isMobile) { ticking = false; return; }

            var scrollY = window.pageYOffset;
            var heroHeight = hero.offsetHeight;

            if (scrollY < heroHeight + 200) {
                var opacity = Math.max(0, 1 - scrollY / 600);
                var textY = scrollY * 0.3;
                var svgY = scrollY * -0.15;

                if (heroText) {
                    heroText.style.transform = 'translateY(' + textY + 'px)';
                    heroText.style.opacity = opacity;
                }
                if (heroIllustration) {
                    heroIllustration.style.transform = 'translateY(' + svgY + 'px)';
                    heroIllustration.style.opacity = opacity;
                }
            }
            ticking = false;
        });
    });
}

// ==========================================
// STEPS PROGRESS LINE
// ==========================================
function initStepsProgress() {
    var wrapper = document.querySelector('.process-grid-wrapper');
    if (!wrapper) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var fill = wrapper.querySelector('.steps-progress-fill');
    var steps = wrapper.querySelectorAll('.process-card[data-step]');
    if (!fill || steps.length === 0) return;

    var ticking = false;
    var activated = {};

    window.addEventListener('scroll', function() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function() {
            // Hide progress on mobile
            if (window.innerWidth < 1024) { ticking = false; return; }

            var rect = wrapper.getBoundingClientRect();
            var windowH = window.innerHeight;
            var sectionTop = rect.top;
            var sectionH = rect.height;

            // Calculate progress: 0 when section enters viewport, 1 when it's centered
            var start = windowH * 0.8;
            var end = windowH * 0.3;
            var progress = 0;

            if (sectionTop < start) {
                progress = Math.min(1, Math.max(0, (start - sectionTop) / (start - end)));
            }

            fill.style.transform = 'scaleX(' + progress + ')';

            // Activate steps based on progress
            for (var i = 0; i < steps.length; i++) {
                var threshold = (i + 0.5) / steps.length;
                if (progress >= threshold) {
                    if (!activated[i]) {
                        steps[i].classList.add('step-active');
                        activated[i] = true;
                    }
                }
            }

            ticking = false;
        });
    });
}

// ==========================================
// COUNT-UP ANIMATION
// ==========================================
function initCountUp() {
    var metrics = document.querySelectorAll('.metric-value[data-count]');
    if (metrics.length === 0) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        // Just show final values immediately
        metrics.forEach(function(el) {
            var target = el.getAttribute('data-count');
            el.textContent = target;
        });
        return;
    }

    function easeOutExpo(t) {
        return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
    }

    function animateCount(el) {
        var target = el.getAttribute('data-count');

        // Non-numeric values (like "24/7") just fade in
        if (isNaN(parseInt(target))) {
            el.textContent = target;
            return;
        }

        var end = parseInt(target);
        var duration = 1500;
        var start = performance.now();

        function update(now) {
            var elapsed = now - start;
            var progress = Math.min(elapsed / duration, 1);
            var easedProgress = easeOutExpo(progress);
            var current = Math.round(easedProgress * end);
            el.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                el.textContent = end;
            }
        }

        requestAnimationFrame(update);
    }

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateCount(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    metrics.forEach(function(el) { observer.observe(el); });
}

// ==========================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ==========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ==========================================
// ACTIVE NAV HIGHLIGHT
// ==========================================
function initActiveNavHighlight() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        } else if (!link.classList.contains('cta-nav')) {
            link.classList.remove('active');
        }
    });
}

// ==========================================
// N8N WEBHOOK - FIRE AND FORGET
// ==========================================
function sendToN8N(formData) {
    try {
        // Determine source from the current page
        const page = window.location.pathname.split('/').pop() || '';
        let source = 'website_contact';
        if (page === 'audit.html' || page.startsWith('audit')) {
            source = 'website_audit';
        }

        // Split full name into first_name / last_name
        const fullName = (formData.get('name') || '').trim();
        const nameParts = fullName.split(/\s+/);
        const firstName = nameParts[0] || '';
        const lastName = nameParts.slice(1).join(' ') || '';

        // Build notes from workflow description + extra fields
        const noteParts = [];
        const workflow = (formData.get('workflow') || '').trim();
        if (workflow) noteParts.push(workflow);
        const company = (formData.get('company') || '').trim();
        if (company) noteParts.push('Company/Role: ' + company);
        const tools = (formData.get('tools') || '').trim();
        if (tools) noteParts.push('Tools: ' + tools);
        const volume = (formData.get('volume') || '').trim();
        if (volume) noteParts.push('Volume: ' + volume);
        const outcome = (formData.get('outcome') || '').trim();
        if (outcome) noteParts.push('Outcome: ' + outcome);
        const budget = (formData.get('budget') || '').trim();
        if (budget) noteParts.push('Budget: ' + budget);
        const timeline = (formData.get('timeline') || '').trim();
        if (timeline) noteParts.push('Timeline: ' + timeline);

        const payload = {
            first_name: firstName,
            last_name: lastName,
            email: (formData.get('email') || '').trim(),
            phone: (formData.get('phone') || '').trim(),
            source: source,
            notes: noteParts.join(' | '),
            landing_page_url: window.location.href,
            sms_opt_in: formData.get('sms_consent') === 'yes'
        };

        // Fire-and-forget: don't await, don't block UI
        fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).catch(function() {
            // Silently ignore — Formspree is the primary path
        });
    } catch (e) {
        // Never break the user experience
    }
}

// ==========================================
// CONTACT FORM HANDLING (FORMSPREE)
// ==========================================
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;

    // Create message container if not exists
    let messageContainer = contactForm.querySelector('.form-message');
    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.className = 'form-message';
        messageContainer.style.cssText = 'padding: 1rem; border-radius: 8px; margin-bottom: 1rem; display: none;';
        contactForm.insertBefore(messageContainer, contactForm.firstChild);
    }

    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        // Disable button and show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        messageContainer.style.display = 'none';

        // Build form data
        const formData = new FormData(this);

        // Handle checkbox tools - combine into comma-separated string
        const tools = formData.getAll('tools');
        formData.delete('tools');
        if (tools.length > 0) {
            formData.append('tools', tools.join(', '));
        }

        try {
            const response = await fetch(FORM_ENDPOINT, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                // Send to n8n WF01 (fire-and-forget, before form reset)
                sendToN8N(formData);

                // GA4 conversion tracking
                var source = (window.location.pathname.indexOf('audit') !== -1) ? 'website_audit' : 'website_contact';
                gtag('event', 'generate_lead', { event_category: 'form', event_label: source, value: 1 });

                // Success
                messageContainer.style.display = 'block';
                messageContainer.style.background = 'rgba(16, 185, 129, 0.1)';
                messageContainer.style.border = '1px solid rgba(16, 185, 129, 0.3)';
                messageContainer.style.color = '#059669';
                messageContainer.innerHTML = '<strong>Thanks!</strong> We reply within 1 business day. If this is a fit, we\'ll send next steps for the Free Automation Audit.';
                this.reset();
            } else {
                throw new Error('Form submission failed');
            }
        } catch (error) {
            // Error
            messageContainer.style.display = 'block';
            messageContainer.style.background = 'rgba(239, 68, 68, 0.1)';
            messageContainer.style.border = '1px solid rgba(239, 68, 68, 0.3)';
            messageContainer.style.color = '#DC2626';
            messageContainer.innerHTML = '<strong>Something went wrong.</strong> Please try again or email us directly at <a href="mailto:support@stromation.com">support@stromation.com</a>.';
        } finally {
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

// ==========================================
// NEWSLETTER FORM HANDLING
// ==========================================
function initNewsletterForm() {
    var form = document.getElementById('newsletterForm');
    if (!form) return;
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        var btn = this.querySelector('button');
        var msg = document.getElementById('newsletterMessage');
        var email = this.querySelector('input[name="email"]').value.trim();
        btn.disabled = true;
        btn.textContent = 'Subscribing...';
        try {
            await fetch('https://n8n.myaibuffet.com/webhook/lead-capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, source: 'newsletter_signup', first_name: '', last_name: '', landing_page_url: window.location.href })
            });
            msg.style.display = 'block';
            msg.style.color = '#059669';
            msg.textContent = 'Subscribed! Check your inbox.';
            gtag('event', 'sign_up', { event_category: 'newsletter' });
            this.reset();
        } catch(err) {
            msg.style.display = 'block';
            msg.style.color = '#DC2626';
            msg.textContent = 'Something went wrong. Try again.';
        }
        btn.disabled = false;
        btn.textContent = 'Subscribe';
    });
}

// ==========================================
// FAQ ACCORDION
// ==========================================
function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) return;

    faqItems.forEach(function(item) {
        const button = item.querySelector('.faq-question');
        if (!button) return;

        button.addEventListener('click', function() {
            const isActive = item.classList.contains('active');

            // Close all items
            faqItems.forEach(function(other) {
                other.classList.remove('active');
                var otherBtn = other.querySelector('.faq-question');
                if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
            });

            // Open clicked item if it was closed
            if (!isActive) {
                item.classList.add('active');
                button.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

// ==========================================
// GA4 CTA CLICK TRACKING
// ==========================================
document.addEventListener('click', function(e) {
    var btn = e.target.closest('a, button');
    if (!btn) return;
    var text = (btn.textContent || '').trim();
    if (/get a free audit|request your audit/i.test(text)) {
        gtag('event', 'cta_click', { event_category: 'engagement', event_label: text });
    }
});
