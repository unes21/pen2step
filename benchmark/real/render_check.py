import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from gt_models import PARTS

check = ["02", "03", "13", "14"]
fig = plt.figure(figsize=(16, 8))
for i, k in enumerate(check, 1):
    code, fam, dims = PARTS[k]
    ns = {}; exec(code, ns); shp = ns["result"].val()
    verts, tris = shp.tessellate(0.3)
    v = np.array([[p.x, p.y, p.z] for p in verts]); t = np.array(tris)
    for j, az in enumerate([-50, 130]):
        ax = fig.add_subplot(2, 4, i + j*4, projection="3d")
        ax.add_collection3d(Poly3DCollection([v[tri] for tri in t], facecolor="#aac4e0",
                            edgecolor="#33506e", linewidths=0.3, alpha=0.95))
        mn, mx = v.min(0), v.max(0); ctr=(mn+mx)/2; r=(mx-mn).max()/2
        ax.set_xlim(ctr[0]-r,ctr[0]+r); ax.set_ylim(ctr[1]-r,ctr[1]+r); ax.set_zlim(ctr[2]-r,ctr[2]+r)
        ax.view_init(elev=22, azim=az); ax.set_title(f"{k}:{fam} az={az}", fontsize=10)
        ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.tick_params(labelsize=5)
plt.tight_layout(); plt.savefig("gt_check.png", dpi=85, bbox_inches="tight")
print("ok")
