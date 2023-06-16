use crate::preparer::Preparer;
use clap::Parser;
use gethostname::gethostname;
#[macro_use]
extern crate lazy_static;

mod cli;
mod files_explorer;
mod preparer;

fn main() {
    let args = cli::Cli::parse();
    let hostname = gethostname().into_string().unwrap();
    let files_explorer: &dyn files_explorer::FilesExplorer =
        &files_explorer::WalkDirFilesExplorer::new(
            args.dir.as_str(),
            args.follow_sym,
        );
    preparer::PreparerImpl::new(files_explorer).run(&args, &hostname);
}
