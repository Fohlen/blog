import sys
import json
from statistics import quantiles

if __name__ == "__main__":
    distances = []

    for line in sys.stdin:
        doc = json.loads(line)
        distances.append(doc["distance"])

    for quantile in quantiles(distances, n=100):
        print(quantile, file=sys.stdout)
