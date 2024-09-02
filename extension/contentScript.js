function extractNewsContent() {
    let content = "";

    const article = document.querySelector('article');
    const mainContent = document.querySelector('main');
    const mainDiv = document.querySelector('div.main-content');

    if (article) {
    content = article.innerText;
    } else if (mainContent) {
    content = mainContent.innerText;
    } else if (mainDiv) {
    content = mainDiv.innerText;
    } else {
    content = document.body.innerText;
    }

    content = content.trim();

    console.log("Extracted content:", content);
    chrome.runtime.sendMessage({ action: 'logContent', content: content });

    chrome.runtime.sendMessage({ action: 'contentExtracted', content: content });
}

extractNewsContent();