$(document).ready(function () {
  // Initialize DataTable
  $('#bootstrapdatatable').DataTable({
    "aLengthMenu": [[5, 10, 25, -1], [5, 10, 25, "All"]],
    "iDisplayLength": 5
  });

  // Account Type Filter
  $('#accountTypeDropdown').change(function () {
    var selectedType = $(this).val().toLowerCase();

    // Filter rows based on selected account type
    $('#bootstrapdatatable tbody tr').each(function () {
      var accountType = $(this).data('account-type').toLowerCase();

      if (selectedType === "" || accountType === selectedType) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
});
