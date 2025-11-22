/**
 * STROMATION - AI AUTOMATION AGENCY
 * Premium JavaScript Animations
 */

// ==========================================
// MAINTAIN SCROLL POSITION ON REFRESH
// ==========================================
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}

// Save scroll position continuously
let scrollSaveTimer;
window.addEventListener('scroll', () => {
    clearTimeout(scrollSaveTimer);
    scrollSaveTimer = setTimeout(() => {
        sessionStorage.setItem('scrollPosition', window.pageYOffset.toString());
    }, 50);
});

// Save before unload as backup
window.addEventListener('beforeunload', () => {
    sessionStorage.setItem('scrollPosition', window.pageYOffset.toString());
});

// ==========================================
// GRADIENT CANVAS BACKGROUND
// ==========================================
class GradientBackground {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.time = 0;

        this.init();
        this.animate();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
    }

    animate() {
        this.time += 0.005;

        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Create flowing gradient effect
        const gradient1 = this.ctx.createRadialGradient(
            this.canvas.width * (0.3 + Math.sin(this.time) * 0.2),
            this.canvas.height * (0.3 + Math.cos(this.time * 0.7) * 0.2),
            0,
            this.canvas.width * (0.3 + Math.sin(this.time) * 0.2),
            this.canvas.height * (0.3 + Math.cos(this.time * 0.7) * 0.2),
            this.canvas.width * 0.6
        );
        gradient1.addColorStop(0, 'rgba(0, 210, 198, 0.15)');
        gradient1.addColorStop(0.5, 'rgba(0, 210, 198, 0.08)');
        gradient1.addColorStop(1, 'rgba(11, 15, 25, 0)');

        const gradient2 = this.ctx.createRadialGradient(
            this.canvas.width * (0.7 + Math.cos(this.time * 1.3) * 0.2),
            this.canvas.height * (0.6 + Math.sin(this.time * 0.9) * 0.2),
            0,
            this.canvas.width * (0.7 + Math.cos(this.time * 1.3) * 0.2),
            this.canvas.height * (0.6 + Math.sin(this.time * 0.9) * 0.2),
            this.canvas.width * 0.5
        );
        gradient2.addColorStop(0, 'rgba(74, 242, 232, 0.12)');
        gradient2.addColorStop(0.5, 'rgba(74, 242, 232, 0.06)');
        gradient2.addColorStop(1, 'rgba(11, 15, 25, 0)');

        const gradient3 = this.ctx.createRadialGradient(
            this.canvas.width * (0.5 + Math.sin(this.time * 1.1) * 0.15),
            this.canvas.height * (0.8 + Math.cos(this.time * 0.8) * 0.15),
            0,
            this.canvas.width * (0.5 + Math.sin(this.time * 1.1) * 0.15),
            this.canvas.height * (0.8 + Math.cos(this.time * 0.8) * 0.15),
            this.canvas.width * 0.4
        );
        gradient3.addColorStop(0, 'rgba(0, 210, 198, 0.1)');
        gradient3.addColorStop(0.5, 'rgba(0, 210, 198, 0.05)');
        gradient3.addColorStop(1, 'rgba(11, 15, 25, 0)');

        // Draw gradients
        this.ctx.fillStyle = gradient1;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = gradient2;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = gradient3;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        requestAnimationFrame(() => this.animate());
    }
}

// ==========================================
// SCROLL ANIMATIONS
// ==========================================
class ScrollAnimations {
    constructor() {
        this.initFadeIns();
        this.initDemoSteps();
    }

    initFadeIns() {
        const elements = document.querySelectorAll('.service-card, .service-card-large, .service-card-core, .demo-video-card, .demo-video-item, .demo-card, .pricing-card, .benefit-card, .testimonial-card, .stat-card, .faq-item, .whyus-card');

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in', 'visible');
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.15,
                rootMargin: '0px 0px -50px 0px'
            }
        );

        elements.forEach(el => {
            el.classList.add('fade-in');
            observer.observe(el);
        });
    }

    initDemoSteps() {
        const observerOptions = {
            threshold: 0.2,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const steps = entry.target.querySelectorAll('.demo-step');
                    steps.forEach((step, index) => {
                        setTimeout(() => {
                            step.classList.add('animate-in');
                        }, index * 150);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.demo-steps').forEach(section => {
            observer.observe(section);
        });
    }
}

// ==========================================
// HEADER SCROLL EFFECT
// ==========================================
function initHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;

        if (scrolled > 100) {
            header.style.background = 'rgba(11, 15, 25, 0.95)';
            header.style.boxShadow = '0 5px 30px rgba(0, 210, 198, 0.1)';
        } else {
            header.style.background = 'rgba(11, 15, 25, 0.85)';
            header.style.boxShadow = 'none';
        }
    });
}

