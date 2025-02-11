
const values = [
  {
    title: "Trust",
    description: "We build and maintain trust with our customers by being transparent, reliable, and consistent in our actions and communications."
  },
  {
    title: "Integrity",
    description: "We uphold the highest standards of honesty and ethical behavior in all our dealings, ensuring that we always do what is right for our customers and stakeholders."
  },
  {
    title: "Customer-Centricity",
    description: "Our customers are at the heart of everything we do. We strive to understand their needs and provide personalized, innovative solutions that enhance their financial well-being."
  },
  {
    title: "Community",
    description: "We are deeply rooted in the communities we serve and are dedicated to their prosperity. We support local initiatives and work collaboratively to drive positive change."
  },
  {
    title: "Innovation",
    description: "We continuously seek new ways to improve our services and meet the evolving needs of our customers. We embrace change and leverage technology to deliver exceptional value."
  },
  {
    title: "Sustainability",
    description: "We promote sustainable farming practices and support initiatives that protect the environment. We are committed to creating a positive impact on the planet and future generations."
  }
];

const valuesContainer = document.getElementById('values-container');

values.forEach(value => {
  const valueDiv = document.createElement('div');
  valueDiv.className = 'value_example1';

  const valueTitle = document.createElement('h3');
  valueTitle.textContent = value.title;

  const valueDescription = document.createElement('p');
  valueDescription.textContent = value.description;

  valueDiv.appendChild(valueTitle);
  valueDiv.appendChild(valueDescription);
  valuesContainer.appendChild(valueDiv);
});
/*our services section*/
const services = [
  {
    title: "Agricultural Loans",
    description: "Tailored financing solutions to help farmers invest in equipment, seeds, and other essentials."
  },
  {
    title: "Savings Accounts",
    description: "Secure and flexible savings options designed to help our customers grow their wealth."
  },
  {
    title: "Insurance",
    description: "Comprehensive insurance plans to protect crops, livestock, and farm assets."
  },
  {
    title: "Advisory Services",
    description: "Expert advice and support on financial planning, investment, and sustainable farming practices."
  }
];

let currentIndex = 0;
const serviceTitle = document.getElementById("service-title");
const serviceDescription = document.getElementById("service-description");

function updateService() {
  const { title, description } = services[currentIndex];
  serviceTitle.textContent = title;
  serviceDescription.textContent = description;

  currentIndex = (currentIndex + 1) % services.length; // Cycle back to the first service
}

setInterval(updateService, 4000); // Change service every 4 seconds

