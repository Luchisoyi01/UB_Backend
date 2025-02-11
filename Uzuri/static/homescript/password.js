
const gridContainer = document.querySelector('.grid-container');
const images = Array.from({ length: 16 }, (_, i) => ({
 id: `img${i + 1}`, 
 src: '{% static "password/' + (i + 1) + '.avif" %}', 
 alt: `Image ${i + 1}`
}));
images.forEach(image => {
  const gridItem = document.createElement('div');
  gridItem.className = 'grid-item';
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = image.id;
  const img = document.createElement('img');
  img.src = image.src;
  img.alt = image.alt;
  gridItem.appendChild(checkbox);
  gridItem.appendChild(img);
  gridContainer.appendChild(gridItem);
});
const selectedImages = [];
gridContainer.addEventListener('change', (event) => {
  if (event.target.type === 'checkbox') {
    const imgElement = event.target.nextElementSibling;
    const imgSrc = imgElement.getAttribute('src');

    if (event.target.checked) {
      selectedImages.push(imgSrc);
    } else {
      const index = selectedImages.indexOf(imgSrc);
      if (index > -1) {
        selectedImages.splice(index, 1);
      }
    }
    console.log('Selected Images:', selectedImages);
  }
});
