async function uploadVideo() {
    const fileInput = document.getElementById("videoInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a video first.");
        return;
    }

    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");

    loadingDiv.style.display = "block";
    resultsDiv.innerHTML = "";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();

        if (data.predictions && data.predictions.length > 0) {
            data.predictions.forEach(item => {
                const itemDiv = document.createElement("div");
                itemDiv.className = "result-item";

                const label = document.createElement("div");
                label.className = "label";
                label.textContent = item.label;

                const barContainer = document.createElement("div");
                barContainer.className = "bar-container";

                const bar = document.createElement("div");
                bar.className = "bar";
                bar.style.width = `${item.probability}%`;

                const barText = document.createElement("div");
                barText.className = "bar-text";
                barText.textContent = `${item.probability.toFixed(1)}%`;

                bar.appendChild(barText);
                barContainer.appendChild(bar);

                itemDiv.appendChild(label);
                itemDiv.appendChild(barContainer);
                resultsDiv.appendChild(itemDiv);
            });
        } else {
            resultsDiv.innerHTML = "<p>No predictions returned.</p>";
        }
    } catch (error) {
        console.error("Upload error:", error);
        resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    } finally {
        loadingDiv.style.display = "none";
    }
}

function previewVideo() {
    const fileInput = document.getElementById("videoInput");
    const file = fileInput.files[0];
    const videoPlayer = document.getElementById("videoPreview");

    if (file) {
        const videoURL = URL.createObjectURL(file);
        videoPlayer.src = videoURL;
        videoPlayer.style.display = "block";
    } else {
        videoPlayer.style.display = "none";
    }
}