import csv
import subprocess
import re
from itertools import product
from tqdm import tqdm

success_re = re.compile(r"SUCCESSES: (\d+) \| FAILURES: (\d+)")

# Define the parameters for the load test
durations = [10, 15, 30]
workers = [1, 5, 10]
scenarios = ["loadtest.py", "loadtest_grpc.py"]

if __name__ == "__main__":
    results = []
    for duration, num_workers, scenario in tqdm(product(durations, workers, scenarios), total=len(workers)*len(durations)*len(scenarios)):
        completed_process_loadtest = subprocess.run(["molotov", "-c", "-d", str(duration), "-w", str(num_workers), scenario], capture_output=True)
        match_loadtest = success_re.search(completed_process_loadtest.stdout.decode())
        results.append((scenario, str(duration), str(num_workers), match_loadtest.group(1), match_loadtest.group(2)))
    
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["scenario", "duration", "num_workers", "successes", "failures"])
        writer.writerows(results)
