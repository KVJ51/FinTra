/**
 * FinTra - Client-side Utilities and Financial Calculations Helper
 */

document.addEventListener("DOMContentLoaded", () => {
    // Initialize Bootstrap tooltips if any
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Format currency inputs smoothly
    const currencyInputs = document.querySelectorAll('.format-currency');
    currencyInputs.forEach(input => {
        input.addEventListener('blur', (e) => {
            const val = parseFloat(e.target.value);
            if (!isNaN(val)) {
                e.target.value = val.toFixed(2);
            }
        });
    });
});
