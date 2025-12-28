# file: retrieval.py
from langchain_chroma import Chroma


class RetrieverUtils:
  def make_retriever(vectorstore: Chroma, k: int = 4):
    # MMR or similarity; start with simple similarity
    return vectorstore.as_retriever(search_kwargs={"k": k})
