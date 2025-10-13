// Scramble animation for the hero heading.
const textElement = document.getElementById("animate-text");
if (textElement) {
    // Prefer a data-value attribute, otherwise fall back to the current text content
    const originalText = textElement.dataset.value || textElement.innerText || "";

    // Characters for the scramble effect (A-Z, 0-9, and symbols)
    const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+=_";

    let interval = null;

    // Use mouseenter so moving across children doesn't retrigger unexpectedly
    textElement.addEventListener('mouseenter', () => {
        let iteration = 0;
        clearInterval(interval);

        interval = setInterval(() => {
            const scrambledText = originalText
                .split("")
                .map((char, index) => {
                    if (index < iteration) return originalText[index];
                    return ALPHABET[Math.floor(Math.random() * ALPHABET.length)];
                })
                .join("");

            textElement.innerText = scrambledText;

            if (iteration >= originalText.length) {
                clearInterval(interval);
            }

            iteration += 1;
        }, 33);
    });

    // Optional: restore original text when mouse leaves
    textElement.addEventListener('mouseleave', () => {
        clearInterval(interval);
        textElement.innerText = originalText;
    });
}