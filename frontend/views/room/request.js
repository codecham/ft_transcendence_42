// export const username = getUserName();

// async function fetchData(url) {
// 	try {
// 	  const response = await fetch(url);
  
// 	  if (!response.ok) {
// 		throw new Error(`HTTP error! Status: ${response.status}`);
// 	  }
  
// 	  const data = await response.json();
// 	  return data;
// 	} catch (error) {
// 	  console.error('Error fetching data:', error.message);
// 	  throw error;
// 	}
//   }

// async function getUserName() {
// 	const data = await fetchData(backendUrl + '/authentification/user_info/');
// 	const usernameElem = document.getElementById("username-btn");

// 	usernameElem.innerHTML = '';
// 	usernameElem.innerHTML = data.username;
// 	return data.username;
// }
