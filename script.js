/* Kipply, kipplyapp.com. Progressive enhancement only: the mobile menu.
   Without JS the links simply show under the bar (see styles.css, .js .nav-links). */
(function () {
    'use strict';

    var header = document.querySelector('.site-header');
    if (header) {
        var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    var toggle = document.querySelector('.nav-toggle');
    var menu = document.getElementById('navmenu');
    if (!toggle || !menu) return;

    function setOpen(open) {
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', (open ? toggle.dataset.labelClose : toggle.dataset.labelOpen) || (open ? 'Close menu' : 'Open menu'));
        menu.classList.toggle('open', open);
    }

    toggle.addEventListener('click', function () {
        setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    menu.addEventListener('click', function (event) {
        if (event.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') setOpen(false);
    });

    window.matchMedia('(min-width: 860px)').addEventListener('change', function () {
        setOpen(false);
    });
})();

/* overscroll:start  status bar color + rubber-band stretch (same as vistoapps.com) */
(function () {
    var meta = document.querySelector('meta[name="theme-color"]');
    var root = document.documentElement;
    var top = meta ? meta.getAttribute("content") : "";
    var scrolled = meta ? meta.getAttribute("data-scrolled") || top : "";
    var last = top, pending = false, stretched = false;
    var apply = function () {
        pending = false;
        var y = window.scrollY;
        var theme = y > 8 ? scrolled : top;
        if (meta && theme !== last) { meta.setAttribute("content", theme); last = theme; }
        if (y < 0) { root.style.setProperty("--osy", String(-y)); stretched = true; }
        else if (stretched) { root.style.removeProperty("--osy"); stretched = false; }
    };
    window.addEventListener("scroll", function () {
        if (!pending) { pending = true; window.requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
})();
/* overscroll:end */
