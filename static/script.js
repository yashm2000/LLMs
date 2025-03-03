async function sendMessage() {
    const input = document.getElementById("userInput").value;
    const responseDiv = document.getElementById("response");

    if (!input) {
        responseDiv.innerHTML = "Please enter a message.";
        return;
    }

    responseDiv.innerHTML = "Waiting for responses...<br>";

    const response = await fetch("/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
    });

    if (!response.ok) {
        responseDiv.innerHTML += "<p style='color:red;'>Error fetching responses.</p>";
        return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.trim().split("\n");

        lines.forEach(line => {
            if (line.startsWith("data:")) {
                try {
                    const data = JSON.parse(line.substring(5)); // Parse JSON safely

                    let modelDiv = document.getElementById(data.model);
                    if (!modelDiv) {
                        modelDiv = document.createElement("div");
                        modelDiv.id = data.model;
                        modelDiv.innerHTML = `<h3>${data.model}</h3><p id="${data.model}-response"></p>`;
                        responseDiv.appendChild(modelDiv);
                    }

                    // Append new responses dynamically
                    document.getElementById(`${data.model}-response`).innerHTML += data.response;
                } catch (error) {
                    console.error("JSON Decode Error:", error);
                    responseDiv.innerHTML += "<p style='color:red;'>Error processing response.</p>";
                }
            }
        });
    }
}
