import gzip
from argparse import ArgumentParser
from os import cpu_count

import numpy as np
from tqdm.contrib.concurrent import thread_map
from sklearn.datasets import fetch_20newsgroups


dataset_train = fetch_20newsgroups(subset='train', random_state=123)["data"]
dataset_test = fetch_20newsgroups(subset='test', random_state=123)["data"]

compressed_train_set = [len(gzip.compress(x2.encode())) for x2 in dataset_train]
compressed_test_set = [len(gzip.compress(x1.encode())) for x1 in dataset_test]


def distances(tup: tuple[str, int]) -> list[int]:
    x1, Cx1 = tup
    distance_from_x1 = []

    for (x2, Cx2) in zip(dataset_train, compressed_train_set):
        x1x2 = " ".join([x1, x2])
        Cx1x2 = len(gzip.compress(x1x2.encode()))
        ncd = (Cx1x2 - min(Cx1,Cx2)) / max(Cx1, Cx2)
        distance_from_x1.append(ncd)

    return distance_from_x1


if __name__ == "__main__":
    parser = ArgumentParser("Calculate normalised compression distance")
    parser.add_argument("--max-workers", default=max(32, cpu_count() + 4), type=int)
    args = parser.parse_args()

    print("Saving training dataset")
    np.save(f"20newsgroups.train.npy", compressed_train_set)
    print("Saving test dataset")
    np.save(f"20newsgroups.test.npy", compressed_test_set)

    print("Calculating NCD")
    distances = thread_map(distances, zip(dataset_test, compressed_test_set), total=len(dataset_test), max_workers=args.max_workers)
    
    print("Stacking")
    distance_matrix = np.stack(distances)
    print("Saving NCD")
    np.save(f"20newsgroups.ncd.npy", distance_matrix)
