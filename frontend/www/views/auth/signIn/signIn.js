var login_link = document.getElementById("register-link");


login_link.addEventListener("click", function(){
    window.location.hash = `sign-up`;
})


document.getElementById("signUp-form").addEventListener("submit", function(event) {
	const url = backendUrl + "/authentification/login/"
	event.preventDefault();

	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;

	var formData = {
		"username": username,
		"password": password
	};

	fetch(url, {
		method: "POST",
		headers: {
		  "Content-Type": "application/json",
		  "Accept": "application/json",
		},
		body: JSON.stringify(formData)
	  })
		.then(response => {
		  if (!response.ok) {
			document.getElementById("error-message").innerText = "";
			document.getElementById("error-message").innerText = "Request error: " + response.statusText;
			document.getElementById("error-message").style.display = "block";
			throw new Error(`Request failed with status ${response.status}`);
		  }
		  return response.json();
		})
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
			window.location.hash = `home`;
		  }
		})
		.catch(error => {
			console.error("Error: " + error);
		});
});

var login_link = document.getElementById("register-link");


login_link.addEventListener("click", function(){
    window.location.hash = `sign-up`;
})