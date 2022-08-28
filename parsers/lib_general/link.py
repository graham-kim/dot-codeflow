import typing as tp
import pydot as pd
import pyparsing as pp

from dataclasses import dataclass

@dataclass
class LinkStorage:
    src: str
    dst: str
    dot_attrs: tp.Dict[str, str]
    label: str
    clus: pd.Cluster
    clus_full_name: str

    def _prepend_clus_name(self, text: str) -> str:
        if self.clus_full_name:
            return f"{self.clus_full_name}_{text}"
        else:
            return text

    @property
    def full_src(self) -> str:
        return self._prepend_clus_name(self.src)

    @property
    def full_dst(self) -> str:
        return self._prepend_clus_name(self.dst)

    def _transform_label(self) -> str:
        return self.label

    def add_to_cluster(self) -> None:
        #pre_existing = self.clus.get_edge(x, y)
        #@3*@
        pre_existing = self.clus.get_edge(self.full_src, self.full_dst)
        if pre_existing:
            link = pre_existing[0]
        else:
            link = pd.Edge(self.full_src, self.full_dst)
            self.clus.add_edge(link)

        transformed_label = self._transform_label()
        if transformed_label:
            link.set_label(transformed_label)

        for attrname,value in self.dot_attrs.items():
            if not hasattr(link, attrname):
                raise Exception(f"pydot.Link has no {attrname} attribute")
            getattr(link, attrname)(value) # e.g. set_label() or set_bgcolor()

class MultiLinksStorage:
    @dataclass
    class DstWithLabel:
        dst: str
        label: str

    def __init__(self, clus: pd.Cluster, clus_full_name: str):
        self.current_srcs: tp.List[str] = []
        self.current_dsts: tp.List[DstWithLabel] = []
        self.current_dot_attrs: tp.Dict[str, str] = {}
        self.finished_links: tp.List[LinkStorage] = []

        self.clus = clus
        self.clus_full_name = clus_full_name

    def finish_links(self):
        if self.current_srcs and not self.current_dsts:
            raise Exception("Need to specify at least one src before finishing link")
        if not self.current_srcs and self.current_dsts:
            raise Exception("Need to specify at least one dst before finishing link")

        for dstdata in self.current_dsts:
            for src in self.current_srcs:
                link = LinkStorage(src, dstdata.dst, self.current_dot_attrs, dstdata.label, \
                                   self.clus, self.clus_full_name)
                self.finished_links.append(link)
        self.current_dsts = []
        self.current_srcs = []
        self.current_dot_attrs = {}

    def add_src(self, tok: pp.ParseResults):
        if self.current_dsts:
            raise Exception(f"Finish current links before adding new sources")

        self.current_srcs.append(tok["name"])

    def add_dst(self, tok: pp.ParseResults):
        if not self.current_srcs:
            raise Exception(f"Add sources before adding destinations")

        label = tok["label"] if "label" in tok else None

        dst_and_label = self.DstWithLabel(tok["name"], label)
        self.current_dsts.append(dst_and_label)

    def add_dot_attrs(self, tok: pp.ParseResults):
        if not self.current_srcs:
            raise Exception(f"Add sources before adding dot attributes")

        for dot_attr in tok["attrs"]:
            attrname, value = dot_attr.split('=')
            attrname = "set_" + attrname

            self.current_dot_attrs.dot_attrs[attrname] = value

    def add_to_cluster(self) -> None:
        for link in self.finished_links:
            link.add_to_cluster()