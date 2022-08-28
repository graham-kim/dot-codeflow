import pyparsing as pp
import pydot as pd

import typing as tp
from enum import Enum
from parsers.interface import ParserInterface
from parsers.lib_general.node import NodeParser
from parsers.lib_general.link import LinkParser

def cluster_pattern() -> pp.And:
    return pp.Word("/@") \ # Start of line
         + pp.Group(pp.Word(pp.alphanums+"_-")[1,...])("name") \
         + pp.Optional(
              pp.Suppress("|") \ # Start of optional labels
            + pp.Combine(
                  pp.Word(pp.alphas) + "=" + pp.Word(pp.alphanums+'"'+"'") \
                + pp.Optional(pp.Suppress(",")) # Allow comma separation
              )[1,...]("labels")
          )

class GeneralParser(ParserInterface):
    class CurrentMode(Enum):
        NOT_PARSING = 0
        PARSE_NODE  = 1
        PARSE_LINK  = 2

    def __init__(self):
        self.mode = self.CurrentMode.NOT_PARSING
        self.dot = pd.Dot()
        self.node_parser = NodeParser(self.dot)
        self.link_parser = LinkParser(self.dot)
        self.clus_dict: tp.Dict[str, pd.Cluster] = {}
        self.curr_clus_hierarchy: tp.List[str] = None

        self.pp_cluster_pattern = cluster_pattern()

    def _finish_current_parsing(self):
        if self.mode == self.CurrentMode.PARSE_NODE:
            pass
        elif self.mode == self.CurrentMode.PARSE_LINK:
            pass
        self.mode = self.CurrentMode.NOT_PARSING

    def _clus_joined_name(self) -> str:
        return '@'.join(self.curr_clus_hierarchy)

    def _get_curr_cluster(self) -> pd.Cluster:
        return self.clus_dict[self._clus_joined_name()]

    def _parse_enter_cluster(self, line_num: int, stripped_line: str):
        if self.curr_clus_hierarchy:
            parent_clus = self._get_curr_cluster()
        else:
            parent_clus = self.dot

        tok = self.pp_cluster_pattern.parseString(stripped_line)
        self.curr_clus_hierarchy.append(tok["name"])

        if self._clus_joined_name() in self.clus_dict:
            clus = self._get_curr_cluster()
        else:
            clus = pd.Cluster(tok["name"])
            parent_clus.add_subgraph(clus)

        if "labels" in tok:
            for label in tok["labels"]:
                attrname, value = label.split('=')
                attrname = "set_" + attrname

                if not hasattr(clus, attrname):
                    raise Exception(f"pydot.Cluster has no {attrname} attribute\n{i}: {stripped_line}")

                getattr(clus, attrname)(value) # e.g. set_label() or set_bgcolor()

    def parse_file(self, filename: str) -> None:
        with open(filename, "r") as inF:
            for i, line in enumerate(inF):
                stripped_line = line.strip('\n').strip()
                if stripped_line.startswith('#'):
                    continue
                elif len(stripped_line) == 0:
                    self._finish_current_parsing()
                elif stripped_line.startswith('/@'):
                    self._parse_enter_cluster(i, stripped_line)
                elif stripped_line.startswith('@/'):
                    if not self.curr_clus_hierarchy:
                        raise Exception(f"Got an @/ when no cluster had been started with /@ first:\n{i}: {stripped_line}")
                    self.curr_clus_hierarchy.pop()
                elif stripped_line.startswith('>') or stripped_line.startswith('<'):
                    if self.mode == self.CurrentMode.PARSE_NODE:
                        raise Exception(f"Got a link line while parsing a node:\n{i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_LINK

                    # get clus from dict
                    raise NotImplementedError("Implement me")
                else:
                    if self.mode == self.CurrentMode.PARSE_LINK:
                        raise Exception(f"Got a node line while parsing a link:\n{i}: {stripped_line}")
                    self.mode = self.CurrentMode.PARSE_NODE

                    # get clus from dict
                    raise NotImplementedError("Implement me")

        self._finish_current_parsing()

    def get_pydot_dot(self):
        self.dot