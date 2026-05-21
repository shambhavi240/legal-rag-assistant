import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(pages):

    # CLEAN DOCUMENT TEXT
    for page in pages:

        # REMOVE TIMESTAMPS
        page.page_content = re.sub(
            r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)",
            "",
            page.page_content
        )

        # REMOVE URLS
        page.page_content = re.sub(
            r"https?://\S+",
            "",
            page.page_content
        )

        # REMOVE EXHIBIT HEADER
        page.page_content = page.page_content.replace(
            "EX-10.43",
            ""
        )

        # REMOVE REPEATED FOOTERS
        page.page_content = re.sub(
            r"Canadian Executive Employment Agreement.*",
            "",
            page.page_content
        )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(pages)

    return chunks