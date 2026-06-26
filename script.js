/* Kipply landing — progressive enhancement only.
   The page is fully usable with JS disabled; this adds the mobile menu,
   scroll reveals, and the play-on-view swipe demo. */
(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ----- Header gets depth once you scroll (no static hairline) --- */
    var header = document.querySelector('.site-header');
    if (header) {
        var onScroll = function () {
            header.classList.toggle('scrolled', window.scrollY > 8);
        };
        onScroll();
        window.addEventListener('scroll', onScroll, { passive: true });
    }

    /* ----- Mobile nav ----------------------------------------------- */
    var toggle = document.querySelector('.nav-toggle');
    var menu = document.getElementById('navmenu');

    function closeMenu() {
        if (!toggle || !menu) return;
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open menu');
        menu.classList.remove('open');
    }

    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            var open = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', String(!open));
            toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
            menu.classList.toggle('open', !open);
        });

        // Close after tapping a link, or on Escape.
        menu.addEventListener('click', function (e) {
            if (e.target.closest('a')) closeMenu();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeMenu();
        });
        // Reset when resizing back up to desktop.
        window.matchMedia('(min-width: 721px)').addEventListener('change', closeMenu);
    }

    /* ----- Scroll reveal -------------------------------------------- */
    var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

    if (reduceMotion || !('IntersectionObserver' in window)) {
        reveals.forEach(function (el) { el.classList.add('is-in'); });
    } else {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-in');
                    io.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px 0px 0px', threshold: 0.12 });
        reveals.forEach(function (el) { io.observe(el); });

        // Failsafe: never let content stay hidden (e.g. a tall viewport that
        // fits the whole page without scrolling). Reveal anything still in
        // view shortly after load.
        window.addEventListener('load', function () {
            setTimeout(function () {
                reveals.forEach(function (el) {
                    var r = el.getBoundingClientRect();
                    if (r.top < window.innerHeight && r.bottom > 0) {
                        el.classList.add('is-in');
                    }
                });
            }, 600);
        });
    }
})();
