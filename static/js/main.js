document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initSwipers();
    initHTMXHooks();
    initContactForm();
    initReorder();
    initScrollAnimations();
});

function initSwipers() {
    document.querySelectorAll('.kula-swiper').forEach((el) => {
        new Swiper(el, {
            slidesPerView: 1,
            spaceBetween: 24,
            loop: el.dataset.loop === 'true',
            autoplay: el.dataset.autoplay === 'true' ? { delay: 5000 } : false,
            pagination: { el: el.querySelector('.swiper-pagination'), clickable: true },
            navigation: {
                nextEl: el.querySelector('.swiper-button-next'),
                prevEl: el.querySelector('.swiper-button-prev'),
            },
            breakpoints: {
                640: { slidesPerView: parseInt(el.dataset.sm || 1, 10) },
                768: { slidesPerView: parseInt(el.dataset.md || 2, 10) },
                1024: { slidesPerView: parseInt(el.dataset.lg || 3, 10) },
            },
        });
    });
}

function initHTMXHooks() {
    document.body.addEventListener('htmx:beforeRequest', (e) => {
        const target = e.detail.target;
        if (target && target.dataset.skeleton) {
            SkeletonManager.render(target, 3, target.dataset.skeletonType || 'card');
        }
    });
    document.body.addEventListener('htmx:afterSwap', () => {
        lucide.createIcons();
        AOS.refresh();
    });
    document.body.addEventListener('htmx:responseError', () => {
        notyf.error('Something went wrong');
    });
}

function initContactForm() {
    const form = document.querySelector('#contact-form');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = form.querySelector('button[type=submit]');
        const original = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>';
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: new FormData(form),
            });
            const data = await response.json();
            if (response.ok) {
                form.reset();
                notyf.success('Message sent. We will be in touch.');
            } else {
                const errors = data.errors || {};
                Object.entries(errors).forEach(([field, msgs]) => {
                    notyf.error(`${field}: ${msgs.join(', ')}`);
                });
            }
        } catch (err) {
            notyf.error('Network error. Try again.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = original;
        }
    });
}

function initReorder() {
    document.querySelectorAll('[data-sortable]').forEach((container) => {
        Sortable.create(container, {
            animation: 150,
            handle: '[data-drag-handle]',
            onEnd: async () => {
                const model = container.dataset.sortable;
                const order = Array.from(container.children).map((child) => parseInt(child.dataset.id, 10));
                try {
                    await fetch(`${window.kulaConfig.apiBase}reorder/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': window.kulaConfig.csrfToken,
                        },
                        body: JSON.stringify({ model, order }),
                    });
                    notyf.success('Order saved');
                } catch (err) {
                    notyf.error('Reorder failed');
                }
            },
        });
    });
}

function initScrollAnimations() {
    AOS.init({ duration: 700, once: true, offset: 60 });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => notyf.success('Copied'));
}

window.copyToClipboard = copyToClipboard;