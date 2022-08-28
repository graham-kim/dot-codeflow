import typing as tp
import pyparsing as pp
import pydot as pd

class NodeParser:
    def __init__(self, dot: pd.Dot):
        self.dot = dot

    def parse_stripped_line(self, line_num: int, stripped_line: str):
        self.line_num = line_num
        if stripped_line.startswith("- "):
            self._parse_method(stripped_line)
        elif stripped_line.startswith("= "):
            self._parse_tags_for_function_or_class(stripped_line)
        elif stripped_line.startswith("@"):
            self._parse_rank_same_cluster(stripped_line)
        else:
            self._finish_class()
            self._start_class(stripped_line)
