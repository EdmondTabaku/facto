chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'logContent' && message.content) {
        console.log('Extracted Content:', message.content);
    }
});
  