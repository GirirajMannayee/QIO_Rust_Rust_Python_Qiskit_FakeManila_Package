import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

path = sys.argv[1] if len(sys.argv) > 1 else "../data/S1_S4_trial_data.csv"
df = pd.read_csv(path)
out = Path("../results")
out.mkdir(exist_ok=True)

metrics = [
    ("grasp_success","Success rate","success_rate.png"),
    ("response_time_ms","Response time (ms)","response_time.png"),
    ("force_error_N","Force error (N)","force_error.png"),
    ("collision","Collision rate","collision_rate.png")
]

for col,title,name in metrics:
    if col in ["grasp_success","collision"]:
        g=df.groupby(["scenario","algorithm"])[col].mean().reset_index()
        g[col] *= 100
    else:
        g=df.groupby(["scenario","algorithm"])[col].mean().reset_index()
    for alg in g.algorithm.unique():
        s=g[g.algorithm==alg]
        plt.plot(s.scenario,s[col],marker="o",label=alg)
    plt.xlabel("Scenario")
    plt.ylabel(title + (" (%)" if col in ["grasp_success","collision"] else ""))
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/name,dpi=300)
    plt.close()
