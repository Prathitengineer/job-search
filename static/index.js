// Sample city data - in a real app, you would fetch this from your Flask backend
const allCities = [
    "New York", "London", "Tokyo", "Berlin", "Paris", "Sydney",
    "Toronto", "Singapore", "Dubai", "Mumbai", "San Francisco",
    "Chicago", "Los Angeles", "Hong Kong", "Shanghai", "Seoul",
    "Rome", "Madrid", "Amsterdam", "Brussels", "Vienna", "Prague",
    "Warsaw", "Moscow", "Istanbul", "Cairo", "Johannesburg",
    "Rio de Janeiro", "São Paulo", "Mexico City", "Buenos Aires",
    "Beijing", "Bangkok", "Kuala Lumpur", "Jakarta", "Manila",
    "Sydney", "Melbourne", "Auckland", "Delhi", "Bangalore"
].sort();

let selectedCities = [];

// Initialize city selector
function initCitySelector() {
    const citySelector = document.getElementById('citySelector');
    citySelector.innerHTML = '';

    allCities.forEach(city => {
        const cityOption = document.createElement('div');
        cityOption.className = 'city-option';
        cityOption.textContent = city;
        cityOption.onclick = () => toggleCitySelection(city);
        citySelector.appendChild(cityOption);
    });
}

// Filter cities based on search input
function filterCities() {
    const searchTerm = document.getElementById('citySearch').value.toLowerCase();
    const cityOptions = document.querySelectorAll('.city-option');

    cityOptions.forEach(option => {
        const cityName = option.textContent.toLowerCase();
        if (cityName.includes(searchTerm)) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

// Toggle city selection
function toggleCitySelection(city) {
    const index = selectedCities.indexOf(city);
    if (index === -1) {
        selectedCities.push(city);
    } else {
        selectedCities.splice(index, 1);
    }
    updateSelectedCities();
}

// Remove selected city
function removeCity(city) {
    selectedCities = selectedCities.filter(c => c !== city);
    updateSelectedCities();
}

// Update the display of selected cities
function updateSelectedCities() {
    const selectedCitiesContainer = document.getElementById('selectedCities');
    const cityOptions = document.querySelectorAll('.city-option');

    // Update display of selected cities
    selectedCitiesContainer.innerHTML = '';
    selectedCities.forEach(city => {
        const tag = document.createElement('div');
        tag.className = 'selected-city';
        tag.innerHTML = `${city} <span class="remove-city" onclick="removeCity('${city}')">×</span>`;
        selectedCitiesContainer.appendChild(tag);
    });

    // Update hidden input for form submission
    document.getElementById('selectedCitiesInput').value = selectedCities.join(',');

    // Update highlighting in city selector
    cityOptions.forEach(option => {
        if (selectedCities.includes(option.textContent)) {
            option.classList.add('selected');
        } else {
            option.classList.remove('selected');
        }
    });
}

function toggleLocation(element, type) {
    const options = document.querySelectorAll('.location-option');
    options.forEach(opt => opt.classList.remove('selected'));
    element.classList.add('selected');

    const citySearchContainer = document.getElementById('citySearchContainer');
    const locationInput = document.getElementById('locationInput'); // Hidden input

    if (type === 'onsite') {
        citySearchContainer.style.display = 'block';
        locationInput.value = 'onsite'; // Update hidden input
    } else {
        citySearchContainer.style.display = 'none';
        selectedCities = [];
        updateSelectedCities();
        locationInput.value = 'remote'; // Update hidden input
    }
}

// Initialize on page load
window.onload = function () {
    initCitySelector();
};