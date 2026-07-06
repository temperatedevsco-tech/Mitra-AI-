let currentChatId = null;
const messages = document.getElementById("messages");
const input = document.getElementById("message");
const send = document.getElementById("send");


send.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// suggestion chips on the welcome screen
document.querySelectorAll(".suggestion").forEach((btn) => {
  btn.addEventListener("click", () => {
    input.value = btn.textContent;
    input.focus();
  });
});

function addMessage(text, isUser) {
  const bubble = document.createElement("div");

  bubble.className = isUser ? "user" : "assistant";

  bubble.textContent = text;

  messages.appendChild(bubble);

  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
    const text = input.value.trim();

    if (!text) return;

    addMessage(text, true);

    input.value = "";

    // Disable sending
    send.disabled = true;
    input.disabled = true;

    // Loading bubble
    const loading = document.createElement("div");
    loading.className = "assistant thinking";
    loading.id = "thinking";
    loading.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    messages.appendChild(loading);
    messages.scrollTop = messages.scrollHeight;

    try {

        const response = await fetch("/api/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                message: text,
                chat_id: currentChatId,
            }),
        });

        const data = await response.json();

        currentChatId = data.chat_id;

        document.getElementById("thinking").remove();

        addMessage(data.reply, false);

        await loadChats();

    } catch (err) {

        document.getElementById("thinking")?.remove();

        addMessage(
            "Mitra is temporarily unavailable.",
            false
        );

        console.error(err);

    } finally {

        send.disabled = false;
        input.disabled = false;
        input.focus();

    }
}

async function loadChats() {

  const response = await fetch("/api/chats");

  const chats = await response.json();

  const list = document.getElementById("chat-list");

  list.innerHTML = "";

  chats.forEach((chat) => {
    const div = document.createElement("div");

    div.className = "chat-item";

div.innerHTML = `
    <span>${chat.title}</span>

    <button
        class="delete-chat"
        onclick="deleteChat(event, ${chat.id})">
        🗑
    </button>
`;

    div.onclick = () => loadChat(chat.id);

    list.appendChild(div);
  });
}

async function loadChat(chatId) {
  currentChatId = chatId;

  const response = await fetch("/api/chat/" + chatId);

  const messagesData = await response.json();

  messages.innerHTML = "";

  messagesData.forEach((msg) => {
    addMessage(
      msg.content,

      msg.role === "user",
    );
  });
}

async function deleteChat(event, chatId) {

    event.stopPropagation();

    const confirmed = confirm(
        "Delete this chat?"
    );

    if (!confirmed) return;

    await fetch("/api/chat/" + chatId, {

        method: "DELETE"

    });

    if (currentChatId === chatId) {

        currentChatId = null;

        messages.innerHTML = `
            <div class="welcome">
                <h1>Welcome 👋</h1>
                <p>Start a conversation with Mitra.</p>
            </div>
        `;

    }

    loadChats();

}

loadChats();

const sidebar = document.querySelector(".sidebar");

const menuBtn = document.getElementById("menu-btn");

const overlay = document.getElementById("overlay");

if (menuBtn && sidebar && overlay) {

    menuBtn.onclick = () => {

        sidebar.classList.add("open");

        overlay.classList.add("active");

    };

    overlay.onclick = () => {

        sidebar.classList.remove("open");

        overlay.classList.remove("active");

    };

}

const newChatBtn = document.getElementById("new-chat-btn");

if (newChatBtn) {

    newChatBtn.onclick = async () => {

        try {

            const response = await fetch("/api/chat/new", {
                method: "POST"
            });

            const chat = await response.json();

            // Save the newly created chat ID
            currentChatId = chat.id;

            // Clear the chat window
            messages.innerHTML = `
                <div class="welcome">
                    <h1>Welcome 👋</h1>
                    <p>Start a conversation with Mitra.</p>
                </div>
            `;

            // Refresh the sidebar
            await loadChats();

            // Automatically open the new chat
            await loadChat(chat.id);

            // Close sidebar on mobile
            if (sidebar && overlay) {
                sidebar.classList.remove("open");
                overlay.classList.remove("active");
            }

        } catch (err) {

            console.error(err);

            alert("Couldn't create a new chat.");

        }

    };

}

const profileBtn = document.getElementById("profile-btn");

const profileMenu = document.getElementById("profile-menu");

if(profileBtn){

    profileBtn.addEventListener("click",(e)=>{

        e.stopPropagation();

        profileMenu.classList.toggle("show");

    });

    document.addEventListener("click",()=>{

        profileMenu.classList.remove("show");

    });

}