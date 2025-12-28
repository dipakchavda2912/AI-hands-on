from utils import GithubUtils


class GithubService:
  def __init__(self):
    self.github_utils = GithubUtils()

  def forRepo(self, repository: str):
    # Step 1: Load repo files
    self.github_utils.read_repo(repository)

    # Step 2: Ingest the files
    self.github_utils.ingest()

  def get_file_chunks(self):
    return self.github_utils.chunks
