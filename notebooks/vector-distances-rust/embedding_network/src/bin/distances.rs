use std::fs::{OpenOptions};
use std::io::{LineWriter, Write};
use std::path::{Path, PathBuf};
use tqdm::pbar;
use embedding_network::{cosine_dist_rust_loop_vec, load_model};


fn write_distances(model_path: &Path, output_path: &Path) {
    let model = load_model(model_path).unwrap();
    let mut pbar = pbar(Some(model.len() * model.len()));
    let file = OpenOptions::new()
        .write(true)
        .create(true)
        .open(output_path).unwrap();
    let mut writer = LineWriter::new(file);

    for (_, vec1) in &model {
        for (_, vec2) in &model {
            pbar.update(1).unwrap();
            let distance = cosine_dist_rust_loop_vec(
                vec1,
                vec2,
                &(vec1.len() as i64)
            );

            writer.write_fmt(format_args!("{}\n", distance)).unwrap();
        }
    }

    writer.flush().unwrap();
}


struct Cli {
    input: PathBuf,
    output: PathBuf,
}

fn main() {
    let input_path = std::env::args().nth(1).expect("no input path given");
    let output_path = std::env::args().nth(2).expect("no output path given");

    let args = Cli {
        input: PathBuf::from(input_path),
        output: PathBuf::from(output_path),
    };

    write_distances(args.input.as_path(), args.output.as_path());
}
