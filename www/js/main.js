server_url = 'http://127.0.0.1:5000/register'

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
    xhttp.open("GET", server_url, true);
    xhttp.send();
}

function signup() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
            alert(this.responseText)

        if (this.status === 400) {
            alert(this.responseText)
        }
    };
    xhttp.open("POST", server_url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    let postMessage = `email=${email}&lname=Ford`
    xhttp.send(postMessage);
    xhttp.send();
}