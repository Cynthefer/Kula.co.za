const InlineEdit = {
    init() {
        if (!window.kulaConfig?.isStaff) return;
        document.addEventListener('click', (e) => {
            const el = e.target.closest('[data-editable]');
            if (!el) return;
            if (!document.body.classList.contains('edit-mode')) return;
            if (el.getAttribute('contenteditable') === 'true') return;
            this.activate(el);
        });
    },

    activate(el) {
        const original = el.innerHTML;
        el.setAttribute('contenteditable', 'true');
        el.setAttribute('data-original', original);
        el.focus();

        const range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);

        const onBlur = () => this.save(el, original);
        const onKey = (e) => {
            if (e.key === 'Escape') {
                el.innerHTML = original;
                el.blur();
            }
            if (e.key === 'Enter' && !e.shiftKey && el.dataset.multiline !== 'true') {
                e.preventDefault();
                el.blur();
            }
        };

        el.addEventListener('blur', onBlur, { once: true });
        el.addEventListener('keydown', onKey);
    },

    async save(el, original) {
        el.removeAttribute('contenteditable');
        const value = el.innerHTML.trim();
        if (value === original.trim()) return;

        const payload = {
            model: el.dataset.model,
            field: el.dataset.field,
            value: value,
        };
        if (el.dataset.objectId) payload.object_id = parseInt(el.dataset.objectId, 10);

        try {
            const response = await fetch(`${window.kulaConfig.apiBase}inline-edit/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.kulaConfig.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify(payload),
            });
            if (!response.ok) throw new Error('Save failed');
            notyf.success('Saved');
        } catch (error) {
            el.innerHTML = original;
            notyf.error('Could not save');
        }
    },

    initImageUpload() {
        if (!window.kulaConfig?.isStaff) return;
        document.addEventListener('click', (e) => {
            const wrapper = e.target.closest('[data-editable-image]');
            if (!wrapper) return;
            if (!document.body.classList.contains('edit-mode')) return;
            const input = wrapper.querySelector('input[type=file]');
            if (input) input.click();
        });

        document.addEventListener('change', async (e) => {
            const input = e.target;
            if (!input.matches('[data-editable-image] input[type=file]')) return;
            const file = input.files[0];
            if (!file) return;
            const wrapper = input.closest('[data-editable-image]');
            const form = new FormData();
            form.append('file', file);
            form.append('upload_preset', wrapper.dataset.uploadPreset || 'kula_unsigned');
            const cloudName = wrapper.dataset.cloudName;
            try {
                const res = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
                    method: 'POST',
                    body: form,
                });
                const data = await res.json();
                if (!data.secure_url) throw new Error('Upload failed');
                await this.saveImage(wrapper, data.secure_url);
                const img = wrapper.querySelector('img');
                if (img) img.src = data.secure_url;
                notyf.success('Image updated');
            } catch (err) {
                notyf.error('Image upload failed');
            }
        });
    },

    async saveImage(wrapper, url) {
        const payload = {
            model: wrapper.dataset.model,
            field: wrapper.dataset.field,
            value: url,
        };
        if (wrapper.dataset.objectId) payload.object_id = parseInt(wrapper.dataset.objectId, 10);
        await fetch(`${window.kulaConfig.apiBase}inline-edit/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.kulaConfig.csrfToken,
            },
            body: JSON.stringify(payload),
        });
    },
};

document.addEventListener('DOMContentLoaded', () => {
    InlineEdit.init();
    InlineEdit.initImageUpload();
});

window.InlineEdit = InlineEdit;