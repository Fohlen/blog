import logging

from mteb import MTEB
import spacy
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
activated = spacy.prefer_gpu()
logger.info(f"Loading spaCy on GPU: {activated}")

DISABLED_COMPONENTS = ["tagger", "parser", "attribute_ruler", "lemmatizer"]
TASK_LIST_CLASSIFICATION = [
    "AmazonCounterfactualClassification",
    "AmazonPolarityClassification",
    "AmazonReviewsClassification",
    "Banking77Classification",
    "EmotionClassification",
    "ImdbClassification",
    "MassiveIntentClassification",
    "MassiveScenarioClassification",
    "MTOPDomainClassification",
    "MTOPIntentClassification",
    "ToxicConversationsClassification",
    "TweetSentimentExtractionClassification",
]

TASK_LIST_CLUSTERING = [
    "ArxivClusteringP2P",
    "ArxivClusteringS2S",
    "BiorxivClusteringP2P",
    "BiorxivClusteringS2S",
    "MedrxivClusteringP2P",
    "MedrxivClusteringS2S",
    "RedditClustering",
    "RedditClusteringP2P",
    "StackExchangeClustering",
    "StackExchangeClusteringP2P",
    "TwentyNewsgroupsClustering",
]

TASK_LIST_PAIR_CLASSIFICATION = [
    "SprintDuplicateQuestions",
    "TwitterSemEval2015",
    "TwitterURLCorpus",
]

TASK_LIST_RERANKING = [
    "AskUbuntuDupQuestions",
    "MindSmallReranking",
    "SciDocsRR",
    "StackOverflowDupQuestions",
]

TASK_LIST_RETRIEVAL = [
    "ArguAna",
    "ClimateFEVER",
    "CQADupstackAndroidRetrieval",
    "CQADupstackEnglishRetrieval",
    "CQADupstackGamingRetrieval",
    "CQADupstackGisRetrieval",
    "CQADupstackMathematicaRetrieval",
    "CQADupstackPhysicsRetrieval",
    "CQADupstackProgrammersRetrieval",
    "CQADupstackStatsRetrieval",
    "CQADupstackTexRetrieval",
    "CQADupstackUnixRetrieval",
    "CQADupstackWebmastersRetrieval",
    "CQADupstackWordpressRetrieval",
    "DBPedia",
    "FEVER",
    "FiQA2018",
    "HotpotQA",
    "MSMARCO",
    "NFCorpus",
    "NQ",
    "QuoraRetrieval",
    "SCIDOCS",
    "SciFact",
    "Touche2020",
    "TRECCOVID",
]

TASK_LIST_STS = [
    "BIOSSES",
    "SICK-R",
    "STS12",
    "STS13",
    "STS14",
    "STS15",
    "STS16",
    "STS17",
    "STS22",
    "STSBenchmark",
    "SummEval",
]

TASK_LIST = (
    TASK_LIST_CLASSIFICATION
    + TASK_LIST_CLUSTERING
    + TASK_LIST_PAIR_CLASSIFICATION
    + TASK_LIST_RERANKING
    + TASK_LIST_RETRIEVAL
    + TASK_LIST_STS
)


class SpacyModel:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.trf_model = "trf" in model_name
        self.nlp = spacy.load(model_name)


    def encode(self, sentences, batch_size=32, **kwargs):
        """
        Returns a list of embeddings for the given sentences.
        Args:
            sentences (`List[str]`): List of sentences to encode
            batch_size (`int`): Batch size for the encoding

        Returns:
            `List[np.ndarray]` or `List[tensor]`: List of embeddings for the given sentences
        """

        if self.trf_model:
            return [
                np.mean([tensor.get() for tensor in doc._.trf_data.tensors[1]], axis=0) if len(doc._.trf_data.tensors) > 1 else np.zeros(768, dtype=np.float32)
                for doc in self.nlp.pipe(sentences, batch_size=batch_size, disable=DISABLED_COMPONENTS, n_process=1)
            ]
        else:
            return [
                doc.vector if len(doc.vector) else np.zeros(96, dtype=np.float32) 
                for doc in self.nlp.pipe(sentences, batch_size=batch_size, disable=DISABLED_COMPONENTS, n_process=-1)
            ]


if __name__ == "__main__":
    models = ["en_core_web_trf", "en_core_web_sm"]
    for model_name in models:
        model = SpacyModel(model_name)
        evaluation = MTEB(task_langs=["en"])
        for task in TASK_LIST:
            logger.info(f"Running task: {task}")
            eval_splits = ["dev"] if task == "MSMARCO" else ["test"]
            evaluation = MTEB(tasks=[task], task_langs=["en"])  # Remove "en" for running all languages
            evaluation.run(model, output_folder=f"results/{model_name}", eval_splits=eval_splits)

    logger.info("Done")
