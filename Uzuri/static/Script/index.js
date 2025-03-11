document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript Loaded Successfully!");

  // === Transaction Popup ===
  const transactionPopup = document.getElementById("transactionPopupOverlay");
  const transactionBtn = document.getElementById("transactionButton");
  const transactionClose = document.getElementById("transactionCancelButton");

  if (transactionBtn && transactionPopup) {
      transactionBtn.addEventListener("click", function () {
          console.log("Opening Transaction Popup");
          transactionPopup.style.display = "flex";
      });

      transactionClose.addEventListener("click", function () {
          console.log("Closing Transaction Popup");
          transactionPopup.style.display = "none";
      });
  }

  // === Deposit Popup ===
  const depositPopup = document.getElementById("depositPopupOverlay");
  const depositBtn = document.getElementById("depositButton");
  const depositClose = document.getElementById("cancelButton");

  if (depositBtn && depositPopup) {
      depositBtn.addEventListener("click", function () {
          console.log("Opening Deposit Popup");
          depositPopup.style.display = "flex";
      });

      depositClose.addEventListener("click", function () {
          console.log("Closing Deposit Popup");
          depositPopup.style.display = "none";
      });
  }

  // === Transaction History Popup ===
  const transactionHistoryPopup = document.getElementById("popupOverlay");
  const transactionHistoryBtn = document.getElementById("viewTransactionBtn");
  const transactionHistoryClose = document.getElementById("closePopup");

  if (transactionHistoryBtn && transactionHistoryPopup) {
      transactionHistoryBtn.addEventListener("click", function () {
          console.log("Opening Transaction History Popup");
          transactionHistoryPopup.style.display = "flex";
      });

      transactionHistoryClose.addEventListener("click", function () {
          console.log("Closing Transaction History Popup");
          transactionHistoryPopup.style.display = "none";
      });
  }

  // Close popups when clicking outside
  document.querySelectorAll(".popup-overlay").forEach((popup) => {
      popup.addEventListener("click", function (event) {
          if (event.target === popup) {
              console.log("Clicked outside, closing popup");
              popup.style.display = "none";
          }
      });
  });
});
