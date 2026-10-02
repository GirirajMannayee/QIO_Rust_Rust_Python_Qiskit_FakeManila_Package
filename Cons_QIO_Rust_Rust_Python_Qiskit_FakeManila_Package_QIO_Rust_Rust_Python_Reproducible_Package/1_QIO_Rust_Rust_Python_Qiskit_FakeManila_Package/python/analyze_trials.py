import pandas as pd
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "../data/S1_S4_trial_data.csv"
df = pd.read_csv(path)

summary = (df.groupby(["scenario","algorithm"])
    .agg(trials=("trial_id","size"),
         success_rate_pct=("grasp_success", lambda x: 100*x.mean()),
         response_time_ms=("response_time_ms","mean"),
         force_error_N=("force_error_N","mean"),
         collision_rate_pct=("collision","mean"))
    .reset_index())
summary["collision_rate_pct"] *= 100
print(summary.to_string(index=False))
summary.to_csv("../results/summary.csv", index=False)
