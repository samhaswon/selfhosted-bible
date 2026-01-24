// Minify using: https://www.digitalocean.com/community/tools/minify
const bookSelect = document.querySelector('#book');
const chapterSelect = document.querySelector('#chapter');
const gridContainer = document.querySelector('#grid-container');
const gridItemTemplate = document.querySelector('#grid-item-template');
const addGridRowButton = document.querySelector('#add-grid-row');
const bookChapters = {'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36, 'Deuteronomy': 34, 'Joshua': 24, 'Judges': 21, 'Ruth': 4, '1 Samuel': 31, '2 Samuel': 24, '1 Kings': 22, '2 Kings': 25, '1 Chronicles': 29, '2 Chronicles': 36, 'Ezra': 10, 'Nehemiah': 13, 'Esther': 10, 'Job': 42, 'Psalms': 150, 'Proverbs': 31, 'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66, 'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12, 'Hosea': 14, 'Joel': 3, 'Amos': 9, 'Obadiah': 1, 'Jonah': 4, 'Micah': 7, 'Nahum': 3, 'Habakkuk': 3, 'Zephaniah': 3, 'Haggai': 2, 'Zechariah': 14, 'Malachi': 4, 'Matthew': 28, 'Mark': 16, 'Luke': 24, 'John': 21, 'Acts': 28, 'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13, 'Galatians': 6, 'Ephesians': 6, 'Philippians': 4, 'Colossians': 4, '1 Thessalonians': 5, '2 Thessalonians': 3, '1 Timothy': 6, '2 Timothy': 4, 'Titus': 3, 'Philemon': 1, 'Hebrews': 13, 'James': 5, '1 Peter': 5, '2 Peter': 3, '1 John': 5, '2 John': 1, '3 John': 1, 'Jude': 1, 'Revelation': 22};

let nextGridIndex = 0;

