const avatarForm = document.getElementById('avatarForm');
const url = backendUrl + '/user_profile/update_profile_image/';

avatarForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('profile_image', file);

        fetch(url, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Profile image update success:', data);
            // Handle success, update UI, etc.
        })
        .catch(error => {
            console.error('Profile image update error:', error);
            // Handle error, show error message, etc.
        });
    } else {
        console.log('No file selected.');
    }
});
