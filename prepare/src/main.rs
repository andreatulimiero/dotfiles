use clap::Parser;
use std::fs;
use regex::Regex;
use std::io;
use std::path::PathBuf;
use walkdir::WalkDir;
use std::collections::HashSet;

#[derive(Parser, Debug)]
struct Cli {
    #[arg(short = 'C', long, default_value = ".")]
    dir: String,
    #[arg(short, long, default_value_t = false)]
    comment: bool,
    #[arg(short, long, default_value_t = true)]
    decomment: bool,
    #[arg(short, long, default_value_t = false)]
    follow_sym: bool,
}

enum Action {
    COMMENT,
    UNCOMMENT,
    NONE,
}

fn inspect_file(file: &PathBuf) {
    if file.is_dir() {
        return;
    }
    let re = Regex::new(r">\s*\[(?P<comment_start>[^0-9A-Za-z]+)@(?P<comment_end>[^0-9A-Za-z]+)(?P<hostname>[0-9A-Za-z]+)\]").unwrap();
    let res = std::fs::read_to_string(file);
    match res {
        Ok(content) => {
            let mut match_found = false;
            for line in content.lines() {
                if re.is_match(line) {
                    match_found = true;
                    println!("{}",line)
                }
            }
            if match_found {
                println!("{:?}",file)
            }
        }
        Err(_) => {}
    }
}

fn inspect_dir(dirname: String, action: Action, follow_sym: bool) {
    let ignore: HashSet<&str> = HashSet::from(
        ["./.git", "./.gitignore", "./prepare.py", "./plugged", "./__pycache__", "./README.md", "./prepare"]);

    WalkDir::new(".")
        .into_iter()
        .filter_entry(|f| !ignore.contains(f.path().to_str().unwrap()))
        .filter_map(|f| f.ok())
        .for_each(|f| { inspect_file(&f.into_path()); })
}

fn main() {
    let args = Cli::parse();
    inspect_dir(args.dir, Action::COMMENT, args.follow_sym)
}
