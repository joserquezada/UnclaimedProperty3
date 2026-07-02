const script = document.createElement("script");
script.src = chrome.runtime.getURL("injected.js");
script.onload = () => script.remove();

(document.head || document.documentElement).appendChild(script);

window.addEventListener("message", (event) => {
  if (event.source !== window) return;
  if (event.data?.type !== "UNCLAIMED_PROPERTY_CAPTURE") return;

  chrome.runtime.sendMessage(
    {
      type: "SAVE_CAPTURE",
      payload: event.data.payload,
    },
    () => {
      if (chrome.runtime.lastError) {
        console.warn(
          "Collector message failed:",
          chrome.runtime.lastError.message
        );
      }
    }
  );
});