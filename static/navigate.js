const bookSelect = document.querySelector('#book');
const chapterSelect = document.querySelector('#chapter');

function updateChapterSelect() {
  // get the selected book
  const book = bookSelect.value;
  // make an AJAX request to the /chapters route to get the number of chapters for the selected book
  fetch(`/chapters/${book}`)
    .then(response => response.json())
    .then(data => {
      // remove all options from the chapter select
      chapterSelect.innerHTML = '';
      // get the number of chapters from the JSON response
      const numChapters = data.num_chapters;
      // add options for each chapter
      for (let i = 1; i <= numChapters; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        if (window.chapterNumber && window.chapterNumber === i) {
            option.selected = true;
        }
        chapterSelect.appendChild(option);
      }
    });
}

bookSelect.addEventListener('change', updateChapterSelect);

// trigger the change event on the book select when the page loads
updateChapterSelect();