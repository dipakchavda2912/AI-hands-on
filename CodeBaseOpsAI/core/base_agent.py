from abc import abstractmethod, ABC


class BaseAgent(ABC):
    """Contract for all agents: must have a name and a load() method."""

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    # abstract property getter
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the agent"""
        raise NotImplementedError

    # abstract property setter
    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        """Set the name of the agent"""
        raise NotImplementedError

    @abstractmethod
    def load(self) -> None:
        """Perform any agent-specific loading/initialization."""
        raise NotImplementedError
