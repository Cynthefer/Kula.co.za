const SkeletonManager = {
    templates: {
        text: (w = '100%', h = '1rem') => `<div class="skeleton" style="width:${w};height:${h}"></div>`,
        card: () => `
            <div class="rounded-2xl border border-kula-light p-6 space-y-4">
                <div class="skeleton" style="width:48px;height:48px;border-radius:12px"></div>
                <div class="skeleton" style="width:70%;height:1.25rem"></div>
                <div class="skeleton" style="width:100%;height:0.875rem"></div>
                <div class="skeleton" style="width:85%;height:0.875rem"></div>
            </div>`,
        row: () => `
            <div class="flex items-center gap-4 py-3">
                <div class="skeleton" style="width:40px;height:40px;border-radius:50%"></div>
                <div class="flex-1 space-y-2">
                    <div class="skeleton" style="width:60%;height:0.875rem"></div>
                    <div class="skeleton" style="width:40%;height:0.75rem"></div>
                </div>
            </div>`,
        image: (h = '16rem') => `<div class="skeleton" style="width:100%;height:${h}"></div>`,
    },

    render(target, count = 3, type = 'card') {
        const el = typeof target === 'string' ? document.querySelector(target) : target;
        if (!el) return;
        el.dataset.skeletonActive = 'true';
        const builder = this.templates[type] || this.templates.card;
        let html = '';
        if (type === 'text' || type === 'image') {
            html = builder();
        } else {
            for (let i = 0; i < count; i++) html += builder();
        }
        el.innerHTML = html;
    },

    clear(target) {
        const el = typeof target === 'string' ? document.querySelector(target) : target;
        if (!el) return;
        delete el.dataset.skeletonActive;
    },

    async load(target, url, options = {}, type = 'card', count = 3) {
        const el = typeof target === 'string' ? document.querySelector(target) : target;
        if (!el) return null;
        this.render(el, count, type);
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    ...(options.headers || {}),
                },
                ...options,
            });
            if (!response.ok) throw new Error('Request failed');
            const data = await response.json();
            this.clear(el);
            return data;
        } catch (error) {
            this.clear(el);
            el.innerHTML = `
                <div class="text-center py-12 text-kula-grey">
                    <i data-lucide="alert-circle" class="w-10 h-10 mx-auto mb-3 text-kula-grey"></i>
                    <p class="text-sm">Unable to load content.</p>
                    <button onclick="SkeletonManager.load('${target}', '${url}', {}, '${type}', ${count})"
                        class="mt-3 text-kula-blue text-sm font-semibold hover:underline">Retry</button>
                </div>`;
            lucide.createIcons();
            return null;
        }
    },
};

window.SkeletonManager = SkeletonManager;