/**
 * STROMATION - AI AUTOMATION AGENCY
 * Interactive Animations & Effects
 */

// ==========================================
// PARTICLE BACKGROUND ANIMATION
// ==========================================
class ParticleBackground {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 80;
        this.mouse = { x: 0, y: 0 };

        this.init();
        this.animate();
        this.setupEventListeners();
    }

    init() {
        this.resize();

        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.resize());
        document.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw particles
        this.particles.forEach((particle, i) => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;

            // Wrap around edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;

            // Mouse interaction
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 150) {
                const force = (150 - dist) / 150;
                particle.x -= dx * force * 0.03;
                particle.y -= dy * force * 0.03;
            }

            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(0, 210, 198, ${particle.opacity})`;
            this.ctx.fill();

            // Draw connections
            this.particles.slice(i + 1).forEach(otherParticle => {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 150) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(otherParticle.x, otherParticle.y);
                    this.ctx.strokeStyle = `rgba(0, 210, 198, ${0.2 * (1 - distance / 150)})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            });
        });

        requestAnimationFrame(() => this.animate());
    }
}

// ==========================================
// NEURAL NETWORK CANVAS ANIMATION
// ==========================================
class NeuralNetwork {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.nodes = [];
        this.nodeCount = 30;

        this.init();
        this.animate();
    }

    init() {
        this.resize();

        for (let i = 0; i < this.nodeCount; i++) {
            this.nodes.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                radius: Math.random() * 3 + 2,
                pulsePhase: Math.random() * Math.PI * 2
            });
        }

        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const time = Date.now() * 0.001;

        this.nodes.forEach((node, i) => {
            // Update position
            node.x += node.vx;
            node.y += node.vy;

            // Bounce off edges
            if (node.x < 0 || node.x > this.canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > this.canvas.height) node.vy *= -1;

            // Pulsing effect
            const pulseSize = node.radius + Math.sin(time * 2 + node.pulsePhase) * 1.5;

            // Draw node glow
            const gradient = this.ctx.createRadialGradient(
                node.x, node.y, 0,
                node.x, node.y, pulseSize * 3
            );
            gradient.addColorStop(0, 'rgba(74, 242, 232, 0.4)');
            gradient.addColorStop(0.5, 'rgba(0, 210, 198, 0.2)');
            gradient.addColorStop(1, 'rgba(0, 210, 198, 0)');

            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, pulseSize * 3, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();

            // Draw node core
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, pulseSize, 0, Math.PI * 2);
            this.ctx.fillStyle = '#00D2C6';
            this.ctx.fill();

            // Draw connections
            this.nodes.slice(i + 1).forEach(otherNode => {
                const dx = node.x - otherNode.x;
                const dy = node.y - otherNode.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 200) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(node.x, node.y);
                    this.ctx.lineTo(otherNode.x, otherNode.y);

                    const opacity = (1 - distance / 200) * 0.3;
                    this.ctx.strokeStyle = `rgba(0, 210, 198, ${opacity})`;
                    this.ctx.lineWidth = 2;
                    this.ctx.stroke();

                    // Animated data flow
                    const flowProgress = (time * 0.5 + i * 0.1) % 1;
                    const flowX = node.x + (otherNode.x - node.x) * flowProgress;
                    const flowY = node.y + (otherNode.y - node.y) * flowProgress;

                    this.ctx.beginPath();
                    this.ctx.arc(flowX, flowY, 3, 0, Math.PI * 2);
                    this.ctx.fillStyle = '#4AF2E8';
                    this.ctx.shadowBlur = 10;
                    this.ctx.shadowColor = '#4AF2E8';
                    this.ctx.fill();
                    this.ctx.shadowBlur = 0;
                }
            });
        });

        requestAnimationFrame(() => this.animate());
    }
}

// ==========================================
// SCROLL ANIMATIONS
// ==========================================
class ScrollAnimations {
    constructor() {
        this.elements = document.querySelectorAll('.showcase-card, .feature-card, .stat-card, .pricing-card');
        this.init();
    }

    init() {
        this.observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry, index) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            entry.target.classList.add('fade-in', 'visible');
                        }, index * 100);
                    }
                });
            },
            { threshold: 0.1 }
        );

        this.elements.forEach(el => {
            el.classList.add('fade-in');
            this.observer.observe(el);
        });
    }
}

// ==========================================
// CURSOR PARTICLE EFFECTS
// ==========================================
class CursorParticles {
    constructor() {
        this.particles = [];
        this.init();
    }

    init() {
        document.addEventListener('mousemove', (e) => {
            if (Math.random() > 0.9) {
                this.createParticle(e.clientX, e.clientY);
            }
        });

        this.animate();
    }

