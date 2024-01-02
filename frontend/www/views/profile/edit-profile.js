function updateProfile(new_username, new_password, new_image) {
    const url = backendUrl + '/user_profile/update_profile/';
    const formData = new FormData();

    if (new_username) {
        formData.append('username', new_username);
    }

    if (new_password) {
        formData.append('password', new_password);
    }

    if (new_image.files.length > 0) {
        formData.append('fileInput', fileInput.files[0]);
    }

    fetch(url, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            window.location.href = '/#profile';
        } else {
            errorMessageElement.textContent = data.message;
        }
    })
    .catch(error => {
        console.error(error.message);
    });
}

function saveProfile() {
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const fileInput = document.getElementById('fileInput');

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    const usernamePattern = /^[a-zA-Z0-9]+$/;
    const passwordPattern = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[A-Z]).{8,}$/;

    if (username || password || fileInput.files.length > 0) {
        if (username) {
            if (!usernamePattern.test(username)) {
                alert("Username must contain only alphanumeric characters.");
                return;
            }
        }
        if (password) {
            if (!passwordPattern.test(password)) {
                alert("Password must contain at least 8 characters, 1 digit, 1 special character, and 1 uppercase letter.");
                return;
            }
        }
        updateProfile(username, password, fileInput)
    }
    else {
        alert("Nothing has been entered!")
    }
}

savebtn.addEventListener("click", saveProfile);