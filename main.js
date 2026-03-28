// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const mobileNav = document.querySelector('.nav-mobile');
const header = document.getElementById('site-header');

toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', !isOpen);
    mobileNav.classList.toggle('is-open');
});

// Close mobile nav on link click
mobileNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        toggle.setAttribute('aria-expanded', 'false');
        mobileNav.classList.remove('is-open');
    });
});

// Sticky header
window.addEventListener('scroll', () => {
    header.classList.toggle('is-scrolled', window.scrollY > 50);
}, { passive: true });

// Scroll reveal
const reveals = document.querySelectorAll(
    '.service-item, .why-item, .story-left, .story-right, .hero-stat-card, ' +
    '.approach-card, .founder-highlight, .service-detail-left, .service-detail-right'
);

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

reveals.forEach(el => revealObserver.observe(el));
