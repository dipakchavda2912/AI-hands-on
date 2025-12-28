from utils import FileUtils


class FileService:
  def __init__(self):
    self.file_utils = FileUtils
    self._files = None
    pass

  def make_chunks(self, files):
    # Step 3: Chunk them
    # doc_chunks = self.github_utils.make_document_chunks()
    self._files = files
    doc_chunks = self.file_utils.make_document_chunks(self, self._files)
    print(f"doc_chunks: {doc_chunks}")
    return doc_chunks
