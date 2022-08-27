import pydotplus.graphviz as pdg

bigdot = pdg.Dot()

dot = pdg.Cluster("clus1")
smol = pdg.Cluster("clus2")
bigdot.add_subgraph( dot )
dot.add_subgraph( smol )

smol.add_node( pdg.Node("A") )
smol.add_node( pdg.Node("B") )

dot.add_edge( pdg.Edge("A", "B") )

bigdot.write("wah.dot")
