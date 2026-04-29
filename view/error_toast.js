// Shared error toast popup. Exposes a single global so every page's inline
// <script> blocks can route alerts and inline error text through the same UI.
(function () {
  const CONTAINER_CLASS = "error-toast-container";
  const TOAST_CLASS = "error-toast";
  const DEFAULT_DURATION_MS = 5000;

  function getOrCreateContainer() {
    let container = document.querySelector("." + CONTAINER_CLASS);
    if (container) return container;

    container = document.createElement("div");
    container.className = CONTAINER_CLASS;

    // Anchor inside .app-shell when available so the popup stays inside the
    // simulated 420px mobile column on desktop. Fall back to body otherwise.
    const host = document.querySelector(".app-shell") || document.body;
    host.appendChild(container);
    return container;
  }

  function showErrorToast(code, message, options) {
    const opts = options || {};
    const durationMs = typeof opts.durationMs === "number" ? opts.durationMs : DEFAULT_DURATION_MS;

    const container = getOrCreateContainer();

    const toast = document.createElement("div");
    toast.className = TOAST_CLASS;
    toast.setAttribute("role", "alert");

    const codeEl = document.createElement("div");
    codeEl.className = "error-toast-code";
    codeEl.textContent = "Error " + (code != null && code !== "" ? String(code) : "UNKNOWN");

    const messageEl = document.createElement("div");
    messageEl.className = "error-toast-message";
    messageEl.textContent = message != null ? String(message) : "";

    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "error-toast-close";
    closeBtn.setAttribute("aria-label", "Dismiss error");
    closeBtn.textContent = "\u00D7"; // ×

    toast.appendChild(codeEl);
    toast.appendChild(messageEl);
    toast.appendChild(closeBtn);
    container.appendChild(toast);

    let timerId = null;
    function dismiss() {
      if (timerId !== null) {
        clearTimeout(timerId);
        timerId = null;
      }
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }

    closeBtn.addEventListener("click", dismiss);
    timerId = setTimeout(dismiss, durationMs);

    return dismiss;
  }

  window.showErrorToast = showErrorToast;
})();
