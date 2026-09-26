import os
import shutil

from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)

from backend.rag import get_retriever
from backend.tools import create_tools


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:

    raise RuntimeError(
        "GOOGLE_API_KEY is missing. "
        "Add it to your .env file."
    )


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="DocuMind AI",
    description="AI Powered PDF Knowledge Assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

DOCUMENT_FOLDER = "backend/documents"
FRONTEND_FOLDER = "frontend"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# ============================================================
# AI MODEL
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)


# ============================================================
# RAG SETUP
# ============================================================

retriever, num_docs = get_retriever()

tools = create_tools(
    retriever
)

llm_with_tools = llm.bind_tools(
    tools
)


# ============================================================
# CHAT HISTORY
# ============================================================

chat_history = []


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str


# ============================================================
# EXTRACT TEXT FROM AI RESPONSE
# ============================================================

def get_text(response):

    content = response.content

    # --------------------------------------------------------
    # Normal string response
    # --------------------------------------------------------

    if isinstance(content, str):

        return content

    # --------------------------------------------------------
    # Gemini content blocks
    # --------------------------------------------------------

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get(
                            "text",
                            ""
                        )
                    )

        return "".join(
            text_parts
        )

    return str(content)


# ============================================================
# EXTRACT DOCUMENT SOURCES
# ============================================================

def extract_sources(text):

    sources = []

    for line in text.splitlines():

        if line.startswith(
            "[SOURCE:"
        ):

            source = (
                line
                .replace(
                    "[SOURCE:",
                    ""
                )
                .replace(
                    "]",
                    ""
                )
                .strip()
            )

            if source not in sources:

                sources.append(
                    source
                )

    return sources


# ============================================================
# ASK AI
# ============================================================

def ask_ai(query):

    global chat_history

    # --------------------------------------------------------
    # Create messages
    # --------------------------------------------------------

    messages = (
        chat_history[-10:]
        +
        [
            HumanMessage(
                content=query
            )
        ]
    )

    # --------------------------------------------------------
    # FIRST AI CALL
    # --------------------------------------------------------

    response = (
        llm_with_tools.invoke(
            messages
        )
    )

    # --------------------------------------------------------
    # CHECK FOR TOOL CALLS
    # --------------------------------------------------------

    if response.tool_calls:

        # Add AI tool-call message
        messages.append(
            response
        )

        # ----------------------------------------------------
        # Execute each tool
        # ----------------------------------------------------

        for tool_call in response.tool_calls:

            tool_name = (
                tool_call["name"]
            )

            tool_args = (
                tool_call.get(
                    "args",
                    {}
                )
            )

            # ------------------------------------------------
            # Find requested tool
            # ------------------------------------------------

            selected_tool = None

            for tool in tools:

                if (
                    tool.name
                    ==
                    tool_name
                ):

                    selected_tool = tool

                    break

            # ------------------------------------------------
            # Execute tool
            # ------------------------------------------------

            if selected_tool:

                try:

                    result = (
                        selected_tool.invoke(
                            tool_args
                        )
                    )

                except Exception as e:

                    result = (
                        f"Tool error: {str(e)}"
                    )

            else:

                result = (
                    "Unknown tool."
                )

            # ------------------------------------------------
            # Add tool result
            # ------------------------------------------------

            messages.append(
                ToolMessage(
                    content=str(
                        result
                    ),
                    tool_call_id=(
                        tool_call["id"]
                    )
                )
            )

        # ----------------------------------------------------
        # SECOND AI CALL
        # ----------------------------------------------------

        response = (
            llm_with_tools.invoke(
                messages
            )
        )

    # --------------------------------------------------------
    # Extract final answer
    # --------------------------------------------------------

    answer = get_text(
        response
    )

    # --------------------------------------------------------
    # Save conversation
    # --------------------------------------------------------

    chat_history.append(
        HumanMessage(
            content=query
        )
    )

    chat_history.append(
        AIMessage(
            content=answer
        )
    )

    return answer


# ============================================================
# API STATUS
# ============================================================

