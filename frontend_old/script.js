async function sendMessage() {
    const input = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");

    const userText = input.value.trim();
    if (!userText) return;

    // show user message
    chatbox.innerHTML += `<div class="user bubble">${userText}</div>`;

    input.value = "";

    // typing indicator
    chatbox.innerHTML += `<div class="bot bubble" id="typing">Typing...</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;

    // API call
    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: userText })
    });

    const data = await response.json();

    // remove typing
    document.getElementById("typing").remove();

    // show bot response
    chatbox.innerHTML += `<div class="bot bubble">${data.answer}</div>`;

    chatbox.scrollTop = chatbox.scrollHeight;
}