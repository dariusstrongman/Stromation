/**
 * STROMATION - WORKFLOW REPLACEMENT STUDIO
 * Clean JavaScript for Professional Site
 */

// ==========================================
// FORM ENDPOINT CONFIGURATION
// ==========================================
const FORM_ENDPOINT = 'https://formspree.io/f/mkobkvwl';

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initHeaderScroll();
    initScrollAnimations();
    initSmoothScroll();
    initActiveNavHighlight();
    initContactForm();
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
    });

    // Close menu when clicking a link
    const links = navLinks.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            toggle.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
            toggle.classList.remove('active');
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
    const fadeElements = document.querySelectorAll('.fade-in');

    if (fadeElements.length === 0) return;

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

    fadeElements.forEach(el => observer.observe(el));
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
                // Success
                messageContainer.style.display = 'block';
                messageContainer.style.background = 'rgba(16, 185, 129, 0.1)';
                messageContainer.style.border = '1px solid rgba(16, 185, 129, 0.3)';
                messageContainer.style.color = '#059669';
                messageContainer.innerHTML = '<strong>Thanks!</strong> We reply within 1 business day. If this is a fit, we\'ll send next steps for the $99 Automation Audit (credited toward your build).';
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
