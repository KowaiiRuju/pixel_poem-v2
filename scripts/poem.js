// Loads a single poem based on the "id" parameter in the URL
async function loadPoem() {
  const content = document.getElementById('poem-content');
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const poemId = parseInt(urlParams.get('id'));

    if (!poemId) {
      content.textContent = 'No poem selected.';
      return;
    }

    const response = await fetch('res/poems.json');
    const poems = await response.json();

    const poem = poems.find(p => p.id === poemId);
    if (!poem) {
      content.textContent = 'Poem not found.';
      return;
    }

    // Set the page title dynamically
    document.title = `${poem.title} - Poem`;

    // Build the poem HTML
    content.innerHTML = '';

    // Title
    const title = document.createElement('h2');
    title.className = 'poem-title';
    title.textContent = poem.title;
    content.appendChild(title);

    // Render each line as a <p> so the browser wraps long lines naturally.
    // Blank lines between stanzas become a small spacer <div>.
    const lines = poem.text.split('\n');
    lines.forEach(line => {
      if (line.trim() === '') {
        // Stanza break — add visible spacing between stanzas
        const spacer = document.createElement('div');
        spacer.className = 'stanza-break';
        content.appendChild(spacer);
      } else {
        const p = document.createElement('p');
        p.className = 'poem-line';
        p.textContent = line;
        content.appendChild(p);
      }
    });

  } catch (error) {
    content.textContent = 'Could not load poem.';
    console.error(error);
  }
}

// Run when the page loads
document.addEventListener('DOMContentLoaded', loadPoem);
