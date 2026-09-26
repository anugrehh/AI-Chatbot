// ============================================================
// DOM ELEMENTS
// ============================================================

const chatArea = document.getElementById("chatArea");

const welcome = document.getElementById("welcome");

const messageInput =
    document.getElementById("messageInput");

const sendBtn =
    document.getElementById("sendBtn");

const newChatBtn =
    document.getElementById("newChatBtn");

const clearChatBtn =
    document.getElementById("clearChatBtn");

const fileInput =
    document.getElementById("fileInput");

const modalFileInput =
    document.getElementById("modalFileInput");

const documentsNav =
    document.getElementById("documentsNav");

const documentModal =
    document.getElementById("documentModal");

const closeModal =
    document.getElementById("closeModal");

const documentList =
    document.getElementById("documentList");

const documentStatus =
    document.getElementById("documentStatus");

const themeBtn =
    document.getElementById("themeBtn");

const recentChats =
    document.getElementById("recentChats");

const uploadPreview =
    document.getElementById("uploadPreview");


// ============================================================
// STATE
// ============================================================

let isLoading = false;

let recentMessages = [];


// ============================================================
// INITIALIZE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        checkStatus();

        loadDocuments();

        loadTheme();

    }
);


// ============================================================
// STATUS
// ============================================================

async function checkStatus() {

    try {

        const response =
            await fetch("/api/status");

        const data =
            await response.json();


        documentStatus.textContent =
            `${data.documents} document${data.documents === 1 ? "" : "s"} loaded`;

    }

    catch (error) {

        documentStatus.textContent =
            "System unavailable";

    }

}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message || isLoading) {

        return;

    }


    hideWelcome();


    addMessage(
        message,
        "user"
    );


    messageInput.value = "";

    autoResize();


    isLoading = true;

    sendBtn.disabled = true;


    const typing =
        addTyping();


    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        typing.remove();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );

        }


        addMessage(
            data.answer,
            "ai",
            data.sources
        );


        addRecentChat(message);


    }

    catch (error) {

        typing.remove();


        addMessage(
            "⚠️ " + error.message,
            "ai"
        );

    }


    finally {

        isLoading = false;

        sendBtn.disabled = false;

        messageInput.focus();

    }

}


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(
    text,
    type,
    sources = []
) {

    const row =
        document.createElement("div");


    row.className =
        `message-row ${type}`;


    const message =
        document.createElement("div");


    message.className =
        `message ${type}`;


    message.textContent = text;


    row.appendChild(message);


    // --------------------------------------------------------
    // SOURCES
    // --------------------------------------------------------

    if (
        type === "ai" &&
        sources &&
        sources.length
    ) {

        const sourceContainer =
            document.createElement("div");


        sourceContainer.className =
            "sources";


        sources.forEach(source => {

            const sourceElement =
                document.createElement("div");


            sourceElement.className =
                "source";


            sourceElement.textContent =
                "📄 " + source;


            sourceContainer.appendChild(
                sourceElement
            );

        });


        message.appendChild(
            sourceContainer
        );

    }


    chatArea.appendChild(row);


    scrollToBottom();


    return row;

}


// ============================================================
// TYPING INDICATOR
// ============================================================

function addTyping() {

    const row =
        document.createElement("div");


    row.className =
        "message-row ai";


    const message =
        document.createElement("div");


    message.className =
        "message ai";


    message.innerHTML = `

        <div class="typing">

            <span></span>
            <span></span>
            <span></span>

        </div>

    `;


    row.appendChild(message);

    chatArea.appendChild(row);

    scrollToBottom();


    return row;

}


// ============================================================
// HIDE WELCOME
// ============================================================

function hideWelcome() {

    if (welcome) {

        welcome.style.display =
            "none";

    }

}


// ============================================================
// SCROLL
// ============================================================

function scrollToBottom() {

    chatArea.scrollTo({
        top: chatArea.scrollHeight,
        behavior: "smooth"
    });

}


// ============================================================
// ENTER TO SEND
// ============================================================

messageInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


// ============================================================
// BUTTON
// ============================================================

sendBtn.addEventListener(
    "click",
    sendMessage
);


// ============================================================
// AUTO RESIZE
// ============================================================

messageInput.addEventListener(
    "input",
    autoResize
);


function autoResize() {

    messageInput.style.height =
        "auto";


    messageInput.style.height =
        Math.min(
            messageInput.scrollHeight,
            150
        ) + "px";

}


// ============================================================
// SUGGESTIONS
// ============================================================

document
    .querySelectorAll(".suggestion")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                messageInput.value =
                    button.dataset.question;

                autoResize();

                sendMessage();

            }
        );

    });


// ============================================================
// NEW CHAT
// ============================================================

newChatBtn.addEventListener(
    "click",
    async () => {

        await clearServerChat();

        chatArea.innerHTML = "";

        chatArea.appendChild(
            welcome
        );

        welcome.style.display =
            "block";

        recentMessages = [];

        recentChats.innerHTML = `

            <div class="recent-empty">

                No recent chats

            </div>

        `;

    }
);


