// Static JavaScript for the scroll-down button
document.addEventListener("DOMContentLoaded", function () {
    // Check if the page has a vertical scrollbar
    function hasVerticalScrollbar() {
        return document.body.scrollHeight > window.innerHeight;
    }

    // Show or hide the scroll-down button based on the presence of vertical scrollbar
    function toggleScrollButton() {
        const scrollButton = document.getElementById('scroll-down-button');
        if (hasVerticalScrollbar()) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }

    // Scroll to the bottom of the page when the button is clicked
    function scrollToBottom() {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }

    // Attach event listeners
    const scrollButton = document.getElementById('scroll-down-button');
    if (scrollButton) {
        scrollButton.addEventListener('click', scrollToBottom);
        window.addEventListener('scroll', toggleScrollButton);
    }

    // Initial check on page load
    toggleScrollButton();
});
