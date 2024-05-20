import pyparsing as pp

import typing as tp
import parsers.lib_grid.patterns as ppp
from parsers.lib_grid.node import Node, Coords

class GridParser():
    def __init__(self):
        self.pp_pattern = ppp.grid_pattern()
        self.node_dict: tp.Dict[int, Node] = {}
        self.link_lines: tp.List[str] = []
        self.max_x = 0
        self.max_y = 0

    def _finish_current_parsing(self):
        self.link_lines.append("")

    def _parse_line(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_pattern.parseString(stripped_line)

        operator = ''.join(tok['operator'].asList())
        self.link_lines.append( \
            f"{operator} {tok['name']}")

        def get_coord(coord: str) -> int:
            return int(coord[1:])

        xy = Coords( int(tok['x_coord'][1:]), int(tok['y_coord'][1:]) )

        self.max_x = max(self.max_x, xy.x)
        self.max_y = max(self.max_y, xy.y)

        if xy.hash not in self.node_dict:
            label = None
            if 'label' in tok:
                label = tok['label']
            self.node_dict[xy.hash] = Node(tok['name'], tok['category'], label, xy, False)

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

    def _fill_invis_nodes(self):
        for x in range(self.max_x+1):
            for y in range(self.max_y+1):
                xy = Coords(x, y)
                if xy.hash not in self.node_dict:
                    self.node_dict[xy.hash] = Node(f"x{x}_y{y}", "", "", xy, True)

    def _print_invis_links(self):
        if self.max_y < 1:
            return

        for x in range(self.max_x+1):
            xy = Coords(x, 0)
            print(f"< {self.node_dict[xy.hash].name}")

            for y in range(1, self.max_y):
                xy = Coords(x, y)
                print("= style=invis")
                print(f"<> {self.node_dict[xy.hash].name}")

            xy = Coords(x, self.max_y)
            print("= style=invis")
            print(f"> {self.node_dict[xy.hash].name}")
            print("")

    def _print_ranksame_links(self):
        if self.max_x < 1:
            return

        x0_node_names = [self.node_dict[Coords(x,0).hash].name \
                    for x in range(self.max_x+1)]
        print(" ".join(['@']+x0_node_names))

        for i, name in enumerate(x0_node_names):
            if i == 0:
                print(f"< {name}")
            elif i+1 < len(x0_node_names):
                print("= style=invis")
                print(f"<> {name}")
            else:
                print("= style=invis")
                print(f"> {name}")

    def print_lines(self, cat_dict: tp.Dict[str, str]):
        self._fill_invis_nodes()

        for node in self.node_dict.values():
            node_line = f"- {node.name}"
            if node.label:
                node_label = " ".join(node.label.asList())
                node_line += f" | {node_label}"
            print(node_line+"")
            if node.invis:
                print(f"= style=invis")
            elif node.category in cat_dict:
                print(f"= {cat_dict[node.category]}")
            print("")

        for line in self.link_lines:
            print(line)

        print("")
        self._print_invis_links()

        self._print_ranksame_links()

