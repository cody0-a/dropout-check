document.getElementById('login').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Regex for email validation
    var usernameRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;

    if (!usernameRegex.test(username) || password.test(passwordRegex)) {
        alert('Please fill all the fields correctly');
    } 
    else {
        var data = {
            email: email,
            password: password
        };
        fetch('127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then((response) => {
            if (response.status == 200) {
                window.location.href = '/home';
            } else {
                alert('Invalid credentials');
            }
        });
    }
});

document.getElementById('register').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    var email = document.getElementById('email').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var password2 = document.getElementById('password2').value; // Fixed variable name
    var f_name = document.getElementById('f_name').value;
    var l_name = document.getElementById('l_name').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;
    var b_date = document.getElementById('b_date').value;

    // Regex for email validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Regex for password strength: at least 8 characters, 1 uppercase, 1 lowercase, 1 number
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;

    if (!emailRegex.test(email) || username.length == 0 || !passwordRegex.test(password) || password !== password2) {
        alert('Please fill all the fields correctly');
    } 
    else {
        var data = {
            email: email,
            username: username,
            password: password,
            f_name: f_name,
            l_name: l_name,
            phone: phone,
            address: address,
            b_date: b_date
        };
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then((response) => {
            if (response.status == 200) {
                window.location.href = '/home';
            } else {
                alert('Email already exists');
            }
        });
    }
});

document.getElementById('logout').addEventListener('click', function(event) {
    fetch('/logout', {
        method: 'POST'
    })
    .then((response) => {
        if (response.status == 200) {
            window.location.href = '/';
        }
    });

});

