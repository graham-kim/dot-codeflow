import typing as tp
import pyparsing as pp
import pydot as pd
from dataclasses import dataclass

class LinkParser:
    @dataclass
    class DstWithMetadata:
        dst: str
        tags: str
        label: str

    def __init__(self, dot: pd.Dot):
        self.dot = dot
        self.current_srcs: tp.List[str] = []
        self.current_dsts_data: tp.List[DstWithMetadata] = []

    def parse_stripped_line(self, line_num: int, stripped_line: str):
        if stripped_line.startswith('#'):
            return
        elif len(stripped_line) == 0:
            self._finish_current_links()
        elif stripped_line.startswith("< "):
            self._add_src(line_num, stripped_line[2:])
        elif stripped_line.startswith("> "):
            self._add_dst(line_num, stripped_line[2:])
        elif stripped_line.startswith("<> "):
            self._add_dst(line_num, stripped_line[3:])
            self._finish_current_links()
            self._add_src(line_num, stripped_line[3:].split('|')[0].strip())
        else:
            raise Exception(f"Unexpected line to parse as link:\n{line_num}: {stripped_line}")
