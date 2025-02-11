function showAlert(message) {
  const modal = document.getElementById("customAlert");
  const alertMessage = document.getElementById("alertMessage");

  alertMessage.textContent = message;
  modal.style.display = "flex";
}

// Function to close the custom alert
function closeAlert() {
  const modal = document.getElementById("customAlert");
  modal.style.display = "none";
}