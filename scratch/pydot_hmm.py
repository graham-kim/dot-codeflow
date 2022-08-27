import pydot as pd

bigdot = pd.Dot()

dot = pd.Cluster("clus1")
smol = pd.Cluster("clus2")
bigdot.add_subgraph( dot )
dot.add_subgraph( smol )

smol.add_node( pd.Node("A") )
smol.add_node( pd.Node("C") )

dot.add_edge( pd.Edge("A", "C") )

bigdot.write("wah.dot")
