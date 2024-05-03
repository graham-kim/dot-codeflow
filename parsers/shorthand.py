import pyparsing as pp

import typing as tp
import parsers.lib_short.patterns as ppp
from parsers.lib_short.node import Node

class ShorthandParser():
    def __init__(self):
        self.pp_pattern = ppp.shorthand_pattern()
        self.node_dict: tp.Dict[str, Node] = {}
        self.link_lines: tp.List[str] = []

    def _finish_current_parsing(self):
        self.link_lines.append("")

    def _parse_line(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_pattern.parseString(stripped_line)

        operator = ''.join(tok['operator'].asList())
        self.link_lines.append( \
            f"{operator} {tok['name']}")

        if tok['name'] not in self.node_dict:
            label = None
            if 'label' in tok:
                label = tok['label']
            self.node_dict[tok['name']] = Node(tok['name'], tok['category'], label)

    def parse_file(self, filename: str) -> None:
        with open(filename, "r") as inF:
            for i, line in enumerate(inF):
                stripped_line = line.strip('\n').strip()
                if stripped_line.startswith('#'):
                    continue
                elif len(stripped_line) == 0:
                    self._finish_current_parsing()
                elif stripped_line.startswith('> ') or stripped_line.startswith('< ') \
                  or stripped_line.startswith('<>'):
                    self._parse_line(i, stripped_line)

        self._finish_current_parsing()

    def print_lines(self, cat_dict: tp.Dict[str, str]):
        for node in self.node_dict.values():
            node_line = f"- {node.name}"
            if node.label:
                node_label = " ".join(node.label.asList())
                node_line += f" | {node_label}"
            print(node_line+"")
            if node.category in cat_dict:
                print(f"= {cat_dict[node.category]}")
            print("")

        for line in self.link_lines:
            print(line)

