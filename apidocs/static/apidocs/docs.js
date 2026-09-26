// ============================================================
// ZELADORX · PORTAL DAS APIS
// ============================================================

(function () {
    'use strict';

    const storageKey = 'zeladorx.apidocs.open-groups';
    const baseUrl = window.location.origin;

    // ---------- endereço base nos exemplos ----------
    function applyBaseUrl() {
        document.querySelectorAll('[data-base-url]').forEach(function (el) {
            el.textContent = baseUrl;
        });
        document.querySelectorAll('.dx-code code, .dx-endpoint code').forEach(function (el) {
            el.textContent = el.textContent.split('{BASE_URL}').join(baseUrl);
        });
    }

    // ---------- realce simples (comentários e textos) ----------
    function highlight() {
        document.querySelectorAll('.dx-code code').forEach(function (el) {
            const lines = el.textContent.split('\n');
            el.textContent = '';
            lines.forEach(function (line, index) {
                const hash = line.indexOf('#');
                const quote = line.search(/["']/);
                if (hash !== -1 && (quote === -1 || hash < quote)) {
                    el.appendChild(document.createTextNode(line.slice(0, hash)));
                    const span = document.createElement('span');
                    span.className = 'dx-comment';
                    span.textContent = line.slice(hash);
                    el.appendChild(span);
                } else {
                    line.split(/("[^"]*"|'[^']*')/).forEach(function (part) {
                        if (/^["'].*["']$/.test(part)) {
                            const span = document.createElement('span');
                            span.className = 'dx-string';
                            span.textContent = part;
                            el.appendChild(span);
                        } else {
                            el.appendChild(document.createTextNode(part));
                        }
                    });
                }
                if (index < lines.length - 1) el.appendChild(document.createTextNode('\n'));
            });
        });
    }

    // ---------- botão copiar ----------
    function bindCopy() {
        document.querySelectorAll('.dx-code').forEach(function (pre) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'dx-copy';
            button.textContent = 'Copiar';
            button.addEventListener('click', function () {
                navigator.clipboard.writeText(pre.querySelector('code').textContent).then(function () {
                    button.textContent = 'Copiado';
                    setTimeout(function () { button.textContent = 'Copiar'; }, 1500);
                });
            });
            pre.appendChild(button);
        });
    }

    // ---------- grupos do menu (persistem entre páginas) ----------
    function readGroups() {
        try { return JSON.parse(localStorage.getItem(storageKey)) || []; } catch (e) { return []; }
    }

    function saveGroups() {
        const open = Array.from(document.querySelectorAll('.dx-group.is-open')).map(function (g) { return g.dataset.group; });
        localStorage.setItem(storageKey, JSON.stringify(open));
    }

    function bindGroups() {
        const saved = readGroups();
        document.querySelectorAll('.dx-group').forEach(function (group) {
            if (saved.indexOf(group.dataset.group) !== -1) group.classList.add('is-open');
            group.querySelector('.dx-group-toggle').addEventListener('click', function () {
                group.classList.toggle('is-open');
                saveGroups();
            });
        });
        saveGroups();
        const active = document.querySelector('.dx-sub-link.is-active');
        const sidebar = document.getElementById('dxSidebar');
        if (active && sidebar) sidebar.scrollTop = active.offsetTop - sidebar.clientHeight / 2;
    }

    // ---------- busca no menu ----------
    function bindSearch() {
        const input = document.getElementById('dxSearch');
        const sidebar = document.getElementById('dxSidebar');
        if (!input) return;
        input.addEventListener('input', function () {
            const term = input.value.trim().toLowerCase();
            sidebar.classList.toggle('is-searching', term.length > 0);
            document.querySelectorAll('.dx-sub-link[data-search]').forEach(function (link) {
                link.classList.toggle('is-hidden', term.length > 0 && link.dataset.search.indexOf(term) === -1);
            });
        });
    }

    // ---------- menu no celular ----------
    function bindMobileMenu() {
        const sidebar = document.getElementById('dxSidebar');
        const backdrop = document.getElementById('dxBackdrop');
        const button = document.getElementById('dxMenuBtn');
        function toggle(open) {
            sidebar.classList.toggle('is-open', open);
            backdrop.classList.toggle('is-open', open);
        }
        if (button) button.addEventListener('click', function () { toggle(true); });
        if (backdrop) backdrop.addEventListener('click', function () { toggle(false); });
    }

    document.addEventListener('DOMContentLoaded', function () {
        applyBaseUrl();
        highlight();
        bindCopy();
        bindGroups();
        bindSearch();
        bindMobileMenu();
    });
})();
