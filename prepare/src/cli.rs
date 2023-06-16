use clap::Parser;

#[derive(Parser, Debug)]
pub struct Cli {
    #[arg(short = 'C', long, default_value = ".")]
    pub dir: String,
    #[arg(short, long, default_value_t = false)]
    pub comment: bool,
    #[arg(short, long, default_value_t = false)]
    pub decomment: bool,
    #[arg(short, long, default_value_t = false)]
    pub follow_sym: bool,
}

#[derive(Debug)]
pub enum Action {
    COMMENT,
    UNCOMMENT,
    PREPARE,
}

pub fn action_from_args(args: &Cli) -> Action {
    if args.comment {
        Action::COMMENT
    } else if args.decomment {
        Action::UNCOMMENT
    } else {
        Action::PREPARE
    }
}


