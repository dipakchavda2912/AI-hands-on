from langchain_text_splitters import RecursiveCharacterTextSplitter


class FileUtils:
  @staticmethod
  def make_document_chunks(file_content: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = text_splitter.split_text(file_content)
    return chunks
