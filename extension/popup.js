document.getElementById('printHtml').addEventListener('click', function() {
    const robotText = document.getElementById('robotText');

    robotText.innerText = 'Checking news...';

    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ['contentScript.js']
        });
    });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'contentExtracted' && message.content) {
        const robotText = document.getElementById('robotText');
        const confidenceText = document.getElementById('confidence');
        const container = document.getElementById('container');
        // Send the content to the endpoint
        fetch('http://127.0.0.1:7000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: message.content })
        })
        .then(response => response.json())
        .then(data => {
            // Set background color based on response
            if (data.fake) {
                if (data.confidence && data.confidence > 0.65) {
                    container.classList.add('fake');
                    robotText.innerText = 'This news contains fake information.';
                } else {
                    container.classList.add('maybe');
                    robotText.innerText = 'This news may contain fake information. Please do some more research on it!';
                }
            } else {
                if (data.confidence && data.confidence > 0.65) {
                    container.classList.add('real');
                    robotText.innerText = 'This news does not contain fake information.';
                } else {
                    container.classList.add('maybe');
                    robotText.innerText = 'This news may contain fake information. Please do some more research on it!';
                }
            }
            if (data.confidence) {
                confidenceText.innerText = `Confidence: ${roundFloat(data.confidence * 100)}%`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            robotText.innerText = 'An error happened while trying to check the news. Please try again later';
        });
    }
});


function roundFloat(num) {
    return Math.round(num * 100) / 100;
}