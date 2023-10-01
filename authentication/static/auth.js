const form = document.querySelector('#regiser-form');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const capchaResponse = grecapcha.getResponse();

    if (!capchaResponse.length > 0) {
        throw new Error("Capcha is not completed");
    }
})