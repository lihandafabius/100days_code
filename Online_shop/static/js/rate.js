// script.js

document.querySelectorAll('.rating-stars').forEach(function(ratingContainer) {
    const stars = ratingContainer.querySelectorAll('.star');

    stars.forEach(function(star) {
        star.addEventListener('click', function() {
            const ratingValue = this.getAttribute('data-value');

            // Update the stars visually within this specific product
            stars.forEach(function(s, index) {
                if (index < ratingValue) {
                    s.innerHTML = '&#9733;';  // Filled star
                    s.classList.add('selected');
                } else {
                    s.innerHTML = '&#9734;';  // Empty star
                    s.classList.remove('selected');
                }
            });
        });
    });
});
