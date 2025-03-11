// Function to preview the image when selected
function previewImage() {
  const file = document.getElementById('profileImage').files[0];
  const reader = new FileReader();
  reader.onload = function(e) {
    document.getElementById('imagePreview').src = e.target.result;
    document.getElementById('imagePreview').style.display = 'block';
  };
  reader.readAsDataURL(file);
}