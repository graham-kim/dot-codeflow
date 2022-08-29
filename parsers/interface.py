from __future__ import annotations

import typing as tp
from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    def get_pydot_dot(self):
        raise NotImplementedError("Implement me")

    @abstractmethod
    def parse_file(self, filename: str):
        raise NotImplementedError("Implement me")
