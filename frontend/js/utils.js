// export const makeHttpRequest = (url, options) => {
//     return fetch(url, options)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`Error HTTP! Statut: ${response.status}`);
//             }
//             return response.json();
//         })
//         .catch(error => {
//             throw error;
//         });
// }