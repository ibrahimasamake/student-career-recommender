/**
 * CareerPath AI - Client-side JavaScript
 * Handles form validation, range slider updates, and UI interactions.
 */

document.addEventListener("DOMContentLoaded", function () {
    // --- Range Slider Updates ---
    initSliders();

    // --- Form Validation ---
    initFormValidation();
});

/**
 * Initialize all range slider inputs to show their current value.
 */
function initSliders() {
    // Score sliders (0-100)
    const scoreFields = [
        "math_score",
        "programming_score",
        "communication_score",
        "problem_solving_score",
    ];

    scoreFields.forEach(function (fieldId) {
        const input = document.getElementById(fieldId);
        const display = document.getElementById(fieldId + "_val");
        if (input && display) {
            input.addEventListener("input", function () {
                display.textContent = this.value;
            });
        }
    });

    // Interest sliders (1-10)
    const interestFields = [
        "web_interest",
        "mobile_interest",
        "ai_interest",
        "database_interest",
        "networking_interest",
        "cloud_interest",
        "design_interest",
    ];

    interestFields.forEach(function (fieldId) {
        const input = document.getElementById(fieldId);
        const display = document.getElementById(fieldId + "_val");
        if (input && display) {
            input.addEventListener("input", function () {
                display.textContent = this.value;
            });
        }
    });
}

/**
 * Initialize Bootstrap form validation.
 */
function initFormValidation() {
    const form = document.getElementById("careerForm");
    if (!form) return;

    form.addEventListener(
        "submit",
        function (event) {
            // Basic client-side validation
            const name = form.querySelector("#name");
            const age = form.querySelector("#age");

            let valid = true;

            if (!name.value.trim()) {
                name.classList.add("is-invalid");
                valid = false;
            } else {
                name.classList.remove("is-invalid");
            }

            const ageVal = parseInt(age.value, 10);
            if (isNaN(ageVal) || ageVal < 15 || ageVal > 30) {
                age.classList.add("is-invalid");
                valid = false;
            } else {
                age.classList.remove("is-invalid");
            }

            if (!valid) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }

            // Show loading state on submit button
            const submitBtn = document.getElementById("submitBtn");
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Analyzing...';
            }

            // Let the form submit normally (server-side handling)
            form.classList.add("was-validated");
        },
        false
    );
}

/**
 * Update the displayed score value for a range input.
 * Called from inline oninput handlers in HTML.
 *
 * @param {HTMLInputElement} input - The range input element.
 */
function updateScore(input) {
    var display = document.getElementById(input.id + "_val");
    if (display) {
        display.textContent = input.value;
    }
}

/**
 * Update the displayed interest value for a range input.
 * Called from inline oninput handlers in HTML.
 *
 * @param {HTMLInputElement} input - The range input element.
 */
function updateInterest(input) {
    var display = document.getElementById(input.id + "_val");
    if (display) {
        display.textContent = input.value;
    }
}
