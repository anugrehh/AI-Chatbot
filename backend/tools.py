from datetime import datetime

from langchain.tools import tool


def create_tools(retriever):

    @tool
    def document_search(query: str) -> str:
        """
        Search information from the uploaded PDF documents.
        Use this tool when the user asks something that may be
        answered from the uploaded documents.
        """

        if retriever is None:
            return "No PDF documents are currently available."

        docs = retriever.invoke(query)

        if not docs:
            return "No relevant information was found in the documents."

        results = []

        for doc in docs:

            source = doc.metadata.get(
                "source",
                "Unknown document"
            )

            page = doc.metadata.get(
                "page",
                None
            )

            if page is not None:
                page_number = page + 1
                location = f"{source} - Page {page_number}"
            else:
                location = source

            results.append(
                f"[SOURCE: {location}]\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(results)

    @tool
    def system_datetime() -> str:
        """
        Get the current system date and time.
        Use this when the user asks for the current date or time.
        """

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    return [
        document_search,
        system_datetime
    ]
    