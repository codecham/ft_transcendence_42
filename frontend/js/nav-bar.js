'Use strict'

const profile_btn = document.getElementById("profile-btn");
profile_btn.addEventListener('click', function(){
    window.location.hash = `profile`;
});
