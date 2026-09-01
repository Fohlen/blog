use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

pub type Embedding = HashMap<String, Vec<f64>>;


pub fn load_model(input_file: &Path) -> Result<Embedding, std::io::Error> {
    let mut model = HashMap::new();
    let file = File::open(input_file)?;
    let reader = BufReader::new(file);

    for line in reader.lines() {
        let line = line?;
        let items: Vec<String> = line.split_whitespace().map(|s| s.to_string()).collect();
        let word = items[0].clone();
        let embedding: Vec<f64> = items[1..]
            .iter()
            .map(|s| s.parse::<f64>())
            .collect::<Result<Vec<_>, _>>().unwrap();
        model.insert(word, embedding);
    }

    Ok(model)
}

pub fn cosine_dist_rust_loop_vec(vec_a: &[f64], vec_b: &[f64], vec_size: &i64) -> f64
{
    let mut a_dot_b:f64 = 0.0;
    let mut a_mag:f64 = 0.0;
    let mut b_mag:f64 = 0.0;

    for i in 0..*vec_size as usize
    {
        a_dot_b += vec_a[i] * vec_b[i];
        a_mag += vec_a[i] * vec_a[i];
        b_mag += vec_b[i] * vec_b[i];
    }

    let dist:f64 = 1.0 - (a_dot_b / (a_mag.sqrt() * b_mag.sqrt()));

    return dist
}
