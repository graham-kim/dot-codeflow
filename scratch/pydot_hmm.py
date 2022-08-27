from PIL import Image
from io import BytesIO

import pydot as pd

def view_pydot(pdot):
    bytes = BytesIO(pdot.create_png())
    Image.open(bytes).show()

bigdot = pd.Dot()

dot = pd.Cluster("clus1")
smol = pd.Cluster("clus2")
bigdot.add_subgraph( dot )
dot.add_subgraph( smol )

smol.add_node( pd.Node("A") )
smol.add_node( pd.Node("C") )

dot.add_edge( pd.Edge("A", "C") )

view_pydot(bigdot)
#bigdot.write("wah.dot")
