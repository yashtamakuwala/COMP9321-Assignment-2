const API_URL = 'http://127.0.0.1:5000/api/v1/'

function getQuote() {
    const zipcode = document.getElementById('zipCode').value;
    const property = document.getElementById('propertyType').value;
    const roomType = document.getElementById('roomType').value;
    const guestCount = document.getElementById('guestCount').value;
    const bedCount = document.getElementById('bedCount').value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        console.log(this.responseText);
        alert(this.responseText)
    };
    xhttp.open("GET", API_URL, true);
    xhttp.send();
}

function signup() {
    let user = {};
    const URL = API_URL + 'users';
    user.email = document.getElementById('email').value;
    user.password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;
    user.first_name = document.getElementById('firstName').value;
    user.last_name = document.getElementById('lastName').value;
    let jsonString = JSON.stringify(user);

    if (user.password === confirmPassword) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && (this.status === 201 || this.status === 400)) {
                const div = document.createElement('div');
                div.setAttribute('id', 'response');
                let res = document.getElementById('response');
                if (res) {
                    res.parentNode.removeChild(res);
                }
                let response = JSON.parse(this.responseText);
                div.innerHTML = response.message;
                document.getElementById('information').appendChild(div);
            }
        };
        xhttp.open("POST", URL, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        console.log(jsonString);
        xhttp.send(jsonString);
    } else {
        alert('Passwords do not match, Try again');
    }


}