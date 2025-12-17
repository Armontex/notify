from base import Base as _Base
from session import engine as _engine

def create_all() -> None:
    _Base.metadata.create_all(_engine)

__all__ = ("create_all",)