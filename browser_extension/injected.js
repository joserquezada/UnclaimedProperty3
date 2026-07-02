(function () {
  const TARGET_PATTERNS = [
    "/SWS/properties",
    "/properties",
    "/search",
    "/claims"
    ];

    function shouldCapture(url) {
    return TARGET_PATTERNS.some((pattern) => url.includes(pattern));
    }

  const originalFetch = window.fetch;

  window.fetch = async function (...args) {
    const response = await originalFetch.apply(this, args);

    try {
      const requestInfo = args[0];
      const requestInit = args[1] || {};

      const url =
        typeof requestInfo === "string"
          ? requestInfo
          : requestInfo?.url || "";
      console.log("Fetch detected:", url);

      const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;

        XMLHttpRequest.prototype.open = function (method, url, ...rest) {
        this._upcMethod = method;
        this._upcUrl = url;
        return originalOpen.call(this, method, url, ...rest);
        };

        XMLHttpRequest.prototype.send = function (body) {
        const xhr = this;

        xhr.addEventListener("load", function () {
            try {
            const url = xhr._upcUrl || "";

            console.log("XHR detected:", url);

            if (!shouldCapture(url)) {
                return;
            }

            let responseJson;

            try {
                responseJson = JSON.parse(xhr.responseText);
            } catch {
                return;
            }

            let requestBody = null;

            if (body) {
                try {
                requestBody = JSON.parse(body);
                } catch {
                requestBody = body;
                }
            }

            console.log("Captured XHR JSON:", url);

            window.postMessage(
                {
                type: "UNCLAIMED_PROPERTY_CAPTURE",
                payload: {
                    captured_at: new Date().toISOString(),
                    url,
                    method: xhr._upcMethod || "UNKNOWN",
                    request: requestBody,
                    response: responseJson,
                },
                },
                "*"
            );
            } catch (error) {
            console.warn("XHR capture failed:", error);
            }
        });

        return originalSend.call(this, body);
        };
      if (!shouldCapture(url)) {
            return response;
        }

      const responseClone = response.clone();
      const responseText = await responseClone.text();

      let responseJson;
      try {
        responseJson = JSON.parse(responseText);
      } catch {
        return response;
      }

      let requestBody = null;

      if (requestInit.body) {
        try {
          requestBody = JSON.parse(requestInit.body);
        } catch {
          requestBody = requestInit.body;
        }
      }
      console.log("Captured unclaimed property JSON:", url);
      window.postMessage(
        {
          type: "UNCLAIMED_PROPERTY_CAPTURE",
          payload: {
            captured_at: new Date().toISOString(),
            url,
            method: requestInit.method || "GET",
            request: requestBody,
            response: responseJson,
          },
        },
        "*"
      );
    } catch (error) {
      console.warn("Unclaimed Property Collector failed:", error);
    }

    return response;
  };

  console.log("Unclaimed Property fetch collector installed.");
})();