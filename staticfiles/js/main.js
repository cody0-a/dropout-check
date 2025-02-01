document.addEventListener('DOMContentLoaded', () => {
    const windowHeight = window.innerHeight;
    const form = document.getElementById('student_form');
    const formFields = form.querySelectorAll('input, select');
    const submitButton = form.querySelector('savebtn')
    const numberOfFields = formFields.length;
    
    // Calculate the available height for the form fields
    const availableHeight = windowHeight - form.offsetTop - (submitButton.offsetHeight + 20); // Assuming some margin
    
    // Calculate the height for each form field
    const fieldHeight = availableHeight / numberOfFields;

    formFields.forEach((field) => {
        field.style.height = `${fieldHeight}px`;
    });

    form.addEventListener('submit', () => {
        console.log('form submitted');
    });
});

