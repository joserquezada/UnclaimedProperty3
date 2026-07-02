console.log("Background service worker started.");

let latestCapture = null;

function safeFilePart(value) {
  if (!value) return "unknown";

  return String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 80);
}


function downloadCapture(capture) {

  const query =
    capture.request?.lastName ||
    capture.request?.ownerName ||
    capture.request?.query ||
    "search";

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

  const filename = `unclaimed_property/${safeFilePart(
    query
  )}_${timestamp}.json`;

  const blob = new Blob([JSON.stringify(capture.response, null, 2)], {
    type: "application/json",
  });

  const reader = new FileReader();

  reader.onload = () => {
    chrome.downloads.download({
      url: reader.result,
      filename,
      saveAs: false,
    });
  };

  reader.readAsDataURL(blob);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SAVE_CAPTURE") {
    latestCapture = message.payload;
    console.log("Stored latest capture:", latestCapture.url);

    // Do NOT auto-download now.
    sendResponse({ ok: true });
    return;
  }

  if (message.type === "DOWNLOAD_LATEST_CAPTURE") {
    if (!latestCapture) {
      sendResponse({ ok: false, error: "No capture available yet." });
      return;
    }

    downloadCapture(latestCapture);
    sendResponse({ ok: true });
    return;
  }

  if (message.type === "GET_LATEST_CAPTURE_STATUS") {
    sendResponse({
      ok: true,
      hasCapture: latestCapture !== null,
      url: latestCapture?.url || null,
      capturedAt: latestCapture?.captured_at || null,
      propertyCount: latestCapture?.response?.properties?.length ?? null,
    });
    return;
  }
});