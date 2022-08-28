import pyparsing as pp
import pydot as pd

import typing as tp
from enum import Enum
from parsers.interface import ParserInterface

class GeneralParser(ParserInterface):
    class CurrentMode(Enum):
        NOT_PARSING = 0
        PARSE_NODE  = 1
        PARSE_LINK  = 2

    def __init__(self):
        self.mode = self.CurrentMode.NOT_PARSING
        self.dot = pd.Dot()

    def _finish_current_parsing(self):
        if self.mode == self.CurrentMode.PARSE_NODE:
            pass
        elif self.mode == self.CurrentMode.PARSE_LINK:
            pass
        self.mode = self.CurrentMode.NOT_PARSING

    def parse_file(self, filename: str) -> None:
        with open(filename, "r") as inF:
            for i, line in enumerate(inF):
                stripped_line = line.strip('\n').strip()
                if stripped_line.startswith('#'):
                    continue
                elif len(stripped_line) == 0:
                    self._finish_current_parsing()
                elif stripped_line.startswith('>') or stripped_line.startswith('<'):
                    if self.mode == self.CurrentMode.PARSE_NODE:
                        raise Exception(f"Got a link line while parsing a node:\n{i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_LINK

                    raise NotImplementedError("Implement me")
                else:
                    if self.mode == self.CurrentMode.PARSE_LINK:
                        raise Exception(f"Got a node line while parsing a link:\n{i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_NODE

                    raise NotImplementedError("Implement me")

        self._finish_current_parsing()

    def get_pydot_dot(self):
        self.dot