@app.get("/api/status")
def status():

    return {
        "status": "online",
        "documents": num_docs,
        "message": "DocuMind AI is running"
    }


# ============================================================
# CHAT API
# ============================================================

@app.post("/api/chat")
def chat(
    request: ChatRequest
):

    message = (
        request.message.strip()
    )

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:

        answer = ask_ai(
            message
        )

        return {
            "success": True,
            "answer": answer,
            "sources": extract_sources(
                answer
            )
        }

    except Exception as e:

        print(
            "AI ERROR:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CLEAR CHAT
# ============================================================

@app.post("/api/clear-chat")
def clear_chat():

    global chat_history

    chat_history = []

    return {
        "success": True,
        "message": "Chat history cleared."
    }


# ============================================================
# GET DOCUMENTS
# ============================================================

@app.get("/api/documents")
def documents():

    files = []

    if os.path.exists(
        DOCUMENT_FOLDER
    ):

        for filename in os.listdir(
            DOCUMENT_FOLDER
        ):

            if filename.lower().endswith(
                ".pdf"
            ):

                files.append(
                    filename
                )

    return {
        "documents": files,
        "count": len(files)
    }


# ============================================================
# UPLOAD PDF
# ============================================================

@app.post("/api/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    global retriever
    global tools
    global llm_with_tools
    global num_docs

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    # --------------------------------------------------------
    # Validate PDF
    # --------------------------------------------------------

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # --------------------------------------------------------
    # Create safe file path
    # --------------------------------------------------------

    safe_filename = os.path.basename(
        file.filename
    )

    file_path = os.path.join(
        DOCUMENT_FOLDER,
        safe_filename
    )

    try:

        # ----------------------------------------------------
        # Save PDF
        # ----------------------------------------------------

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(
            f"Uploaded: {safe_filename}"
        )

        # ----------------------------------------------------
        # Rebuild RAG
        # ----------------------------------------------------

        retriever, num_docs = (
            get_retriever()
        )

        tools = create_tools(
            retriever
        )

        llm_with_tools = (
            llm.bind_tools(
                tools
            )
        )

        return {
            "success": True,
            "filename": safe_filename,
            "documents": num_docs,
            "message": (
                "PDF uploaded successfully."
            )
        }

    except Exception as e:

        print(
            "UPLOAD ERROR:",
            e
        )

        # ----------------------------------------------------
        # Remove failed upload
        # ----------------------------------------------------

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# DELETE PDF
# ============================================================

@app.delete(
    "/api/documents/{filename}"
)
def delete_document(
    filename: str
):

    global retriever
    global tools
    global llm_with_tools
    global num_docs

    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    if not filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid file."
        )

    # --------------------------------------------------------
    # Prevent path traversal
    # --------------------------------------------------------

    safe_filename = os.path.basename(
        filename
    )

    file_path = os.path.join(
        DOCUMENT_FOLDER,
        safe_filename
    )

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not os.path.exists(
        file_path
    ):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:

        # ----------------------------------------------------
        # Delete PDF
        # ----------------------------------------------------

        os.remove(
            file_path
        )

        print(
            f"Deleted: {safe_filename}"
        )

        # ----------------------------------------------------
        # Rebuild RAG
        # ----------------------------------------------------

        retriever, num_docs = (
            get_retriever()
        )

        tools = create_tools(
            retriever
        )

        llm_with_tools = (
            llm.bind_tools(
                tools
            )
        )

        return {
            "success": True,
            "message": (
                "Document deleted successfully."
            ),
            "documents": num_docs
        }

    except Exception as e:

        print(
            "DELETE ERROR:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# SERVE FRONTEND
# ============================================================

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

app.mount(
    "/css",
    StaticFiles(
        directory="frontend/css"
    ),
    name="css"
)


# ------------------------------------------------------------
# JAVASCRIPT
# ------------------------------------------------------------

app.mount(
    "/js",
    StaticFiles(
        directory="frontend/js"
    ),
    name="js"
)


# ------------------------------------------------------------
# FRONTEND WEBSITE
# ------------------------------------------------------------

app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_FOLDER,
        html=True
    ),
    name="frontend"
)