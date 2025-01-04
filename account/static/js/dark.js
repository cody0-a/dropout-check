document.getElementsByClassName('theme')[0].addEventListener('click', function() {
    document.body.classList.toggle('dark');
    document.body.classList.toggle('light');
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});