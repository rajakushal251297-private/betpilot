// Get modal element
const modal = document.getElementById("walletModal");
// Get open modal button
const walletButton = document.querySelector(".wallet-button");
// Get close button
const closeButton = document.getElementById("closeModal");

// Listen for open click
walletButton.addEventListener("click", () => {
  modal.style.display = "block"; // Show the modal
});

// Listen for close click
closeButton.addEventListener("click", () => {
  modal.style.display = "none"; // Hide the modal
});

// Listen for outside click to close modal
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none"; // Hide the modal
  }
});

document.getElementById("withdraw").addEventListener("click", () => {
  window.location.href ="/withdraw";
});

document.getElementById('recharge').onclick = function() {
  window.location.href = "/deposit";
    // document.getElementById('rechargeModal').style.display = 'block';
};

document.getElementById('closeRechargeModal').onclick = function() {
    document.getElementById('rechargeModal').style.display = 'none';
};

// Close the recharge modal when clicking outside of it
window.onclick = function(event) {
    if (event.target === document.getElementById('rechargeModal')) {
        document.getElementById('rechargeModal').style.display = 'none';
    }
};



