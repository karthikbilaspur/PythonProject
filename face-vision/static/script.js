const form = document.querySelector("#compare-form");
const button = document.querySelector("#submit-button");
const resultBox = document.querySelector("#result");

function previewFile(inputId, previewId) {
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  input.addEventListener("change", () => {
    const file = input.files?.[0];
    preview.replaceChildren();
    if (!file) {
      preview.textContent = "Choose a photo";
      return;
    }
    if (!file.type.startsWith("image/")) {
      preview.textContent = "Please select an image file";
      return;
    }
    const image = document.createElement("img");
    image.alt = "Selected image preview";
    image.src = URL.createObjectURL(file);
    preview.appendChild(image);
  });
}
previewFile("file1", "preview1");
previewFile("file2", "preview2");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resultBox.className = "result";
  resultBox.textContent = "Comparing faces…";
  button.disabled = true;

  try {
    const response = await fetch("/face_compare", {
      method: "POST",
      body: new FormData(form),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Comparison failed.");

    resultBox.replaceChildren();
    const heading = document.createElement("h2");
    heading.textContent = data.verified ? "Face match" : "No match detected";
    const details = document.createElement("p");
    details.textContent =
      `Verified: ${data.verified ? "Yes" : "No"} · Distance: ${data.distance.toFixed(4)} · Model threshold: ${data.threshold}`;
    const note = document.createElement("p");
    note.textContent = data.note || "The result is model-dependent and is not proof of identity.";
    resultBox.append(heading, details, note);
  } catch (error) {
    resultBox.className = "result error";
    resultBox.textContent = error.message || "Something went wrong.";
  } finally {
    button.disabled = false;
  }
});
