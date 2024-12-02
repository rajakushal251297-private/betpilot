//  // Example: Fetching user data dynamically
//  document.addEventListener("DOMContentLoaded", function () {
//     const username = "User123"; // Example username
//     const email = "user@example.com"; // Example email
//     const walletBalance = "₹5000"; // Example balance

//     document.querySelector(".username").innerText = `Username: ${username}`;
//     document.querySelector(".email-id").innerText = `Email: ${email}`;
//     document.querySelector(".wallet-balance").innerText = `Wallet Balance: ${walletBalance}`;
// });

document.getElementById("withdrawId").addEventListener("click", function () { window.location.href = "/withdraw";});
document.getElementById("depositId").addEventListener("click", function () { window.location.href = "/deposit";});

document.getElementById("userlogoutbtn").addEventListener("click", function (){
    window.location.href = "/logout"
})