const url = backendUrl + "/friends/friends_view/";

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
        <p>${friend.username} - <span class="status">${friend.online_status ? 'Online' : 'Offline'}</span></p>
        <button class="add-button">ADD</button>
        <hr>
    `;

    friendElement.querySelector('.add-button').addEventListener('click', () => {
        addFriend(friend.username);
    });
    return friendElement;
}

function addFriend(username) {
    console.log(`Adding friend: ${username}`);
}


//<button class="add-button" onclick="addFriend('${friend.username}')">ADD</button>
