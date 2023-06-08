use clap::Parser;
use gethostname::gethostname;
use regex::Regex;
use std::collections::HashSet;
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;
use walkdir::WalkDir;
#[macro_use]
extern crate lazy_static;

#[derive(Parser, Debug)]
struct Cli {
    #[arg(short = 'C', long, default_value = ".")]
    dir: String,
    #[arg(short, long, default_value_t = false)]
    comment: bool,
    #[arg(short, long, default_value_t = false)]
    decomment: bool,
    #[arg(short, long, default_value_t = false)]
    follow_sym: bool,
}

#[derive(Debug)]
enum Action {
    COMMENT,
    UNCOMMENT,
    PREPARE,
}

fn action_from_args(args: &Cli) -> Action {
    if args.comment {
        Action::COMMENT
    } else if args.decomment {
        Action::UNCOMMENT
    } else {
        Action::PREPARE
    }
}

fn process_file(file: &PathBuf, action: &Action, hostname: &str) {
    lazy_static! {
        static ref RE: Regex = Regex::new(r">\s*\[(?P<comment_start>[^0-9A-Za-z]+)@(?P<comment_end>[^0-9A-Za-z]+)(?P<hostname>[0-9A-Za-z]+)\]").unwrap();
    }
    let res = std::fs::read_to_string(file);
    let mut lines: Vec<String> = Vec::new();
    match res {
        Ok(content) => {
            let mut match_found = false;
            for line in content.lines() {
                let modified_line = match RE.captures(line) {
                    Some(cap) => {
                        match_found = true;
                        let comment_start = cap.name("comment_start").unwrap().as_str();
                        let comment_end = cap.name("comment_end").unwrap().as_str();
                        let actual_comment_end = get_actual_comment_end(comment_end);
                        let target_hostname = cap.name("hostname").unwrap().as_str();
                        let should_comment = match action {
                            Action::COMMENT => true,
                            Action::UNCOMMENT => false,
                            Action::PREPARE => target_hostname != hostname,
                        };
                        println!("Before: {}", line);
                        let modified_line = {
                            if should_comment {
                                comment_line(line, comment_start, actual_comment_end)
                            } else {
                                decomment_line(line, comment_start, actual_comment_end)
                            }
                        };
                        println!("After:  {}", line);
                        modified_line
                    }
                    None => line.to_string(),
                };
                lines.push(modified_line)
            }
            if match_found {
                let mut file = File::options().write(true).open(file).unwrap();
                for line in lines {
                    file.write_all((line + "\n").as_bytes()).unwrap();
                }
            }
        }
        Err(_) => {}
    }
}

fn get_actual_comment_end(comment_end: &str) -> Option<&str> {
    match comment_end {
        "_" => None,
        _ => Some(comment_end),
    }
}

fn is_commented(line: &str, comment_start: &str, comment_end: Option<&str>) -> bool {
    println!("{} is_commented={}", line, line.starts_with(comment_start) && comment_end.map_or(true, |e| line.ends_with(e)));
    line.starts_with(comment_start) && comment_end.map_or(true, |e| line.ends_with(e))
}

fn comment_line(line: &str, comment_start: &str, comment_end: Option<&str>) -> String {
    if is_commented(line, comment_start, comment_end) {
        line.to_string()
    } else {
        format!("{}{}{}", comment_start, line, comment_end.unwrap_or(""))
    }
}

fn decomment_line(line: &str, comment_start: &str, comment_end: Option<&str>) -> String {
    if !is_commented(line, comment_start, comment_end) {
        line.to_string()
    } else {
        get_commented_line_content(line, comment_start, comment_end)
    }
}

fn get_commented_line_content(
    line: &str,
    comment_start: &str,
    comment_end: Option<&str>,
) -> String {
    let line_without_start = line.replacen(comment_start, "",1);
    match comment_end {
        Some(comment_end) => line_without_start
            .chars()
            .rev()
            .collect::<String>()
            .replace(&comment_end.chars().rev().collect::<String>(), "")
            .chars()
            .rev()
            .collect::<String>(),
        None => line_without_start,
    }
}

fn inspect_dir(dirname: &str, action: &Action, follow_sym: bool, hostname: &str) {
    lazy_static! {
        static ref IGNORE: HashSet<&'static str> = HashSet::from([
            ".git",
            ".gitignore",
            "prepare.py",
            "plugged",
            "__pycache__",
            "README.md",
            "prepare",
            "target",
        ]);
    }
    WalkDir::new(dirname)
        .follow_links(follow_sym)
        .into_iter()
        .filter_entry(|e| {
            return !IGNORE.contains(e.file_name().to_str().unwrap());
        })
        .filter_map(|e| e.ok())
        .for_each(|e| {
            let file_path = e.into_path();
            if !file_path.is_dir() {
                process_file(&file_path, &action, hostname);
            }
        })
}

trait PrepareRunner {
    fn run(&self, args: &Cli, hostname: &str);
}

struct PrepareRunnerImpl {}
impl PrepareRunner for PrepareRunnerImpl {
    fn run(&self, args: &Cli, hostname: &str) {
        let action = action_from_args(&args);
        inspect_dir(
            args.dir.to_string().as_str(),
            &action,
            args.follow_sym,
            hostname,
        )
    }
}

fn main() {
    let args = Cli::parse();
    let hostname = gethostname().into_string().unwrap();
    PrepareRunnerImpl {}.run(&args, &hostname);
}
