
function scrollToBottom(chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function createMessageElement(text, sender, imageUrl = null) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (imageUrl) {
        const img = document.createElement("img");
        img.src = imageUrl;
        img.className = "message-img";
        bubble.appendChild(img);
    }

    if (text) {
        const div = document.createElement("div");
        div.className = "message-text";
        div.innerHTML = text.replace(/\n/g, "<br>");
        bubble.appendChild(div);
    }

    msgDiv.appendChild(bubble);
    return msgDiv;
}

function createLoadingMessage() {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message bot";
    const bubble = document.createElement("div");
    bubble.className = "bubble loading";
    bubble.innerHTML = `<span class="dot">·</span><span class="dot">·</span><span class="dot">·</span>`;
    msgDiv.appendChild(bubble);
    return msgDiv;
}

function cleanAnswer(text) {
    return text
        .replace(/#{1,6}\s*/g,"")
        .replace(/\*\*(.*?)\*\*/g,"$1")
        .replace(/\*(.*?)\*/g,"$1")
        .replace(/`{1,3}(.*?)`{1,3}/g,"$1")
        .replace(/!\[.*?\]\(.*?\)/g,"")
        .replace(/\[.*?\]\(.*?\)/g,"$1")
        .replace(/> /g,"")
        .replace(/---/g,"\n") 
        .trim();
}

export { scrollToBottom, createMessageElement, createLoadingMessage, cleanAnswer };
