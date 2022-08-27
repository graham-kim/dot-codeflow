import pydotplus.graphviz as pdg

dot = pdg.Dot()

dot.add_node( pdg.Node("A") )
dot.add_node( pdg.Node("B") )

dot.add_edge( pdg.Edge("A", "B") )

dot.write("wah.dot")