// ==========================================
// SMOOTH SCROLL
// ==========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ==========================================
// BUTTON RIPPLE EFFECT
// ==========================================
function initButtonEffects() {
    // Add ripple animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        .btn {
            position: relative;
            overflow: hidden;
        }
    `;
    document.head.appendChild(style);

    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// ==========================================
// STATS COUNTER ANIMATION
// ==========================================
function initStatsCounter() {
    const statValues = document.querySelectorAll('.stat-value');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                entry.target.classList.add('counted');
                animateValue(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statValues.forEach(stat => observer.observe(stat));
}

function animateValue(element) {
    const text = element.textContent;
    const hasPercent = text.includes('%');
    const hasPlus = text.includes('+');
    const hasHours = text.includes('hrs');

    let targetValue = parseFloat(text.replace(/[^0-9.]/g, ''));

    const duration = 2000;
    const steps = 60;
    const stepValue = targetValue / steps;
    const stepDuration = duration / steps;

    let current = 0;
    const timer = setInterval(() => {
        current += stepValue;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(timer);
        }

        let displayValue = Math.round(current);

        if (hasHours) {
            element.textContent = displayValue + '+ hrs';
        } else if (hasPlus) {
            element.textContent = displayValue + '+';
        } else if (hasPercent) {
            element.textContent = displayValue + '%';
        } else {
            element.textContent = displayValue;
        }
    }, stepDuration);
}

// ==========================================
// PRICING CARD TILT EFFECT
// ==========================================
function initPricingTilt() {
    const cards = document.querySelectorAll('.pricing-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 25;
            const rotateY = (centerX - x) / 25;

            const isFeatured = card.classList.contains('featured');
            const baseTransform = isFeatured ? 'scale(1.05)' : '';

            card.style.transform = `${baseTransform} perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });

        card.addEventListener('mouseleave', () => {
            const isFeatured = card.classList.contains('featured');
            card.style.transform = isFeatured ? 'scale(1.05)' : '';
        });
    });
}

// ==========================================
// LOGO CLICK TO TOP
// ==========================================
function initLogoClick() {
    const logo = document.querySelector('.logo');
    const logoImg = document.querySelector('.logo-img');

    if (logo) {
        logo.style.cursor = 'pointer';
        logo.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    if (logoImg) {
        logoImg.style.cursor = 'pointer';
    }
}

// ==========================================
// CARD HOVER EFFECTS
// ==========================================
function initCardEffects() {
    const cards = document.querySelectorAll('.service-card, .benefit-card, .testimonial-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
}

// ==========================================
// INITIALIZE ALL
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize gradient background
    new GradientBackground('gradientCanvas');

    // Initialize scroll animations
    new ScrollAnimations();

    // Initialize utility functions
    initHeaderScroll();
    initSmoothScroll();
    initButtonEffects();
    initStatsCounter();
    initPricingTilt();
    initLogoClick();
    initCardEffects();

    console.log('%c🚀 Stromation Website Loaded', 'color: #00D2C6; font-size: 16px; font-weight: bold;');
    console.log('%cPremium AI Automation Agency', 'color: #4AF2E8; font-size: 12px;');
});

// ==========================================
// PERFORMANCE OPTIMIZATION
// ==========================================
// Reduce animations on low-performance devices
if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
    document.documentElement.style.setProperty('--transition', 'none');
    console.log('⚡ Reduced animations for performance');
}

// Pause animations when tab is not visible
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('⏸️ Animations paused (tab hidden)');
    } else {
        console.log('▶️ Animations resumed');
    }
});

// ==========================================
// DEMO MODAL FULLSCREEN FUNCTIONALITY
// ==========================================
function initDemoModal() {
    const modal = document.getElementById('demoModal');
    const modalFrame = document.getElementById('modalFrame');
    const closeBtn = document.querySelector('.demo-modal-close');
    const demoCards = document.querySelectorAll('.demo-card');

    if (!modal || !modalFrame || !closeBtn) return;

    // Click handler for all demo cards
    demoCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Find the iframe within this card
            const iframe = this.querySelector('.demo-frame');
            if (!iframe) return;

            const src = iframe.getAttribute('src');
            if (!src) return;

            // Set the modal iframe src
            modalFrame.setAttribute('src', src);

            // Show modal
            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        });

        // Add cursor pointer to show it's clickable
        card.style.cursor = 'pointer';
    });

    // Close modal on X button click
    closeBtn.addEventListener('click', closeModal);

    // Close modal on outside click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    function closeModal() {
        modal.classList.remove('active');
        modalFrame.setAttribute('src', ''); // Clear iframe src to stop animations
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Add to DOMContentLoaded initialization
document.addEventListener('DOMContentLoaded', () => {
    // Initialize demo modal
    initDemoModal();
});
