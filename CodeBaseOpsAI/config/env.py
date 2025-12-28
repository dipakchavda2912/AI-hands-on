import logging

logger = logging.getLogger(__name__)


class Env:
  @staticmethod
  def load_env():
    try:
      from dotenv import load_dotenv
      logger.info(".env loaded")
      load_dotenv()
    except Exception as e:
      # Avoid breaking imports if dotenv isn't installed or no .env present.
      logger.warning(f"Could not load .env file: {e}")
      pass
