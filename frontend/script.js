async function uploadVideo() {
    const fileInput = document.getElementById("videoInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a video.");
        return;
    }

    const resultsList = document.getElementById("results");
    const loading = document.getElementById("loading");

    loading.style.display = "block";
    resultsList.innerHTML = "";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        data.predictions.forEach(item => {
            const container = document.createElement("div");

            const label = document.createElement("p");
            label.textContent = `${item.label} (${item.probability.toFixed(2)}%)`;

            const bar = document.createElement("div");
            bar.style.width = item.probability + "%";
            bar.style.height = "10px";
            bar.style.background = "#4CAF50";

            container.appendChild(label);
            container.appendChild(bar);

            resultsList.appendChild(container);
        });

    } catch (error) {
        alert("Error uploading video.");
        console.error(error);
    }

    loading.style.display = "none";
}

function previewVideo() {
    const fileInput = document.getElementById("videoInput");
    const file = fileInput.files[0];

    if (file) {
        const videoURL = URL.createObjectURL(file);
        const videoPlayer = document.getElementById("videoPreview");
        videoPlayer.src = videoURL;
        videoPlayer.style.display = "block";
    }
}