use std::collections::{HashSet};
use std::fs::{OpenOptions};
use std::io::{LineWriter, Write};
use std::path::{Path, PathBuf};
use tqdm::pbar;
use embedding_network::{cosine_dist_rust_loop_vec, Embedding, load_model};


type Edges = HashSet<(usize, usize)>;

fn create_network(model: Embedding, threshold: f64) -> (Vec<String>, Edges) {
    let mut pbar = pbar(Some(model.len() * model.len()));
    let words: Vec<String> = model.keys().map(|key| key.to_string()).collect();
    let mut edges: HashSet<(usize, usize)> = HashSet::new();

    for (index1, word1) in words.iter().enumerate() {
        for (index2, word2) in words.iter().enumerate() {
            pbar.update(1).unwrap();

            if !edges.contains(&(index1, index2)) {
                let vec1 = model.get(word1).unwrap();
                let vec2 = model.get(word2).unwrap();
                let distance = cosine_dist_rust_loop_vec(
                    vec1,
                    vec2,
                    &(vec1.len() as i64)
                );

                if distance >= threshold {
                    edges.insert((index1, index2));
                }
            }
        }
    }

    return (words, edges);
}

fn write_graph(words: &Vec<String>, edges: &Edges, output_path: &Path) {
    let file = OpenOptions::new()
        .write(true)
        .create(true)
        .open(output_path).unwrap();
    let mut writer = LineWriter::new(file);

    for (index1, index2) in edges {
        writer.write_fmt(format_args!("{}\t{}\n", words[*index1], words[*index2])).unwrap()

    }
}


struct Cli {
    input: PathBuf,
    output: PathBuf,
    threshold: f64
}

fn main() {
    let input_path = std::env::args().nth(1).expect("no input path given");
    let output_path = std::env::args().nth(2).expect("no output path given");
    let threshold = std::env::args().nth(3).expect("no threshold given");

    let args = Cli {
        input: PathBuf::from(input_path),
        output: PathBuf::from(output_path),
        threshold: threshold.parse().unwrap()
    };

    let model = load_model(args.input.as_path()).unwrap();

    let (words, edges) = create_network(
        model,
        args.threshold
    );

    write_graph(&words, &edges, args.output.as_path());
}
