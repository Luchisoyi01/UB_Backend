$(document).ready(function () {
  // Initialize DataTable
  $('#bootstrapdatatable').DataTable({
    "aLengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
    "iDisplayLength": 10
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
