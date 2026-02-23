import os
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from processor import process_file
from utils.timer import time_it

# ---------- Baseline ----------

@time_it
def run_baseline(files):
    results = []
    for f in files:
        results.append(process_file(f))
    return results

# ---------- Optimized (Multiprocessing chosen) ----------

@time_it
def run_optimized(files):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_file, files))
    return results

# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["baseline", "optimized"], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    files = [
        os.path.join(args.input, f)
        for f in os.listdir(args.input)
        if f.endswith(".csv")
    ]

    print(f"📂 Files found: {len(files)}")

    # Run baseline
    baseline_result, baseline_time = run_baseline(files)

    # Run optimized
    optimized_result, optimized_time = run_optimized(files)

    speedup = round(baseline_time / optimized_time, 2) if optimized_time else 0

    performance = {
        "filesProcessed": len(files),
        "baselineSeconds": baseline_time,
        "optimizedSeconds": optimized_time,
        "speedupX": speedup,
        "methodUsed": "multiprocessing",
    }

    os.makedirs(args.output, exist_ok=True)

    with open(os.path.join(args.output, "performance_results.json"), "w") as f:
        json.dump(performance, f, indent=4)

    print("✅ Performance results saved!")

if __name__ == "__main__":
    main()