import pathlib
import argparse
import json
from collections import defaultdict
from statistics import mean
import csv
import sys


def result_from_path(input_file: pathlib.Path, property) -> float:
    with input_file.open() as fp:
        result_dict = json.load(fp)
        if "en" in result_dict["test"]:
            eval_dict = result_dict["test"]["en"]
        elif "en-en" in result_dict["test"]:
            eval_dict = result_dict["test"]["en-en"]
        else:
            eval_dict = result_dict["test"]
        if isinstance(property, str):
            return eval_dict[property]
        else:
            return property(eval_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("results_dir", type=pathlib.Path)

    args = parser.parse_args()
    eval_results = defaultdict(list)
    
    for classification_result in args.results_dir.glob("*Classification.json"):
        eval_results["Classification"].append(result_from_path(classification_result, "accuracy"))
    
    for clustering_result in args.results_dir.glob("*Clustering*.json"):
        eval_results["Clustering"].append(result_from_path(clustering_result, "v_measure"))

    for pair_classification_result in ["SprintDuplicateQuestions", "TwitterSemEval2015", "TwitterURLCorpus"]:
        prop = lambda d: d["cos_sim"]["precision"]
        eval_results["Pair classification"].append(result_from_path(args.results_dir / f"{pair_classification_result}.json", prop))

    for reranking_result in ["AskUbuntuDupQuestions", "MindSmallReranking", "SciDocsRR", "StackOverflowDupQuestions"]:
        eval_results["Reranking"].append(result_from_path(args.results_dir / f"{reranking_result}.json", "map"))

    for retrieval_result in args.results_dir.glob("*Retrieval.json"):
        eval_results["Retrieval"].append(result_from_path(retrieval_result, "ndcg_at_10"))

    prop_sum = lambda d: d["cos_sim"]["spearman"]

    for sts_result in ["BIOSSES", "SICK-R", "STS12", "STS13", "STS14", "STS15", "STS16", "STS17", "STS22", "STSBenchmark"]:
        eval_results["STS"].append(result_from_path(args.results_dir / f"{sts_result}.json", prop_sum))

    eval_results["Summarization"].append(result_from_path(args.results_dir / "SummEval.json", prop_sum))
    
    writer = csv.writer(sys.stdout)
    writer.writerows([
        (args.results_dir.name, task, round(mean(values) * 100, 2))
        for task, values in eval_results.items()
    ])
