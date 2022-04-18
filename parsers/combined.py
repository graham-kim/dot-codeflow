import typing as tp
from enum import Enum
from entities.dotClass import DotClass
from entities.dotFunction import DotFunction
from entities.dotLink import DotLink
from parsers.node import NodeParser
from parsers.multi_links import MultiLinkParser

class CombinedParser:
    class CurrentMode(Enum):
        NOT_PARSING = 0
        PARSE_NODE  = 1
        PARSE_LINK  = 2

    def __init__(self):
        self.mode = self.CurrentMode.NOT_PARSING
        self.node_parser = NodeParser()
        self.link_parser = MultiLinkParser()

    @property
    def nodes(self) -> tp.List[tp.Union[DotClass, DotFunction]]:
        return self.node_parser.nodes

    @property
    def links(self) -> tp.List[DotLink]:
        return self.link_parser.finished_links

    def _finish_current_parsing(self):
        if self.mode == self.CurrentMode.PARSE_NODE:
            self.node_parser._finish_class()
        elif self.mode == self.CurrentMode.PARSE_LINK:
            self.link_parser._finish_current_links()
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
                    self.link_parser.parse_stripped_line(i, stripped_line)
                else:
                    if self.mode == self.CurrentMode.PARSE_LINK:
                        raise Exception(f"Got a node line while parsing a link:\n{i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_NODE
                    self.node_parser.parse_stripped_line(stripped_line)
        self._finish_current_parsing()