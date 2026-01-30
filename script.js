/**
 * STROMATION - AI AUTOMATION AGENCY
 * Clean JavaScript for Professional Site
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initHeaderScroll();
    initScrollAnimations();
    initSmoothScroll();
    initActiveNavHighlight();
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
// CONTACT FORM HANDLING
// ==========================================
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);

        // For now, just show a success message
        // In production, you would send this to your backend
        alert('Thank you for your message! We will get back to you within one business day.');
        this.reset();

        // You can integrate with services like:
        // - Formspree
        // - Netlify Forms
        // - Your own backend API
    });
}
