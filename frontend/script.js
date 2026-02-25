async function uploadVideo() {
    const fileInput = document.getElementById("videoInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a video.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    const resultsList = document.getElementById("results");
    resultsList.innerHTML = "";

    data.predictions.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.label} (${item.probability.toFixed(2)}%)`;
        resultsList.appendChild(li);
    });
}