// Scramble animation for the hero heading.
const textElement = document.getElementById("animate-text");
if (textElement) {
    // Prefer a data-value attribute, otherwise fall back to the current text content
    const originalText = textElement.dataset.value || textElement.innerText || "";

    // Characters for the scramble effect (A-Z, 0-9, and symbols)
    const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    let interval = null;

    // Determine which characters are allowed to be randomized (letters & digits).
    const originalChars = Array.from(originalText);
    const isRandomizable = originalChars.map(ch => /[A-Za-z0-9]/.test(ch));

    // Helper: lock the element's width so wrapping/line breaks remain stable during animation
    function lockWidth() {
        // measure current rendered width
        const w = textElement.offsetWidth;
        textElement.style.display = 'inline-block';
        textElement.style.width = w + 'px';
    }

    function unlockWidth() {
        textElement.style.width = '';
        textElement.style.display = '';
    }

    // Use mouseenter so moving across children doesn't retrigger unexpectedly
    textElement.addEventListener('mouseenter', () => {
        // lock width to preserve line breaks
        lockWidth();

        let iteration = 0;
        clearInterval(interval);

        interval = setInterval(() => {
            const scrambled = originalChars
                .map((char, index) => {
                    // always keep punctuation/whitespace stable
                    if (!isRandomizable[index]) return char;

                    if (index < iteration) return char; // reveal original

                    // otherwise pick a random ALPHABET char
                    return ALPHABET[Math.floor(Math.random() * ALPHABET.length)];
                })
                .join('');

            textElement.innerText = scrambled;

            if (iteration >= originalChars.length) {
                clearInterval(interval);
            }

            iteration += 1;
        }, 33);
    });

    // restore original text and unlock width when mouse leaves
    textElement.addEventListener('mouseleave', () => {
        clearInterval(interval);
        textElement.innerText = originalText;
        // small timeout to avoid jump if mouse re-enters quickly
        setTimeout(unlockWidth, 50);
    });

    // recompute width on resize so future animations keep correct wrapping
    window.addEventListener('resize', () => {
        // if width is currently locked, recompute and re-lock
        if (textElement.style.width) {
            // temporarily unlock so offsetWidth reflects current wrapping
            unlockWidth();
            lockWidth();
        }
    });
}