const statusEl = document.getElementById("status");
const downloadBtn = document.getElementById("downloadBtn");

function refreshStatus() {
  chrome.runtime.sendMessage(
    { type: "GET_LATEST_CAPTURE_STATUS" },
    (response) => {
      if (chrome.runtime.lastError) {
        statusEl.textContent = "Extension background not available.";
        return;
      }

      if (!response?.hasCapture) {
        statusEl.textContent = "No JSON captured yet.";
        downloadBtn.disabled = true;
        return;
      }

      statusEl.textContent = `Captured ${
        response.propertyCount ?? "unknown"
      } records.`;

      downloadBtn.disabled = false;
    }
  );
}

downloadBtn.addEventListener("click", () => {
  chrome.runtime.sendMessage(
    { type: "DOWNLOAD_LATEST_CAPTURE" },
    (response) => {
      if (chrome.runtime.lastError || !response?.ok) {
        statusEl.textContent = "Download failed.";
        return;
      }

      statusEl.textContent = "Downloaded latest JSON.";
    }
  );
});

refreshStatus();