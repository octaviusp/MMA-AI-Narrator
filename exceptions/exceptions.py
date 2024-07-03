class NetworkCallException(Exception):
    def __init__(self, message: str = "Network error") -> None:
        super().__init__(message)