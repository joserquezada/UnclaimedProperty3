console.log("Background service worker started.");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Background received message:", message);

  if (message.type !== "SAVE_CAPTURE") {
    sendResponse({ ok: false, reason: "Unknown message type" });
    return;
  }

  const capture = message.payload;

  const blob = new Blob([JSON.stringify(capture.response, null, 2)], {
    type: "application/json",
  });

  const reader = new FileReader();

  reader.onload = () => {
    chrome.downloads.download({
      url: reader.result,
      filename: `unclaimed_property/capture_${Date.now()}.json`,
      saveAs: false,
    });

    sendResponse({ ok: true });
  };

  reader.readAsDataURL(blob);

  return true;
});