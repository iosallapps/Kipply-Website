/* Kipply, kipplyapp.com. Progressive enhancement only: the mobile menu.
   Without JS the links simply show under the bar (see styles.css, .js .nav-links). */
(function () {
    'use strict';

    var toggle = document.querySelector('.nav-toggle');
    var menu = document.getElementById('navmenu');
    if (!toggle || !menu) return;

    function setOpen(open) {
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
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
