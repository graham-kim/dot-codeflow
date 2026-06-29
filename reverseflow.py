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
    cluster_edges = {None: []}

    def process_cluster(clus: pydot.core.Subgraph, parent_name: str | None):
        name = strip_cluster_prefix(clus.get_name())
        cluster_edges[name] = []
        cluster_objs[name] = clus
        for node in clus.get_nodes():
            node_to_cluster[node.get_name()] = name

        for edge in clus.get_edges():
            src = edge.get_source()
            dst = edge.get_destination()
            src_cluster = node_to_cluster.get(src)
            dst_cluster = node_to_cluster.get(dst)
            if src_cluster == dst_cluster:
                cluster_edges[src_cluster].append(edge)
            else:
                cluster_edges[name].append(edge)

        for sub in clus.get_subgraphs():
            if isinstance(sub, pydot.core.Subgraph):
                process_cluster(sub, name)

    # Process root cluster
    for node in dot.get_nodes():
        node_to_cluster[node.get_name()] = None

    for edge in dot.get_edges():
        src = edge.get_source()
        dst = edge.get_destination()
        src_cluster = node_to_cluster.get(src)
        dst_cluster = node_to_cluster.get(dst)
        if src_cluster == dst_cluster:
            cluster_edges[src_cluster].append(edge)
        else:
            cluster_edges[None].append(edge)

    for sub in dot.get_subgraphs():
        if isinstance(sub, pydot.core.Subgraph):
            process_cluster(sub, None)

    def write_cluster(name: str | None, outF, prior_names: list[str] = []):
        if name is None:
            clus = dot
            header_written = False
        else:
            clus = cluster_objs[name]
            header_written = True
            prior_names.append(name)
            # cluster header
            header = f"\n/@ {name}"
            label = clus.get_attributes().get("label")
            if label:
                header += f" | {label}"
            outF.write(header+'\n')

            for key, value in clus.get_attributes().items():
                if key == "label":
                    continue
                outF.write(f"= {key}={value}\n")

        # nodes in cluster
        for node in clus.get_nodes():
            node_name = node.get_name()
            node_label = node.get_label()
            prior_names_joined = '_'.join(prior_names)
            if name is not None and node_name.startswith(prior_names_joined):
                name_len_1 = len(prior_names_joined) + 1
                node_name = node_name[name_len_1:]
            if node_label:
                node_label = node_label.replace('<BR/>', '\\n')
                # the label is bracked with < and >, don't print those
                outF.write(f"\n- {node_name} | {node_label[1:-1]}\n")
            else:
                outF.write(f"\n- {node_name}\n")

            # Node attributes, if any
            kv_pairs = [f"{k}={v}" for k, v in node.get_attributes().items() \
                        if k != "label"]
            if kv_pairs:
                kv_str = ' '.join(kv_pairs)
                outF.write(f"= {kv_str}\n")

        # subclusters
        for sub in clus.get_subgraphs():
            if isinstance(sub, pydot.core.Subgraph):
                sub_name = strip_cluster_prefix(sub.get_name())
                write_cluster(sub_name, outF, prior_names)

        # edges in this cluster
        for edge in cluster_edges.get(name, []):
            src = edge.get_source()
            dst = edge.get_destination()

            if name is not None and src.startswith(prior_names_joined) and dst.startswith(prior_names_joined):
                name_len_1 = len(prior_names_joined) + 1
                src = src[name_len_1:]
                dst = dst[name_len_1:]

            outF.write(f"\n< {src}\n")
            outF.write(f"> {dst}\n")
            for key, value in edge.get_attributes().items():
                outF.write(f"= {key}={value}\n")

        if name is not None:
            outF.write("\n@/\n")

    with open(out_file, "w") as outF:
        write_cluster(None, outF)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dot_file", help="input .dot file")
    parser.add_argument("out_file", help="output .txt file")
    args = parser.parse_args()

    reverse_flow(args.dot_file, args.out_file)
