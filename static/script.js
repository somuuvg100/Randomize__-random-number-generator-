/**
 * @file Client-side logic for the Random Number Generator.
 * Handles API requests, DOM manipulation, animations, and local storage history.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const minEl = document.getElementById("minimum");
  const maxEl = document.getElementById("maximum");
  const rngForm = document.getElementById("rngForm");
  const swapBtn = document.getElementById("swapBtn");
  const randRangeBtn = document.getElementById("randomRangeBtn");
  const resultValue = document.getElementById("resultValue");
  const copyBtn = document.getElementById("copyBtn");
  const errorEl = document.getElementById("error");
  const historyList = document.getElementById("historyList");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");

  /**
   * Displays an error message on the UI.
   * @param {string} msg - The error message to display.
   */
  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
    errorEl.animate([
      { opacity: 0, transform: "translateY(-10px)" },
      { opacity: 1, transform: "translateY(0)" }
    ], { duration: 250, easing: "ease-out" });
  }

  /**
   * Clears the currently displayed error message.
   */
  function clearError() {
    errorEl.hidden = true;
    errorEl.textContent = "";
  }

  /**
   * Loads the history from localStorage and populates the UI list.
   */
  function loadHistory() {
    try {
      const items = JSON.parse(localStorage.getItem("rngHistory") || "[]");
      historyList.innerHTML = "";
      
      if (items.length === 0) {
        const emptyState = document.createElement("li");
        emptyState.textContent = "No recent generations.";
        emptyState.style.justifyContent = "center";
        emptyState.style.color = "var(--text-muted)";
        historyList.appendChild(emptyState);
        return;
      }

      items.forEach(it => {
        const li = document.createElement("li");
        
        const valSpan = document.createElement("span");
        valSpan.className = "history-val";
        valSpan.textContent = it.value;
        
        const metaSpan = document.createElement("span");
        metaSpan.className = "history-meta";
        metaSpan.textContent = `[${it.range[0]} - ${it.range[1]}] • ${new Date(it.ts).toLocaleTimeString()}`;
        
        li.appendChild(valSpan);
        li.appendChild(metaSpan);
        historyList.appendChild(li);
      });
    } catch (e) {
      historyList.innerHTML = "";
      console.error("Failed to load history", e);
    }
  }

  /**
   * Pushes a new generation record into localStorage and updates the UI.
   * @param {Object} obj - The history object to store.
   * @param {number} obj.value - The generated value.
   * @param {Array<number>} obj.range - The [min, max] range used.
   * @param {string} obj.ts - ISO timestamp.
   */
  function pushHistory(obj) {
    const arr = JSON.parse(localStorage.getItem("rngHistory") || "[]");
    arr.unshift(obj);
    // Keep only the last 20 records
    localStorage.setItem("rngHistory", JSON.stringify(arr.slice(0, 20)));
    loadHistory();
  }

  /**
   * Handles the form submission to generate a random number.
   */
  rngForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearError();
    
    const minimum = minEl.value.trim();
    const maximum = maxEl.value.trim();
    
    if (!minimum || !maximum) {
      showError("Please provide both minimum and maximum values.");
      return;
    }

    try {
      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ minimum, maximum }),
      });
      
      const data = await resp.json();
      
      if (!resp.ok) {
        showError(data.error || "An error occurred.");
        return;
      }
      
      // Update the result UI with an animation
      resultValue.textContent = data.value;
      resultValue.animate([
        { transform: "scale(0.8)", opacity: 0 },
        { transform: "scale(1.1)", opacity: 1, offset: 0.7 },
        { transform: "scale(1)", opacity: 1 }
      ], { duration: 400, easing: "cubic-bezier(0.175, 0.885, 0.32, 1.275)" });
      
      // Save to history
      pushHistory({ value: data.value, range: data.range, ts: data.timestamp });
    } catch (err) {
      showError("Network error. Try again later.");
      console.error("API Fetch Error:", err);
    }
  });

  /**
   * Copies the currently generated result to the clipboard.
   */
  copyBtn.addEventListener("click", () => {
    const txt = resultValue.textContent;
    if (!txt || txt === "—") {
      alert("Generate a value first.");
      return;
    }
    navigator.clipboard?.writeText(txt).then(() => {
      const originalText = copyBtn.textContent;
      copyBtn.textContent = "Copied!";
      copyBtn.style.color = "var(--success)";
      
      setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.color = "";
      }, 1500);
    }).catch(err => {
      console.error("Failed to copy", err);
    });
  });

  /**
   * Swaps the minimum and maximum input values.
   */
  swapBtn.addEventListener("click", () => {
    const temp = minEl.value;
    minEl.value = maxEl.value;
    maxEl.value = temp;
    
    // Add small visual feedback
    [minEl, maxEl].forEach(el => {
      el.animate([
        { transform: "translateY(-2px)" },
        { transform: "translateY(0)" }
      ], { duration: 200 });
    });
  });

  /**
   * Populates the inputs with a random range.
   */
  randRangeBtn.addEventListener("click", () => {
    const a = Math.floor(Math.random() * 2001) - 1000;
    const b = Math.floor(Math.random() * 2001) - 1000;
    minEl.value = Math.min(a, b);
    maxEl.value = Math.max(a, b);
  });

  /**
   * Clears the entire generation history from localStorage and updates UI.
   */
  clearHistoryBtn.addEventListener("click", () => {
    localStorage.removeItem("rngHistory");
    loadHistory();
  });

  // Initial load
  loadHistory();
});