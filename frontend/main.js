import { scrollToBottom, createMessageElement, createLoadingMessage, cleanAnswer } from "./utils.js";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const tongueImageInput = document.getElementById("tongue-image");

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const prompt = userInput.value.trim();
    const imageFile = tongueImageInput.files[0];

    if(!prompt && !imageFile) return;

    if(prompt) appendMessage(prompt, "user");
    if(imageFile){
        const imgUrl = URL.createObjectURL(imageFile);
        appendMessage(null, "user", imgUrl);
    }

    userInput.value = "";
    tongueImageInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;

    const loadingMsg = createLoadingMessage();
    chatBox.appendChild(loadingMsg);
    scrollToBottom(chatBox);

    try {
        const formData = new FormData();
        if(prompt) formData.append("user_input", prompt);
        if(imageFile) formData.append("tongue_image", imageFile);

        const response = await fetch(`${CONFIG.API_URL}`, {
            method: "POST",
            body: formData
        });

        if(!response.ok) throw new Error("网络请求失败");

        const data = await response.json();
        const answer = cleanAnswer(data.answer || "[后端未返回回答]");

        loadingMsg.remove();
        appendMessage(answer, "bot");

    } catch(err) {
        loadingMsg.remove();
        appendMessage("[后端请求失败]", "bot");
        console.error(err);
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function appendMessage(text, sender, imageUrl=null) {
    const msg = createMessageElement(text, sender, imageUrl);
    chatBox.appendChild(msg);
    scrollToBottom(chatBox);
}
