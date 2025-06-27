document.addEventListener('DOMContentLoaded', function() {
    tippy('[data-tippy-content]', {
        arrow: true,
        animation: 'fade'
    });
    
    document.querySelectorAll('.dropdown-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            this.nextElementSibling.classList.toggle('hidden');
        });
    });
});