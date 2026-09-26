import os
from glob import glob

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()


def get_retriever():

    pdfs = glob("backend/documents/*.pdf")

    if not pdfs:
        print("No PDF found in backend/documents/")
        return None, 0

    documents = []

    for pdf in pdfs:

        try:
            loader = PyPDFLoader(pdf)
            documents.extend(loader.load())

            print(f"Loaded: {pdf}")

        except Exception as e:

            print(f"Error loading {pdf}: {e}")


    if not documents:

        return None, 0


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )


    chunks = splitter.split_documents(
        documents
    )


    print(
        f"Created {len(chunks)} document chunks."
    )


    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv(
            "GOOGLE_API_KEY"
        )
    )


    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )


    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )


    return retriever, len(pdfs)