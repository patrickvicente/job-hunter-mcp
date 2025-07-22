let latestJobData = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "JOB_DATA") {
    latestJobData = message.data;
  }
  if (message.type === "GET_JOB_DATA") {
    sendResponse({ data: latestJobData });
  }
});

// Open the side panel when the extension icon is clicked
chrome.action.onClicked.addListener(() => {
    chrome.windows.getCurrent({}, (window) => {
      if (window && chrome.sidePanel && chrome.sidePanel.open) {
        chrome.sidePanel.open({ windowId: window.id });
      }
    });
  });