use regex::Regex;
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;

use crate::cli::{action_from_args, Action, Cli};
use crate::files_explorer::FilesExplorer;

pub trait Preparer {
    fn run(&self, args: &Cli, hostname: &str);
}

pub struct PreparerImpl<'a> {
    files_explorer: &'a dyn FilesExplorer,
}
impl <'a> PreparerImpl<'a> {
    pub fn new(files_explorer: &'a dyn FilesExplorer) -> Self {
        Self {
            files_explorer
        }
    }
}
impl<'a> Preparer for PreparerImpl<'a> {
    fn run(&self, args: &Cli, hostname: &str) {
        let action = action_from_args(&args);
        for file_path in self.files_explorer.files_iterator() {
            process_file(&file_path, &action, hostname);
        }
    }
}

fn process_file(file: &PathBuf, action: &Action, hostname: &str) {
    let res = std::fs::read_to_string(file);
    let mut lines: Vec<String> = Vec::new();
    match res {
        Ok(content) => {
            let mut match_found = false;
            for line in content.lines() {
                let (modified_line, line_matches) =
                    process_line(&line, &action, hostname);
                lines.push(modified_line);
                match_found |= line_matches;
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

fn process_line(line: &str, action: &Action, hostname: &str) -> (String, bool) {
    lazy_static! {
        static ref RE: Regex = Regex::new(r">\s*\[(?P<comment_start>[^0-9A-Za-z]+)@(?P<comment_end>[^0-9A-Za-z]+)(?P<hostname>[0-9A-Za-z]+)\]").unwrap();
    }
    match RE.captures(line) {
        Some(cap) => {
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
            (modified_line, true)
        }
        None => (line.to_string(), false),
    }
}

fn get_actual_comment_end(comment_end: &str) -> Option<&str> {
    match comment_end {
        "_" => None,
        _ => Some(comment_end),
    }
}

fn is_commented(
    line: &str,
    comment_start: &str,
    comment_end: Option<&str>,
) -> bool {
    line.starts_with(comment_start)
        && comment_end.map_or(true, |e| line.ends_with(e))
}

fn comment_line(
    line: &str,
    comment_start: &str,
    comment_end: Option<&str>,
) -> String {
    if is_commented(line, comment_start, comment_end) {
        line.to_string()
    } else {
        format!("{}{}{}", comment_start, line, comment_end.unwrap_or(""))
    }
}

fn decomment_line(
    line: &str,
    comment_start: &str,
    comment_end: Option<&str>,
) -> String {
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
    let line_without_start = line.replacen(comment_start, "", 1);
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
