// web/app.js

const btn = document.getElementById("send");

btn.onclick = async () => {
  const prompt = document.getElementById("prompt").value;
  const resEl = document.getElementById("result");

  resEl.textContent = "Loading...";

  try {
    const resp = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const data = await resp.json();

    if (data.error) {
      resEl.textContent = "Error: " + data.error;
    } else {
      resEl.textContent = data.xml;
    }
  } catch (e) {
    resEl.textContent = "Fetch error: " + e.message;
  }
};
