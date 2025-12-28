# file: indexing.py
from typing import List, Dict

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def sanitize_metadata(md: dict) -> dict:
  clean = {}
  for k, v in md.items():
    if isinstance(v, (str, int, float, bool)) or v is None:
      clean[k] = v
    else:
      # Flatten/convert any complex types (list/dict/etc.) to strings
      clean[k] = str(v)
  return clean


class FileIndexingUtils:

  def build_vectorstore(docs: List[Dict], persist_dir: str = "./chroma_db"):
    # Initialize Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
      model="gemini-2.5-flash",  # current embedding model
      # Note: some client versions use "models/gemini-embedding-001"; both are supported in latest docs
      # Optional: task_type="RETRIEVAL_DOCUMENT",
      # Optional: output_dimensionality=768,
    )
    # Initialize Chroma vector store (persist to disk)
    vs = Chroma(
      collection_name="repo_index",
      embedding_function=embeddings,
      persist_directory=persist_dir,
    )

    # Convert docs to LangChain Document objects
    from langchain_core.documents import Document

    # lc_docs = [
    #     Document(page_content=d["text"], metadata=d["metadata"]) for d in docs
    # ]
    #

    lc_docs = [
      Document(page_content=d["text"], metadata=sanitize_metadata(d["metadata"]))
      for d in docs
    ]

    # Upsert into Chroma (ids are auto if not provided; we’ll supply for reproducibility)
    vs.add_documents(documents=lc_docs, ids=[d["id"] for d in docs])
    return vs
