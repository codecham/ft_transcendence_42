/*

    Function called to redirect on the user page when someone click on a username 

*/
function redirect_other_profile(username) {
    window.location.hash = `other_profile?username=${username}`;
}



/*

    Function called for remove a friend. Reload the page if it's ok

*/
function removeFriend(username) {
    const url = backendUrl + `/friends/remove_friend_view/${username}`;

    fetch(url, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        location.reload();
    })
    .catch(error => {
        console.error('Request failed:', error);
    });
}


/*

    Set the friend list

*/
function set_friend_list() {
    const url = backendUrl + "/friends/friends_list_view/";

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const friendsContainer = document.getElementById('friends-container');
                data.friends.forEach(friend => {
                    const friendElement = createFriendElement(friend);
                    friendsContainer.appendChild(friendElement);
                });
            });

        function createFriendElement(friend) {
            const friendElement = document.createElement('div');
            friendElement.classList.add(friend.online_status ? 'online-status-true' : 'online-status-false');
            friendElement.innerHTML = `
                <p class="other_user">${friend.username} - <span class="status">${friend.online_status ? 'Online' : 'Offline'}</span></p>
                <button class="remove-button">REMOVE</button>
                <hr>
            `;

            friendElement.querySelector('.remove-button').addEventListener('click', () => {
                removeFriend(friend.username);
            });

            friendElement.querySelector('.other_user').addEventListener('click', () => {
                redirect_other_profile(friend.username);
            });

            return friendElement;
        }
}



/*

    Function called for add a friend. Reload the page if it's ok

*/
function addFriend(username) {
    const url = backendUrl + `/friends/add_friend_view/${username}`;

    fetch(url, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        location.reload();
    })
    .catch(error => {
        console.error('Request failed:', error);
    });
}


/*

    set the user non friend list

*/
function set_user_list() {
    const url = backendUrl + "/friends/non_friends_list_view/";

        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const userContainer = document.getElementById('user-container');
                data.user.forEach(user => {
                    const userElement = createUserElement(user);
                    userContainer.appendChild(userElement);
                });
            });

        function createUserElement(user) {
            const userElement = document.createElement('div');
            userElement.innerHTML = `
                <p class="other_user">${user.username}</p>
                <button class="add-button">ADD</button>
                <hr>
            `;

            userElement.querySelector('.add-button').addEventListener('click', () => {
                addFriend(user.username);
            });

            userElement.querySelector('.other_user').addEventListener('click', () => {
                redirect_other_profile(user.username);
            });

            return userElement;
        }
}

set_friend_list();
set_user_list();