// ============================================================
// CLEAR CHAT
// ============================================================

clearChatBtn.addEventListener(
    "click",
    async () => {

        await clearServerChat();

        chatArea.innerHTML = "";

        chatArea.appendChild(
            welcome
        );

        welcome.style.display =
            "block";

    }
);


async function clearServerChat() {

    try {

        await fetch(
            "/api/clear-chat",
            {
                method: "POST"
            }
        );

    }

    catch (error) {

        console.error(error);

    }

}


// ============================================================
// RECENT CHAT
// ============================================================

function addRecentChat(message) {

    recentMessages.unshift(
        message
    );


    recentMessages =
        recentMessages.slice(0, 5);


    renderRecentChats();

}


function renderRecentChats() {

    recentChats.innerHTML = "";


    recentMessages.forEach(
        message => {

            const item =
                document.createElement("div");


            item.className =
                "recent-empty";


            item.textContent =
                "💬 " +
                message.substring(
                    0,
                    30
                );


            recentChats.appendChild(
                item
            );

        }
    );

}


// ============================================================
// DOCUMENT MODAL
// ============================================================

documentsNav.addEventListener(
    "click",
    () => {

        documentModal.classList.add(
            "show"
        );

        loadDocuments();

    }
);


closeModal.addEventListener(
    "click",
    () => {

        documentModal.classList.remove(
            "show"
        );

    }
);


documentModal.addEventListener(
    "click",
    event => {

        if (
            event.target ===
            documentModal
        ) {

            documentModal.classList.remove(
                "show"
            );

        }

    }
);


// ============================================================
// LOAD DOCUMENTS
// ============================================================

async function loadDocuments() {

    try {

        const response =
            await fetch(
                "/api/documents"
            );


        const data =
            await response.json();


        documentList.innerHTML = "";


        if (
            !data.documents.length
        ) {

            documentList.innerHTML = `

                <div class="recent-empty">

                    No PDF documents uploaded yet.

                </div>

            `;

            documentStatus.textContent =
                "No documents loaded";

            return;

        }


        documentStatus.textContent =
            `${data.count} document${data.count === 1 ? "" : "s"} loaded`;


        data.documents.forEach(
            filename => {

                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "document-item";


                item.innerHTML = `

                    <div class="document-info">

                        <span>📄</span>

                        <span class="document-name">
                            ${escapeHtml(filename)}
                        </span>

                    </div>

                    <button
                        class="delete-document"
                        data-filename="${escapeHtml(filename)}"
                    >
                        🗑
                    </button>

                `;


                const deleteBtn =
                    item.querySelector(
                        ".delete-document"
                    );


                deleteBtn.addEventListener(
                    "click",
                    () => deleteDocument(
                        filename
                    )
                );


                documentList.appendChild(
                    item
                );

            }
        );

    }

    catch (error) {

        documentList.innerHTML =
            "Unable to load documents.";

    }

}


// ============================================================
// UPLOAD
// ============================================================

fileInput.addEventListener(
    "change",
    event => {

        uploadFile(
            event.target.files[0]
        );

    }
);


modalFileInput.addEventListener(
    "change",
    event => {

        uploadFile(
            event.target.files[0]
        );

    }
);


async function uploadFile(file) {

    if (!file) {

        return;

    }


    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        alert(
            "Please select a PDF file."
        );

        return;

    }


    uploadPreview.innerHTML = `

        <div class="upload-card">

            ⏳ Uploading

            <strong>
                ${escapeHtml(file.name)}
            </strong>

        </div>

    `;


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                "/api/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Upload failed."
            );

        }


        uploadPreview.innerHTML = `

            <div class="upload-card">

                ✅

                <strong>
                    ${escapeHtml(file.name)}
                </strong>

                uploaded

            </div>

        `;


        await loadDocuments();

        await checkStatus();


        setTimeout(
            () => {

                uploadPreview.innerHTML =
                    "";

            },
            3000
        );


    }

    catch (error) {

        uploadPreview.innerHTML = `

            <div class="upload-card">

                ❌ ${escapeHtml(
                    error.message
                )}

            </div>

        `;

    }

}


// ============================================================
// DELETE DOCUMENT
// ============================================================

async function deleteDocument(
    filename
) {

    const confirmed =
        confirm(
            `Delete "${filename}"?`
        );


    if (!confirmed) {

        return;

    }


    try {

        const response =
            await fetch(
                `/api/documents/${encodeURIComponent(filename)}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Delete failed."
            );

        }


        await loadDocuments();

        await checkStatus();

    }

    catch (error) {

        alert(
            error.message
        );

    }

}


// ============================================================
// THEME
// ============================================================

themeBtn.addEventListener(
    "click",
    () => {

        document.body.classList.toggle(
            "light"
        );


        localStorage.setItem(
            "theme",
            document.body.classList.contains(
                "light"
            )
                ? "light"
                : "dark"
        );

    }
);


function loadTheme() {

    const theme =
        localStorage.getItem(
            "theme"
        );


    if (theme === "light") {

        document.body.classList.add(
            "light"
        );

    }

}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}