import pyparsing as pp
import pydot as pd

import typing as tp
from enum import Enum
from parsers.interface import ParserInterface
from parsers.lib_general.node import NodeStorage
from parsers.lib_general.link import MultiLinksStorage
import parsers.lib_general.patterns as ppp

from parsers.lib_general.utils import prepend_clus_name

class GeneralParser(ParserInterface):
    class CurrentMode(Enum):
        NOT_PARSING = 0
        PARSE_NODE  = 1
        PARSE_LINK  = 2
        PARSE_NODE_AND_LINKS = 3
        PARSE_CLUSTER = 4

    def __init__(self):
        self.mode = self.CurrentMode.NOT_PARSING
        self.dot = pd.Dot()

        self.clus_dict: tp.Dict[str, pd.Cluster] = {}
        self.curr_clus_hierarchy: tp.List[str] = []

        self.curr_node: NodeStorage = None
        self.curr_links: MultiLinksStorage = None

        self.pp_cluster_pattern = ppp.cluster_pattern()
        self.pp_node_pattern = ppp.node_pattern()
        self.pp_link_pattern = ppp.link_pattern()
        self.pp_dot_attr_pattern = ppp.dot_attr_pattern()
        self.pp_ranksame_pattern = ppp.ranksame_pattern()

        self.ranksame_lists: tp.List[tp.List[str]] = []

    def _finish_current_parsing(self):
        if self.mode == self.CurrentMode.PARSE_NODE:
            self.curr_node.add_to_cluster()
            self.curr_node = None
        elif self.mode == self.CurrentMode.PARSE_LINK:
            self.curr_links.finish_links()
            self.curr_links.add_to_cluster()
            self.curr_links = None
        elif self.mode == self.CurrentMode.PARSE_NODE_AND_LINKS:
            pass
        self.mode = self.CurrentMode.NOT_PARSING

    @property
    def clus_joined_name(self) -> str:
        return '_'.join(self.curr_clus_hierarchy)

    def _get_curr_cluster(self) -> pd.Cluster:
        if self.curr_clus_hierarchy:
            return self.clus_dict[self.clus_joined_name]
        else:
            return self.dot

    def _parse_enter_cluster(self, line_num: int, stripped_line: str) -> None:
        if self.curr_clus_hierarchy:
            parent_clus = self._get_curr_cluster()
        else:
            parent_clus = self.dot

        tok = self.pp_cluster_pattern.parseString(stripped_line)
        self.curr_clus_hierarchy.append(tok["name"])

        if self.clus_joined_name in self.clus_dict:
            clus = self._get_curr_cluster()
        else:
            clus = pd.Cluster(tok["name"])
            clus.set_label(tok["name"])
            parent_clus.add_subgraph(clus)
            self.clus_dict[self.clus_joined_name] = clus

        if "label" in tok and tok["label"]:
            label = " ".join(tok["label"]).replace("@this@", tok["name"])
            clus.set_label(label)

    def _add_cluster_attr(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_dot_attr_pattern.parseString(stripped_line)
        for dot_attr in tok["attrs"]:
            attrname, value = dot_attr.split('=')
            attrname = "set_" + attrname

            if not hasattr(self._get_curr_cluster(), attrname):
                raise Exception(f"pydot.Cluster has no {attrname} attribute\nline {line_num}: {stripped_line}")

            getattr(self._get_curr_cluster(), attrname)(value)

    def _parse_new_node(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_node_pattern.parseString(stripped_line)
        self.curr_node = NodeStorage(tok.name, tok.label, self._get_curr_cluster(), self.clus_joined_name)

    def _add_node_attr(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_dot_attr_pattern.parseString(stripped_line)
        for dot_attr in tok["attrs"]:
            attrname, value = dot_attr.split('=')
            attrname = "set_" + attrname

            self.curr_node.dot_attrs[attrname] = value

    def _parse_link_line(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_link_pattern.parseString(stripped_line)
        if not self.curr_links:
            self.curr_links = MultiLinksStorage(self._get_curr_cluster(), self.clus_joined_name)

        try:
            if tok["operator"][0] == "<":
                self.curr_links.add_src(tok)
            elif tok["operator"][0] == ">":
                self.curr_links.add_dst(tok)
            else: # <>
                self.curr_links.add_dst(tok)
                self.curr_links.finish_links()
                self.curr_links.add_src(tok)
        except Exception as ex:
            raise Exception(f"Above exception caused by line {line_num}:\n{stripped_line}") from ex

    def _add_link_attr(self, line_num: int, stripped_line: str) -> None:
        tok = self.pp_dot_attr_pattern.parseString(stripped_line)
        try:
            self.curr_links.add_dot_attrs(tok)
        except Exception as ex:
            raise Exception(f"Above exception caused by line {line_num}:\n{stripped_line}") from ex

    def _add_ranksame_line(self, line_num: int, stripped_line: str) -> None:
        try:
            tok = self.pp_ranksame_pattern.parseString(stripped_line)
        except Exception as ex:
            raise Exception(f"Above exception caused by line {line_num}:\n{stripped_line}") from ex

        if "ranksame" in tok:
            ranksames = []
            for name in tok["ranksame"]:
                full_name = prepend_clus_name(self.clus_joined_name, name)
                ranksames.append(full_name)

            self.ranksame_lists.append(ranksames)

    def _parsing_node_or_link(self) -> bool:
        return self.mode in (
            self.CurrentMode.PARSE_NODE,
            self.CurrentMode.PARSE_LINK,
            self.CurrentMode.PARSE_NODE_AND_LINKS,
        )

    def parse_file(self, filename: str) -> None:
        with open(filename, "r") as inF:
            for i, line in enumerate(inF):
                stripped_line = line.strip('\n').strip()
                if stripped_line.startswith('#'):
                    continue
                elif len(stripped_line) == 0:
                    self._finish_current_parsing()
                elif stripped_line.startswith('/@'):
                    if self._parsing_node_or_link():
                        raise Exception(f"Finish parsing node/link before starting a new cluster:\nline {i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_CLUSTER
                    self._parse_enter_cluster(i, stripped_line)
                elif stripped_line.startswith('@/'):
                    if not self.curr_clus_hierarchy:
                        raise Exception(f"Got an @/ when no cluster had been started with /@ first:\nline {i}: {stripped_line}")
                    self._finish_current_parsing()
                    self.curr_clus_hierarchy.pop()
                elif stripped_line.startswith('> ') or stripped_line.startswith('< ') \
                  or stripped_line.startswith('<>'):
                    if self.mode in (self.CurrentMode.PARSE_NODE, self.CurrentMode.PARSE_NODE_AND_LINKS):
                        raise Exception(f"Got a link line while parsing a node:\nline {i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_LINK

                    self._parse_link_line(i, stripped_line)
                elif stripped_line.startswith('- '):
                    if self.mode == self.CurrentMode.PARSE_LINK:
                        raise Exception(f"Got a node line while parsing a link:\nline {i}: {stripped_line}")
                    self._finish_current_parsing()
                    self.mode = self.CurrentMode.PARSE_NODE

                    self._parse_new_node(i, stripped_line)
                elif stripped_line.startswith('= '):
                    if self.mode == self.CurrentMode.NOT_PARSING:
                        raise Exception(f"Start a node or link before specifying DOT object attributes:\nline {i}: {stripped_line}")
                    elif self.mode == self.CurrentMode.PARSE_CLUSTER:
                        self._add_cluster_attr(i, stripped_line)
                    elif self.mode == self.CurrentMode.PARSE_LINK:
                        self._add_link_attr(i, stripped_line)
                    else:
                        self._add_node_attr(i, stripped_line)
                elif stripped_line.startswith('@ '):
                    self._add_ranksame_line(i, stripped_line)
                elif stripped_line.startswith('>>@') or stripped_line.startswith('<<@'):
                    raise NotImplementedError("Implement me")

        self._finish_current_parsing()

    def get_pydot_dot(self) -> tp.Tuple[pd.Dot, tp.List[tp.List[str]]]:
        return self.dot, self.ranksame_lists