// TimerHaven Background Service Worker (MV3)

chrome.runtime.onInstalled.addListener(() => {
  console.log('TimerHaven Extension Installed.');
  
  // Create Context Menu for quick clipping
  chrome.contextMenus.create({
    id: "addToTimerHaven",
    title: "Add to TimerHaven Clips",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "addToTimerHaven") {
    const selectedText = info.selectionText;
    console.log('Clipping to TimerHaven:', selectedText);
    
    // Future: Use chrome.storage.local to sync with the website's clipboard manager
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.webp',
      title: 'Clipped to TimerHaven',
      message: 'Your selection has been saved for your next session.',
      priority: 2
    });
  }
});
