// Minify using: https://www.digitalocean.com/community/tools/minify
const bookSelect = document.querySelector('#book');
const chapterSelect = document.querySelector('#chapter');
const bookChapters = {'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36, 'Deuteronomy': 34, 'Joshua': 24, 'Judges': 21, 'Ruth': 4, '1 Samuel': 31, '2 Samuel': 24, '1 Kings': 22, '2 Kings': 25, '1 Chronicles': 29, '2 Chronicles': 36, 'Ezra': 10, 'Nehemiah': 13, 'Esther': 10, 'Job': 42, 'Psalms': 150, 'Proverbs': 31, 'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66, 'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12, 'Hosea': 14, 'Joel': 3, 'Amos': 9, 'Obadiah': 1, 'Jonah': 4, 'Micah': 7, 'Nahum': 3, 'Habakkuk': 3, 'Zephaniah': 3, 'Haggai': 2, 'Zechariah': 14, 'Malachi': 4, 'Matthew': 28, 'Mark': 16, 'Luke': 24, 'John': 21, 'Acts': 28, 'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13, 'Galatians': 6, 'Ephesians': 6, 'Philippians': 4, 'Colossians': 4, '1 Thessalonians': 5, '2 Thessalonians': 3, '1 Timothy': 6, '2 Timothy': 4, 'Titus': 3, 'Philemon': 1, 'Hebrews': 13, 'James': 5, '1 Peter': 5, '2 Peter': 3, '1 John': 5, '2 John': 1, '3 John': 1, 'Jude': 1, 'Revelation': 22};

var bookSelectors = [], chapterSelectors = [], versionSelectors = [], bibleFrames = [];

async function chapterOptions(count, chapterSelectElement) {
    if (chapterSelectElement.value) {
        window.chapterNumber = chapterSelectElement.value;
    }
    // remove all options from the chapter select
    chapterSelectElement.innerHTML = '';
    // add options for each chapter
    for (let i = 1; i <= count; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        if (window.chapterNumber && window.chapterNumber == i) {
            option.selected = true;
        }
        chapterSelectElement.appendChild(option);
    }
}

async function updateChapterSelect() {
  // get the selected book
  const book = bookSelect.value;
  chapterOptions(bookChapters[book], chapterSelect);
}
async function updateThisChapterSelect(bookSelector, chapterSelector) {
  // get the selected book
  const book = bookSelector.value;
  chapterOptions(bookChapters[book], chapterSelector);
}

async function updateiframe(iframe, bookSelector, chapterSelector, versionSelector) {
    iframe.src = `/embed?version=${versionSelector.value}&book=${bookSelector.value}&chapter=${chapterSelector.value}`;
}

if (bookSelect) {
    for (let i = 0; i < bookSelect.length; i++) {
        if (bookSelect.options[i].label === book) {
            bookSelect.selectedIndex = i;
        }
    }
    bookSelect.addEventListener('change', updateChapterSelect);

    // trigger the change event on the book select when the page loads
    updateChapterSelect();
} else {
    try {
        for (let i = 0; i < 4; i++) {
            bookSelectors.push(document.querySelector(`#book-${i}`));
            chapterSelectors.push(document.querySelector(`#chapter-${i}`));
            versionSelectors.push(document.querySelector(`#version-selection-${i}`));
            bibleFrames.push(document.querySelector(`#bible-frame-${i}`));
        }
        for (let i = 0; i < 4; i++) {
            bookSelectors[i].addEventListener(
                'change',
                async function() {
                    updateThisChapterSelect(
                        bookSelectors[i],
                        chapterSelectors[i]
                    );
                }
            );
            updateThisChapterSelect(
                bookSelectors[i],
                chapterSelectors[i]
            );
        }
        /* Add listeners to update the iframes */
        for (let i = 0; i < 4; i++) {
            bookSelectors[i].addEventListener('change', async function() {
                updateiframe(
                    bibleFrames[i],
                    bookSelectors[i],
                    chapterSelectors[i],
                    versionSelectors[i]
                );
            });
            chapterSelectors[i].addEventListener('change', async function() {
                updateiframe(
                    bibleFrames[i],
                    bookSelectors[i],
                    chapterSelectors[i],
                    versionSelectors[i]
                );
            });
            versionSelectors[i].addEventListener('change', async function() {
                updateiframe(
                    bibleFrames[i],
                    bookSelectors[i],
                    chapterSelectors[i],
                    versionSelectors[i]
                );
            });
        }
        /* Fix iframes not following theming */
        button.addEventListener("click", (event) => {
            for (let i = 0; i < 4; i++) {
                document.querySelector(`#bible-frame-${i}`).contentWindow.document.querySelector("html").setAttribute("data-theme", currentThemeSetting);
            }
        });
    } catch {(e) => {
        console.log(e);
        console.log("Unable to get any navigation selectors.");
    }
    }
}
