import pandas as pd
from scipy import stats
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "../data/S1_S4_trial_data.csv"
df = pd.read_csv(path)

rows=[]
for scenario, g in df.groupby("scenario"):
    groups = [x["response_time_ms"].values for _,x in g.groupby("algorithm")]
    h,p = stats.kruskal(*groups)
    rows.append({"scenario":scenario,"metric":"response_time_ms",
                 "kruskal_H":h,"p_value":p})
out=pd.DataFrame(rows)
print(out.to_string(index=False))
out.to_csv("../results/statistical_tests.csv", index=False)