    createParticle(x, y) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.background = '#00D2C6';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';
        particle.style.boxShadow = '0 0 10px #00D2C6';
        particle.style.opacity = '1';

        document.body.appendChild(particle);

        this.particles.push({
            element: particle,
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2 - 1,
            life: 1
        });
    }

    animate() {
        this.particles.forEach((particle, index) => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.vy += 0.1; // gravity
            particle.life -= 0.02;

            particle.element.style.left = particle.x + 'px';
            particle.element.style.top = particle.y + 'px';
            particle.element.style.opacity = particle.life;

            if (particle.life <= 0) {
                particle.element.remove();
                this.particles.splice(index, 1);
            }
        });

        requestAnimationFrame(() => this.animate());
    }
}

// ==========================================
// SMOOTH SCROLL
// ==========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
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
// HEADER SCROLL EFFECT
// ==========================================
function initHeaderScroll() {
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.background = 'rgba(11, 15, 25, 0.95)';
            header.style.boxShadow = '0 5px 30px rgba(0, 210, 198, 0.1)';
        } else {
            header.style.background = 'rgba(11, 15, 25, 0.8)';
            header.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });
}

// ==========================================
// BUTTON CLICK EFFECTS
// ==========================================
function initButtonEffects() {
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
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// ==========================================
// SHOWCASE CARD ANIMATIONS
// ==========================================
function initShowcaseAnimations() {
    const cards = document.querySelectorAll('.showcase-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // Enhance animation on hover
            const animation = card.getAttribute('data-animation');

            if (animation === 'chat') {
                const messages = card.querySelectorAll('.chat-message');
                messages.forEach((msg, i) => {
                    msg.style.animation = 'none';
                    setTimeout(() => {
                        msg.style.animation = `messageSlide 0.5s ease-out ${i * 0.3}s backwards`;
                    }, 10);
                });
            } else if (animation === 'workflow') {
                const blocks = card.querySelectorAll('.workflow-block');
                blocks.forEach((block, i) => {
                    block.style.animation = 'none';
                    setTimeout(() => {
                        block.style.animation = `blockSlide 1s ease-out ${i * 0.3}s backwards infinite`;
                    }, 10);
                });
            }
        });
    });
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

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
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
    const isPercentage = text.includes('%');
    const isMultiplier = text.includes('x');
    const hasUnit = text.includes('hrs/week');

    let value;
    if (hasUnit) {
        value = parseInt(text);
    } else if (isPercentage) {
        value = parseInt(text);
    } else if (isMultiplier) {
        value = parseFloat(text);
    }

    const duration = 2000;
    const steps = 60;
    const stepValue = value / steps;
    const stepDuration = duration / steps;

    let current = 0;
    const timer = setInterval(() => {
        current += stepValue;
        if (current >= value) {
            current = value;
            clearInterval(timer);
        }

        if (hasUnit) {
            element.textContent = Math.round(current) + ' hrs/week';
        } else if (isPercentage) {
            element.textContent = Math.round(current) + '%';
        } else if (isMultiplier) {
            element.textContent = current.toFixed(1) + 'x';
        }
    }, stepDuration);
}

// ==========================================
// WORKFLOW NODE HOVER EFFECT
// ==========================================
function initWorkflowHover() {
    const nodes = document.querySelectorAll('.workflow-node');

    nodes.forEach(node => {
        node.addEventListener('mouseenter', () => {
            nodes.forEach(n => n.style.opacity = '0.3');
            node.style.opacity = '1';
            node.style.transform = 'scale(1.2) translateY(-10px)';
        });

        node.addEventListener('mouseleave', () => {
            nodes.forEach(n => {
                n.style.opacity = '1';
                n.style.transform = '';
            });
        });
    });
}

// ==========================================
// LOGO CLICK TO TOP
// ==========================================
function initLogoClick() {
    const logo = document.querySelector('.logo');

    if (logo) {
        logo.style.cursor = 'pointer';
        logo.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// ==========================================
// INITIALIZE ALL
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize canvas animations
    new ParticleBackground('particleCanvas');
    new NeuralNetwork('networkCanvas');

    // Initialize scroll and interaction effects
    new ScrollAnimations();
    new CursorParticles();

    // Initialize utility functions
    initSmoothScroll();
    initHeaderScroll();
    initButtonEffects();
    initShowcaseAnimations();
    initPricingTilt();
    initStatsCounter();
    initWorkflowHover();
    initLogoClick();

    console.log('🚀 Stromation website loaded successfully!');
});

// ==========================================
// PERFORMANCE OPTIMIZATION
// ==========================================
// Reduce animations on low-performance devices
if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
    document.documentElement.style.setProperty('--transition-smooth', 'none');
    console.log('⚡ Reduced animations for performance');
}

// ==========================================
// DEMO SECTION ANIMATIONS
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
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
});
