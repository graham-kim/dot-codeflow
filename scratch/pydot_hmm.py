import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

import pydot as pd

def view_pydot(pdot):
    bytes = BytesIO(pdot.create_png())
    img = mpimg.imread(bytes)
    plt.imshow(img, aspect='equal')
    plt.show()

bigdot = pd.Dot()

dot = pd.Cluster("clus1")
smol = pd.Cluster("clus2")
bigdot.add_subgraph( dot )
dot.add_subgraph( smol )

smol.add_node( pd.Node("A") )
smol.add_node( pd.Node("C") )

dot.add_edge( pd.Edge("A", "C") )

print(dot.get_node("A"))
print(smol.get_node("A")[0].get_name())

smol.set_label("The Label")
smol.set_color("red")
smol.set_bgcolor("green")
smol.set_style("dashed")

#view_pydot(bigdot)
#bigdot.write("wah.dot")
