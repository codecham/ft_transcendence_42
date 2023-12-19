document.getElementById("signUp-form").addEventListener("submit", function(event) {
	const url = backendUrl + "/authentification/register/"
	event.preventDefault();

	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;

	var formData = {
		"username": username,
		"password": password
	};

	fetch( url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json",
		},
		body: JSON.stringify(formData)
	})
		.then(response => response.json())
		.then(data => {
			if (data.error) {
				document.getElementById("error-message").innerText = "";
				document.getElementById("error-message").innerText = data.error;
				document.getElementById("error-message").style.display = "block";
			} else if (data.success) {
				document.getElementById("error-message").style.display = "none";
				document.getElementById("success-message").style.display = "block";
				document.getElementById("username").disabled = true;
				document.getElementById("password").disabled = true;
			}
		})
		.catch(error => {
			console.error("Error:", error);
		});
});

var login_link = document.getElementById("login-link");

login_link.addEventListener("click", function(){
    window.location.hash = `sign-in`;
})