// Load the list of poems from JSON and populate the div
async function loadPoemsList() {
  const container = document.getElementById('poem-list');
  try {
    const response = await fetch('res/poems.json');
    const poems = await response.json();

    container.innerHTML = ''; // Clear old content first
    poems.forEach(poem => {
      const link = document.createElement('a');
      link.className = 'poem-link';
      link.href = `poem.html?id=${poem.id}`;
      link.textContent = `${poem.id}. ${poem.title}`;
      link.style.display = 'block'; // Make each link on a new line

      link.style.margin = '5px 0';
      container.appendChild(link);
    });
  } catch (error) {
    container.textContent = 'Could not load poems.';
    console.error('Error loading poems:', error);
  }
}

// Toggle visibility of the poem list
function setupToggle() {
  const toggleButton = document.getElementById('toggle-poems');
  const container = document.getElementById('poem-list');

  toggleButton.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent link navigation
    if (container.style.display === 'none' || container.style.display === '') {
      container.style.display = 'block';
    } else {
      container.style.display = 'none';
    }
  });
}

// Initialize everything after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  loadPoemsList();
  setupToggle();
});