async function chapterOptions(count, chapterSelectElement, preferredChapter = null) {
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
        if (preferredChapter !== null && Number(preferredChapter) === i) {
            option.selected = true;
        } else if (preferredChapter === null && window.chapterNumber && window.chapterNumber == i) {
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
    if (iframe.dataset.gridMode === 'search') {
        return;
    }
    iframe.src = `/embed?version=${versionSelector.value}&book=${bookSelector.value}&chapter=${chapterSelector.value}`;
}

function assignGridIds(itemRoot, index) {
    const bookLabel = itemRoot.querySelector('[data-grid-role="book-label"]');
    const bookSelector = itemRoot.querySelector('[data-grid-role="book"]');
    const chapterLabel = itemRoot.querySelector('[data-grid-role="chapter-label"]');
    const chapterSelector = itemRoot.querySelector('[data-grid-role="chapter"]');
    const versionLabel = itemRoot.querySelector('[data-grid-role="version-label"]');
    const versionSelector = itemRoot.querySelector('[data-grid-role="version"]');
    const iframe = itemRoot.querySelector('[data-grid-role="iframe"]');

    if (bookSelector) {
        bookSelector.id = `book-${index}`;
        bookSelector.name = 'book';
    }
    if (chapterSelector) {
        chapterSelector.id = `chapter-${index}`;
        chapterSelector.name = 'chapter';
    }
    if (versionSelector) {
        versionSelector.id = `version-selection-${index}`;
    }
    if (iframe) {
        iframe.id = `bible-frame-${index}`;
        iframe.title = `Bible frame ${index}`;
    }
    if (bookLabel) {
        bookLabel.setAttribute('for', `book-${index}`);
        bookLabel.setAttribute('aria-label', `Book selection ${index}`);
    }
    if (chapterLabel) {
        chapterLabel.setAttribute('for', `chapter-${index}`);
        chapterLabel.setAttribute('aria-label', `Chapter selection ${index}`);
    }
    if (versionLabel) {
        versionLabel.setAttribute('for', `version-selection-${index}`);
        versionLabel.setAttribute('aria-label', `Version selection ${index}`);
    }
    itemRoot.dataset.gridIndex = index;
}

function initGridItem(itemRoot) {
    const bookSelector = itemRoot.querySelector('[data-grid-role="book"]');
    const chapterSelector = itemRoot.querySelector('[data-grid-role="chapter"]');
    const versionSelector = itemRoot.querySelector('[data-grid-role="version"]');
    const bibleFrame = itemRoot.querySelector('[data-grid-role="iframe"]');

    if (!bookSelector || !chapterSelector || !versionSelector || !bibleFrame) {
        return;
    }

    updateThisChapterSelect(bookSelector, chapterSelector);

    bookSelector.addEventListener('change', async function() {
        updateThisChapterSelect(bookSelector, chapterSelector);
    });

    const updateFrame = async function() {
        updateiframe(bibleFrame, bookSelector, chapterSelector, versionSelector);
    };
    bookSelector.addEventListener('change', updateFrame);
    chapterSelector.addEventListener('change', updateFrame);
    versionSelector.addEventListener('change', updateFrame);
}

function loadExistingGridItems() {
    if (!gridContainer) {
        return;
    }
    let maxIndex = -1;
    const items = gridContainer.querySelectorAll('[data-grid-item]');
    items.forEach((item) => {
        const index = Number.parseInt(item.dataset.gridIndex, 10);
        if (!Number.isNaN(index)) {
            maxIndex = Math.max(maxIndex, index);
        }
        initGridItem(item);
    });
    nextGridIndex = maxIndex + 1;
}

function createGridItem(index) {
    if (!gridItemTemplate) {
        return null;
    }
    const fragment = gridItemTemplate.content.cloneNode(true);
    const itemRoot = fragment.querySelector('[data-grid-item]');
    if (!itemRoot) {
        return null;
    }
    assignGridIds(itemRoot, index);
    const chapterSelector = itemRoot.querySelector('[data-grid-role="chapter"]');
    const bookSelector = itemRoot.querySelector('[data-grid-role="book"]');
    if (bookSelector && chapterSelector) {
        chapterOptions(bookChapters[bookSelector.value], chapterSelector, 1);
    }
    return { fragment, itemRoot };
}

function createGridSpacer() {
    const spacerFragment = document.createDocumentFragment();
    spacerFragment.appendChild(document.createElement('br'));
    const spacer = document.createElement('span');
    spacer.style.width = '2%';
    spacer.innerHTML = '&nbsp;';
    spacerFragment.appendChild(spacer);
    spacerFragment.appendChild(document.createElement('br'));
    return spacerFragment;
}

function addGridRow() {
    if (!gridContainer) {
        return;
    }
    const row = document.createElement('div');
    row.className = 'container';

    const leftItem = createGridItem(nextGridIndex);
    if (leftItem) {
        row.appendChild(leftItem.fragment);
        initGridItem(leftItem.itemRoot);
        nextGridIndex += 1;
    }

    row.appendChild(createGridSpacer());

    const rightItem = createGridItem(nextGridIndex);
    if (rightItem) {
        row.appendChild(rightItem.fragment);
        initGridItem(rightItem.itemRoot);
        nextGridIndex += 1;
    }

    gridContainer.appendChild(row);
    gridContainer.appendChild(document.createElement('hr'));
}

function toggleSearchView(index) {
    if (!gridContainer) {
        return;
    }
    const itemRoot = gridContainer.querySelector(`[data-grid-index="${index}"]`);
    if (!itemRoot) {
        return;
    }
    const bookSelector = itemRoot.querySelector('[data-grid-role="book"]');
    const chapterSelector = itemRoot.querySelector('[data-grid-role="chapter"]');
    const versionSelector = itemRoot.querySelector('[data-grid-role="version"]');
    const bibleFrame = itemRoot.querySelector('[data-grid-role="iframe"]');
    if (!bibleFrame || !bookSelector || !chapterSelector || !versionSelector) {
        return;
    }
    if (bibleFrame.dataset.gridMode === 'search') {
        delete bibleFrame.dataset.gridMode;
        updateiframe(bibleFrame, bookSelector, chapterSelector, versionSelector);
    } else {
        bibleFrame.dataset.gridMode = 'search';
        bibleFrame.src = '/search_embed';
    }
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
} else if (gridContainer) {
    try {
        loadExistingGridItems();
        const searchButtons = gridContainer.querySelectorAll('[data-search-toggle]');
        searchButtons.forEach((buttonEl) => {
            buttonEl.addEventListener('click', () => {
                const targetIndex = Number.parseInt(buttonEl.dataset.gridIndex, 10);
                if (!Number.isNaN(targetIndex)) {
                    toggleSearchView(targetIndex);
                }
            });
        });
        if (addGridRowButton) {
            addGridRowButton.addEventListener('click', addGridRow);
        }
        /* Fix iframes not following theming */
        if (button) {
            button.addEventListener("click", () => {
                const gridFrames = gridContainer.querySelectorAll('[data-grid-role="iframe"]');
                gridFrames.forEach((frame) => {
                    try {
                        frame.contentWindow.document.querySelector("html").setAttribute(
                            "data-theme",
                            currentThemeSetting
                        );
                    } catch (e) {
                        console.log(e);
                    }
                });
            });
        }
    } catch (e) {
        console.log(e);
        console.log("Unable to get any navigation selectors.");
    }
}
