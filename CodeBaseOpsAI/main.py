import logging
from typing import Optional

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from config import Env, CONSTANTS, setup_logging
from services import GithubService

logger = logging.getLogger(__name__)

setup_logging()

Env.load_env()


class Main:
    chain: Optional[RetrievalQA] = None

    def init(self) -> None:
        """Initializes the RetrievalQA chain with documents from GithubService."""
        # Step 1: Initialize GithubService and fetch repo chunks
        g_services = GithubService()
        g_services.forRepo(CONSTANTS["GITHUB"]["REPO"])

        file_chunks = g_services.get_file_chunks()
        logger.info(f"Total document chunks fetched: {len(file_chunks)}")

        # Convert to Document objects
        file_chunks = [Document(page_content=chunk) for chunk in file_chunks]

        # Step 2: Initialize embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        logger.debug("Embeddings initialized")

        # Step 3: Create vector store from documents
        vector_store = Chroma.from_documents(file_chunks, embeddings)
        # Persist the vector store to disk
        vector_store.persist()

        # Step 4: Set up RetrievalQA chain
        retriever = vector_store.as_retriever()

        # Initialize the language model
        model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

        # Create the RetrievalQA chain
        self.chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever)

    def ask(self, query: str) -> str:
        """Queries the RetrievalQA chain and returns the result."""
        if not self.chain:
            logger.error("Chain not initialized.")
            return "Chain not initialized."
        response = self.chain.invoke(query)
        return response.get("result", "No result returned.")
