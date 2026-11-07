(() => {
  "use strict";

  const API_URL = "http://127.0.0.1:8000/generate-hint";
  const MAX_LENGTH = 1000;
  const MIN_LENGTH = 5;
  const REQUEST_TIMEOUT_MS = 180000; // small local models can be slow on CPU

  const $ = (id) => document.getElementById(id);
  const form = $("problemForm");
  const input = $("problemInput");
  const counter = $("charCount");
  const formError = $("formError");
  const generateBtn = $("generateBtn");
  const clearBtn = $("clearBtn");
  const resultSection = $("resultSection");
  const loadingCard = $("loadingCard");
  const hintCard = $("hintCard");
  const hintQuestion = $("hintQuestion");
  const hintText = $("hintText");
  const errorCard = $("errorCard");
  const errorText = $("errorText");

  function updateCounter() {
    counter.textContent = `${input.value.length} / ${MAX_LENGTH}`;
  }

  function showFieldError(message) {
    formError.textContent = message;
    formError.hidden = false;
    input.classList.add("is-invalid");
    input.focus();
  }

  function clearFieldError() {
    formError.hidden = true;
    formError.textContent = "";
    input.classList.remove("is-invalid");
  }

  function setLoading(isLoading) {
    generateBtn.disabled = isLoading;
    clearBtn.disabled = isLoading;
    generateBtn.classList.toggle("is-loading", isLoading);
    generateBtn.querySelector(".btn__label").textContent = isLoading ? "Generating…" : "Generate Hint";
    generateBtn.setAttribute("aria-busy", String(isLoading));
  }

  function showOnly(card) {
    resultSection.hidden = false;
    [loadingCard, hintCard, errorCard].forEach((el) => { el.hidden = el !== card; });
  }

  function renderHint(question, hint) {
    hintQuestion.textContent = question;
    hintText.textContent = "";
    String(hint)
      .split(/\n+/)
      .map((line) => line.trim())
      .filter(Boolean)
      .forEach((line) => {
        const p = document.createElement("p");
        p.textContent = line; // textContent keeps model output safe from HTML injection
        hintText.appendChild(p);
      });
    showOnly(hintCard);
  }

  function renderError(message) {
    errorText.textContent = message;
    showOnly(errorCard);
  }

  async function readErrorDetail(response) {
    try {
      const data = await response.json();
      if (typeof data.detail === "string") return data.detail;
      if (Array.isArray(data.detail) && data.detail[0]?.msg) return data.detail[0].msg;
    } catch (_) { /* response was not JSON */ }
    return "";
  }

  async function requestHint(question) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
        signal: controller.signal,
      });

      if (!response.ok) {
        const detail = await readErrorDetail(response);
        throw new Error(detail || `The server returned an error (HTTP ${response.status}).`);
      }

      const data = await response.json();
      if (!data || typeof data.hint !== "string" || !data.hint.trim()) {
        throw new Error("The server replied, but no hint was included. Please try again.");
      }
      return data;
    } catch (err) {
      if (err.name === "AbortError") {
        throw new Error("The request took too long. Check that the backend is running, then try again.");
      }
      if (err instanceof TypeError) {
        throw new Error("Can't reach the HintWise server at 127.0.0.1:8000. Make sure the backend is running and allows requests from this page.");
      }
      throw err;
    } finally {
      clearTimeout(timer);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    clearFieldError();

    const question = input.value.trim();
    if (!question) {
      showFieldError("Enter a math problem to get a hint.");
      return;
    }
    if (question.length < MIN_LENGTH) {
      showFieldError("Add a little more detail so the tutor can understand the problem.");
      return;
    }

    setLoading(true);
    showOnly(loadingCard);
    resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });

    try {
      const data = await requestHint(question);
      renderHint(data.question || question, data.hint);
    } catch (err) {
      renderError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    input.value = "";
    updateCounter();
    clearFieldError();
    resultSection.hidden = true;
    [loadingCard, hintCard, errorCard].forEach((el) => { el.hidden = true; });
    input.focus();
  }

  input.addEventListener("input", () => {
    updateCounter();
    if (!formError.hidden) clearFieldError();
  });
  input.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") form.requestSubmit();
  });
  form.addEventListener("submit", handleSubmit);
  clearBtn.addEventListener("click", handleClear);

  updateCounter();
})();