const profileImageUrl = backendUrl + "/user_profile/get_profile_image/";

// Utilisez fetch pour récupérer l'image
fetch(profileImageUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.blob();
    })
    .then(blob => {
        // Convertissez le blob en URL d'objet
        const imageUrl = URL.createObjectURL(blob);

        // Utilisez imageUrl comme source pour votre image HTML
        const profileImageElement = document.getElementById('profile-image');
        profileImageElement.src = imageUrl;
    })
    .catch(error => {
        console.error("Error fetching profile image:", error);
    });

function updateUsername(username) {
    const url = backendUrl + '/user_profile/update_user_name/';
    var formData = {
        "user_name": username
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
            console.error('Error:', error.message);
        });
}

function updatePassword(password) {
    const url = backendUrl + '/user_profile/update_password/';
    var formData = {
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
        .then(response => response.json())
        .then(data => {
            console.log("Update username success:", data);
            return true;
            // Handle success, update UI, etc.
        })
        .catch(error => {
            console.error("Update username error:", error);
            return false;
            // Handle error, show error message, etc.
        });
}

function updateProfileImage(file) {
    const url = backendUrl + '/user_profile/update_profile_image/';
    const formData = new FormData();
    formData.append('profile_image', file);

    fetch(url, {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log("Update profile_image success:", data);
            return true;
            // Handle success, update UI, etc.
        })
        .catch(error => {
            console.error("Update profile_image error:", error);
            // Handle error, show error message, etc.
        });
}

function update_profile(new_username, new_password, new_image) {
    console.log(new_username)
    console.log(new_password)
    console.log(new_image)

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
        console.error('Error:', error.message);
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

    if (username || password || fileInput) {
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
        update_profile(username, password, fileInput)
    }

}

savebtn.addEventListener("click", saveProfile);