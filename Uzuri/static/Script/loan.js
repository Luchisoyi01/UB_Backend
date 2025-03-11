// the loan page JS code
document.getElementById('applyBtn').addEventListener('click', function() {
  document.getElementById('popupForm').style.display = 'flex';
});

// Close the loan application popup without applying
document.getElementById('cancelBtn').addEventListener('click', function() {
  document.getElementById('popupForm').style.display = 'none';
});



// Show the payment popup
document.getElementById('payBtn').addEventListener('click', function() {
  const approvedLoans = document.querySelectorAll('#loanTable tbody tr td:nth-child(3)');
  const loanSelect = document.getElementById('loanSelect');
  loanSelect.innerHTML = ''; // Clear the select options

  approvedLoans.forEach((statusCell, index) => {
      if (statusCell.textContent === 'Approved') {
          const row = document.getElementById('loanTable').rows[index + 1];
          const loanAmount = row.cells[0].textContent;
          const loanReason = row.cells[1].textContent;

          const option = document.createElement('option');
          option.value = index;
          option.textContent = `${loanAmount} - ${loanReason}`;
          loanSelect.appendChild(option);
      }
  });

  document.getElementById('paymentForm').style.display = 'flex';
});

// Close the payment popup without paying
document.getElementById('cancelPaymentBtn').addEventListener('click', function() {
  document.getElementById('paymentForm').style.display = 'none';
});


// Highlight the loan amount cell when the user starts typing
const popup = document.getElementById("paymentForm");
  const closeButton = document.getElementById("closePopup");

  // Close the popup when the close button is clicked
  closeButton.onclick = function() {
    popup.style.display = "none";
  }

  // Optionally, you can also close the popup when clicking outside of the popup content
  window.onclick = function(event) {
    if (event.target == popup) {
      popup.style.display = "none";
    }
  }