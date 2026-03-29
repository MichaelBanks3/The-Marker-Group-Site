const toggle = document.querySelector('.nav-toggle');
const mobileNav = document.querySelector('.nav-mobile');
const header = document.getElementById('site-header');

if (toggle && mobileNav) {
    toggle.addEventListener('click', () => {
        const isOpen = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!isOpen));
        mobileNav.classList.toggle('is-open');
    });

    mobileNav.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            toggle.setAttribute('aria-expanded', 'false');
            mobileNav.classList.remove('is-open');
        });
    });
}

if (header) {
    window.addEventListener(
        'scroll',
        () => {
            header.classList.toggle('is-scrolled', window.scrollY > 50);
        },
        { passive: true }
    );
}

const revealElements = document.querySelectorAll('[data-reveal]');

if ('IntersectionObserver' in window && revealElements.length > 0) {
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    revealElements.forEach((element) => revealObserver.observe(element));
} else {
    revealElements.forEach((element) => element.classList.add('is-visible'));
}

const heroCards = document.querySelectorAll('[data-reveal="hero"]');
heroCards.forEach((card, index) => {
    window.setTimeout(() => {
        card.classList.add('is-visible');
    }, 400 + index * 120);
});

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
        const targetSelector = anchor.getAttribute('href');
        const target = targetSelector ? document.querySelector(targetSelector) : null;

        if (!target) {
            return;
        }

        event.preventDefault();

        const headerOffset = 72;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    });
});
