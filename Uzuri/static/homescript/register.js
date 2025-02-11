
const idToAccountMap = new Map();
function generateAccountNumber() {
  const idInput = document.getElementById("Idno");
  const accountNumberInput = document.getElementById("accountNumber");
  const idNumber = idInput.value.trim();

  if (!idNumber) {
    showAlert("Please enter your ID number first.");
    return;
  }
  if (idToAccountMap.has(idNumber)) {
    // Retrieve existing account number
    accountNumberInput.value = idToAccountMap.get(idNumber);
    showAlert("Account number already exists for this ID.");
  } else {
    // Generate a new unique 10-digit account number
    let accountNumber;
    do {
      accountNumber = Math.floor(1000000000 + Math.random() * 9000000000);
    } while (Array.from(idToAccountMap.values()).includes(accountNumber));

    // Map the ID number to the new account number
    idToAccountMap.set(idNumber, accountNumber);
    accountNumberInput.value = accountNumber;
  }
}
document.querySelector('form').addEventListener('submit', function(e) {
  const email = document.getElementById('email').value;
  const phone = document.getElementById('phone').value;
  const Idno = document.getElementById('Idno').value;
  if (!email.includes('@')) {
    e.preventDefault();
    showAlert('Please enter a valid email address.');
  }
  if (!/^\d{10}$/.test(phone)) {
    e.preventDefault();
    showAlert('Please enter a valid phone number.');
  }
  /*if (!/^\d{8}$/.test(Idno)) {
    e.preventDefault();
    showAlert('Please enter a valid ID number.');
  }*/
  });