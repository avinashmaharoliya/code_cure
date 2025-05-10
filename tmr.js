function uploadImage() {
    let input = document.getElementById("imageInput");

    if (!input.files.length) {
        alert("Please select an image file.");
        return;
    }

    let file = input.files[0];
    let formData = new FormData();
    formData.append("file", file);

    let uplink = "https://cf57-103-148-1-82.ngrok-free.app/tumor";

    document.querySelector(".predict-btn").textContent = "Predicting...";

    fetch(uplink, { method: "POST", body: formData })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to get PDF");
            }
            return response.blob();
        })
        .then(blob => {
            const blobUrl = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = blobUrl;
            a.download = "report.pdf";
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                window.URL.revokeObjectURL(blobUrl);
                a.remove();
            }, 1000); // Give it a second to start downloading
        })
        .catch(err => {
            console.error("Error:", err);
            alert("Something went wrong. Please try again.");
        })
        .finally(() => {
            document.querySelector(".predict-btn").textContent = "Predict";
        });
}
