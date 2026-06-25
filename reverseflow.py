import argparse
import pydot


def strip_cluster_prefix(name: str) -> str:
    return name[8:] if name.startswith("cluster_") else name


def reverse_flow(dot_file: str, out_file: str) -> None:
    dot = pydot.graph_from_dot_file(dot_file)[0]

    # Map node name to cluster name (None for root)
    node_to_cluster = {}
    # Map cluster name to cluster object
    cluster_objs = {}

    def process_cluster(clus: pydot.Cluster, parent_name: str | None):
        name = strip_cluster_prefix(clus.get_name())
        cluster_objs[name] = clus
        for node in clus.get_nodes():
            node_to_cluster[node.get_name()] = name
        for sub in clus.get_subgraphs():
            if isinstance(sub, pydot.Cluster):
                process_cluster(sub, name)

    # Process root cluster
    for node in dot.get_nodes():
        node_to_cluster[node.get_name()] = None
    for sub in dot.get_subgraphs():
        if isinstance(sub, pydot.Cluster):
            process_cluster(sub, None)

    # Group edges by cluster
    cluster_edges = {name: [] for name in cluster_objs}
    cluster_edges[None] = []
    for edge in dot.get_edges():
        src = edge.get_source()
        dst = edge.get_destination()
        src_cluster = node_to_cluster.get(src)
        dst_cluster = node_to_cluster.get(dst)
        if src_cluster == dst_cluster:
            cluster_edges[src_cluster].append(edge)
        else:
            cluster_edges[None].append(edge)

    lines = []

    def write_cluster(name: str | None):
        if name is None:
            clus = dot
            header_written = False
        else:
            clus = cluster_objs[name]
            header_written = True
            # cluster header
            header = f"/@ {name}"
            label = clus.get_attributes().get("label")
            if label:
                header += f" | {label}"
            lines.append(header)
        # cluster attributes (excluding label)
        attrs = clus.get_attributes()
        if name is not None:
            for key, value in attrs.items():
                if key == "label":
                    continue
                lines.append(f"= {key}={value}")
        # nodes in cluster
        for node in clus.get_nodes():
            node_name = node.get_name()
            lines.append(f"- {node_name}")
            node_attrs = node.get_attributes()
            for key, value in node_attrs.items():
                lines.append(f"= {key}={value}")
        # subclusters
        for sub in clus.get_subgraphs():
            if isinstance(sub, pydot.Cluster):
                sub_name = strip_cluster_prefix(sub.get_name())
                write_cluster(sub_name)
        # edges in this cluster
        for edge in cluster_edges.get(name, []):
            src = edge.get_source()
            dst = edge.get_destination()
            lines.append(f"< {src}")
            lines.append(f"> {dst}")
            edge_attrs = edge.get_attributes()
            for key, value in edge_attrs.items():
                lines.append(f"= {key}={value}")
        if name is not None:
            lines.append("@/")

    write_cluster(None)
    with open(out_file, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dot_file", help="input .dot file")
    parser.add_argument("out_file", help="output .txt file")
    args = parser.parse_args()

    reverse_flow(args.dot_file, args.out_file)
