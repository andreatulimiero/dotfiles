use std::collections::HashSet;
use std::path::PathBuf;
use walkdir::WalkDir;

pub trait FilesExplorer {
    fn files_iterator(&self) -> Box<dyn Iterator<Item = PathBuf>>;
}

pub struct WalkDirFilesExplorer<'a> {
    root_dirname: &'a str,
    follow_sym: bool,
}
impl<'a> WalkDirFilesExplorer<'a> {
    pub fn new(root_dirname: &'a str, follow_sym: bool) -> Self {
        Self {
            root_dirname,
            follow_sym
        }
    }
}
impl<'a> FilesExplorer for WalkDirFilesExplorer<'a> {
    fn files_iterator(&self) -> Box<dyn Iterator<Item = PathBuf>> {
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
        Box::new(
            WalkDir::new(self.root_dirname)
                .follow_links(self.follow_sym)
                .into_iter()
                .filter_entry(|e| {
                    return !IGNORE.contains(e.file_name().to_str().unwrap());
                })
                .filter_map(|e| e.ok())
                .filter_map(|e| {
                    let path = e.into_path();
                    if path.is_dir() {
                        Some(path)
                    } else {
                        None
                    }
                }),
        )
    }
}


