// Assign API endpoint url
var API_ENDPOINT = 'https://4z7j9imbab.execute-api.us-east-1.amazonaws.com/prod/reminderapp';


// Create divs for status report messages
var errorMsg = document.getElementById('error-message')
var successMsg = document.getElementById('success-message')
var resultsMsg = document.getElementById('results-message')

// Functions return button contents 
function waitSecondsValue() { return document.getElementById('waitSeconds').value }
function messageValue() { return document.getElementById('message').value }
function emailValue() { return document.getElementById('email').value }
function phoneValue() { return document.getElementById('phone').value }

// Clear existing notifications
function clearNotifications() {
	errorMsg.textContent = '';
	resultsMsg.textContent = '';
	successMsg.textContent = '';
}

// Add listeners for buttons to make API requests
document.getElementById('bothButton').addEventListener('click', function(e) {
	sendData(e, 'both');
});

document.getElementById('emailButton').addEventListener('click', function(e) {
	sendData(e, 'email');
});

document.getElementById('smsButton').addEventListener('click', function(e) {
	sendData(e, 'sms');
});

// Combines functions to send request
function sendData (e, pref) {
	e.preventDefault()
	clearNotifications()
	fetch(API_ENDPOINT, {
		headers:{
			"Content-type": "application/json"
		},
		method: 'POST',
		body: JSON.stringify({
			waitSeconds: waitSecondsValue(),
			preference: pref,
			message: messageValue(),
			email: emailValue(),
			phone: phoneValue()
		}),
		mode: 'cors'
	})
	.then((resp) => resp.json())
	.then(function(data) {
		console.log(data)
		successMsg.textContent = 'Request Submitted Successfully';
		resultsMsg.textContent = JSON.stringify(data);
	})
	.catch(function(err) {
		errorMsg.textContent = 'Error:\n' + err.toString();
		errorMsg.textContent = 'Service Disconnected - email jacob.farner1@gmail.com to reconnect.';
		console.log(err)
	});
};