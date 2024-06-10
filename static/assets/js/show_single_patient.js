const cardsClickable = document.querySelectorAll(".card-clickable");

cardsClickable.forEach((card) => {
    card.addEventListener("click", () => {
        const patientId = card.getAttribute('data-patient-id');
        const url = `/patient/${patientId}`;
        window.location.href = url;
    });
});