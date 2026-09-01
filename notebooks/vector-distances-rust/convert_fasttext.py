import argparse
from pathlib import Path

from fasttext import FastText
import fasttext.util
from tqdm import tqdm


def write_model(output_file: Path, model: FastText):
    with output_file.open("wt") as fp:
        for word in tqdm(model.words):
            line_elements = [word] + [str(num) for num in ft.get_word_vector(word)]
            line = " ".join(line_elements)
            print(line, file=fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    
    ft = fasttext.load_model('cc.en.300.bin')
    write_model(args.output_file, ft)
