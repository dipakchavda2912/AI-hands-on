# from typing import TypedDict, List
#
#
# # 1) Define the JSON schema your agent should return
# class QAResponse(TypedDict, total=False):
#     answer: str
#     sources: List[dict]  # each: {path: str, sha: str, chunk_index: int, snippet: str}
#
#
# class AgentService:
#     def __init__(self):
#         pass
#
#     # def build_agent(self):
#     #     llm = ChatGoogleGenerativeAI(
#     #         model="gemini-2.5-flash"
#     #     )  # fast; use pro for deeper reasoning
#     #     # Ask Gemini to return a dictionary conforming to QAResponse
#     #     structured_llm = llm.with_structured_output(
#     #         schema={
#     #             "type": "object",
#     #             "properties": {
#     #                 "answer": {"type": "string"},
#     #                 "sources": {
#     #                     "type": "array",
#     #                     "items": {
#     #                         "type": "object",
#     #                         "properties": {
#     #                             "path": {"type": "string"},
#     #                             "sha": {"type": "string"},
#     #                             "chunk_index": {"type": "integer"},
#     #                             "snippet": {"type": "string"},
#     #                         },
#     #                         "required": ["path", "sha", "chunk_index", "snippet"],
#     #                     },
#     #                 },
#     #             },
#     #             "required": ["answer", "sources"],
#     #         },
#     #         method="json_schema",
#     #     )
#     #     return structured_llm
#     #
#     # def init(self, doc_chunks, question: str):
#     #     # 4) Build index (Chroma + Gemini embeddings)
#     #     vs = FileIndexingUtils.build_vectorstore(doc_chunks)
#     #     retriever = RetrieverUtils.make_retriever(vs, k=4)
#     #
#     #     # 4) Retrieve relevant chunks
#     #     retrieved = retriever.invoke(question)
#     #
#     #     # 5) Build prompt with context
#     #     prompt = [
#     #         ("system", CONSTANTS["SYSTEM_INSTRUCTIONS"]),
#     #         (
#     #             "human",
#     #             f"Question: {question}\n\nContext:\n{self.forRepo(retrieved)}\n\nReturn JSON.",
#     #         ),
#     #     ]
#     #
#     #     # 6) Ask Gemini for structured JSON
#     #     llm = self.build_agent()
#     #     result: Dict[str, Any] = llm.invoke(prompt)
#     #
#     #     # 7) Attach sources with snippets
#     #     sources = []
#     #     for d in retrieved:
#     #         m = d.metadata
#     #         sources.append(
#     #             {
#     #                 "path": m["path"],
#     #                 "sha": m["sha"],
#     #                 "chunk_index": m["chunk_index"],
#     #                 "snippet": d.page_content[:300],
#     #             }
#     #         )
#     #     # Make sure sources exist in the JSON (some models may not echo them back reliably)
#     #     result["sources"] = sources
#     #     return result
