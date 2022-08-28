import typing as tp
import pydot as pd

from parsers.lib_general.utils import prepend_clus_name

class NodeStorage:
    def __init__(self, name: str, label: tp.List[str], clus: pd.Cluster, clus_full_name: str):
        self.name = name
        self.dot_attrs: tp.Dict[str, str] = {}
        if label:
            self.label = " ".join(label)
        else:
            self.label = ""
        self.clus = clus
        self.clus_full_name = clus_full_name

    def _transform_label(self) -> str:
        return self.label.replace("@this@", self.name)

    def add_to_cluster(self) -> None:
        pre_existing = self.clus.get_node(self.name)
        if pre_existing:
            node = pre_existing[0]
        else:
            full_name = prepend_clus_name(self.clus_full_name, self.name)
            node = pd.Node(full_name)
            self.clus.add_node(node)

        transformed_label = self._transform_label()
        if transformed_label:
            node.set_label(transformed_label)

        for attrname,value in self.dot_attrs.items():
            if not hasattr(node, attrname):
                raise Exception(f"pydot.Node has no {attrname} attribute")
            getattr(node, attrname)(value) # e.g. set_label() or set_bgcolor()


