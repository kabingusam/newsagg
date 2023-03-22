// Function to add an article to bookmarks
function addBookmark(url, title) {
    // Get the bookmarks from local storage
    let bookmarks = JSON.parse(localStorage.getItem('bookmarks')) || [];

    // Check if the article is already bookmarked
    let existingBookmark = bookmarks.find(bookmark => bookmark.url === url);
    if (existingBookmark) {
        alert('Article already bookmarked!');
        return;
    }

    // Add the article to bookmarks
    bookmarks.push({ url: url, title: title });
    localStorage.setItem('bookmarks', JSON.stringify(bookmarks));

    alert('Article bookmarked!');
}

// Function to remove an article from bookmarks
function removeBookmark(url) {
    // Get the bookmarks from local storage
    let bookmarks = JSON.parse(localStorage.getItem('bookmarks')) || [];

    // Find the bookmarked article and remove it from bookmarks
    bookmarks = bookmarks.filter(bookmark => bookmark.url !== url);
    localStorage.setItem('bookmarks', JSON.stringify(bookmarks));

    alert('Article removed from bookmarks!');
}

// Function to check if an article is bookmarked
function isBookmarked(url) {
    // Get the bookmarks from local storage
    let bookmarks = JSON.parse(localStorage.getItem('bookmarks')) || [];

    // Check if the article is bookmarked
    let existingBookmark = bookmarks.find(bookmark => bookmark.url === url);
    return existingBookmark ? true : false;
}
