document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const openers = document.querySelectorAll('[data-sidebar-open]');
    const closers = document.querySelectorAll('[data-sidebar-close]');

    openers.forEach(function (button) {
        button.addEventListener('click', function () { body.classList.add('sidebar-open'); });
    });
    closers.forEach(function (button) {
        button.addEventListener('click', function () { body.classList.remove('sidebar-open'); });
    });

    document.querySelectorAll('.topbar-search input').forEach(function (input) {
        input.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') { input.value = ''; input.blur(); }
        });
    });
});
