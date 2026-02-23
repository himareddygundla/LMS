import os
import pandas as pd
import random

folder = "bulk_data"
os.makedirs(folder, exist_ok=True)

num_files = 200 # change if needed

for i in range(1, num_files + 1):
    data = {
        "studentId": list(range(1, 101)),
        "marks": [random.randint(30, 100) for _ in range(100)],
    }

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(folder, f"file{i}.csv"), index=False)

print("✅ Dummy files generated!")