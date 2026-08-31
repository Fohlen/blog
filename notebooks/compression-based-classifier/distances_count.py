from collections import defaultdict

import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm



if __name__ == "__main__":
    dataset_train = fetch_20newsgroups(subset='train', random_state=123)
    dataset_test = fetch_20newsgroups(subset='test', random_state=123)
    
    vectorizer = CountVectorizer()
    train_dataset_count = vectorizer.fit_transform(dataset_train["data"])
    test_dataset_count = vectorizer.transform(dataset_test["data"])
    
    # calculate number of tokens per row, this is analogous to len(gzip(...))
    train_dataset_count_len = train_dataset_count.sum(axis=1).squeeze().tolist()[0]
    test_dataset_count_len = test_dataset_count.sum(axis=1).squeeze().tolist()[0]
    
    # nonzero indexes represents where data is actually stored
    indices_row_train = defaultdict(set)
    indices_row_test = defaultdict(set)
    
    for row, column in zip(*train_dataset_count.nonzero()):
        indices_row_train[row].add(column)
    
    for row, column in zip(*test_dataset_count.nonzero()):
        indices_row_test[row].add(column)

    count_distances = []

    print("Calculating count distance matrix")
    
    for index_x1, Cx1 in tqdm(enumerate(test_dataset_count_len), total=len(test_dataset_count_len)):
        distance_from_x1 = []
    
        for index_x2, Cx2 in enumerate(train_dataset_count_len):
            intersect = indices_row_test[index_x1].intersection(indices_row_train[index_x2])
            Cx1x2 = (Cx1 + Cx2) - len(intersect)
            nd = (Cx1x2 - min(Cx1,Cx2)) / max(Cx1, Cx2)
            distance_from_x1.append(nd)
    
        count_distances.append(distance_from_x1)

    print("Stacking")
    count_matrix = np.stack(count_distances)
    print("Saving count distances")
    np.save(f"20newsgroups.count_distances.npy", count_matrix)
